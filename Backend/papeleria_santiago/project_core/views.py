from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404
from django.template.loader import get_template
from io import BytesIO
from xhtml2pdf import pisa
from django.core import signing
from django.core.mail import send_mail
from django.urls import reverse
from urllib.parse import quote
from django.views.decorators.clickjacking import xframe_options_exempt
from django.db.models import Q, F
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.utils.text import slugify
from django.utils import timezone
from django.db import transaction
from decimal import Decimal, InvalidOperation
from datetime import timedelta
import secrets
from .models import Comprobante, Pedido, Producto, Carrito, DetalleCarrito, Cliente, DetallePedido, Inventario, Subcategoria, Transportista # Importamos DetallePedido, Inventario y Subcategoria
from .models import PreRegistroUser, PasswordResetOtp
from rest_framework import viewsets, filters, status, mixins, permissions, serializers # Importar filters, status, mixins, permissions y serializers
from rest_framework import generics
from rest_framework.decorators import action # Importar action
from django_filters.rest_framework import DjangoFilterBackend # Importar DjangoFilterBackend
from .serializers import (
    ProductoSerializer,
    CarritoSerializer,
    DetalleCarritoSerializer,
    FavoritosClienteSerializer,
    SubcategoriaSerializer,
    PedidoSerializer,
    ClientePerfilSerializer,
    InitRegisterSerializer,
    VerifyOtpSerializer,
    ResendOtpSerializer,
    SolicitarRecuperacionSerializer,
    ConfirmarRecuperacionSerializer,
) # Importar el serializador
from rest_framework.response import Response # Importar Response
from .models import FavoritosCliente # Importar el modelo FavoritosCliente
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.pagination import PageNumberPagination

# Create your views here.

# ------------------
# Aquí es en dónde se generará el comprobante de pago mediante un canal HTTP hacia la interfaz
#------------------

# La factura se genera a partir del ID del pedido; caso de no existir factura retornar 404. 
# La siguiente anotación permite quitar X-FRAME-OPTIONS de DENY para que se pueda mostrar en el frontend 
@xframe_options_exempt
def generar_factura_pdf(request, pedido_id):
    # --- Seguridad (Opción B): URL firmada con expiración ---
    # Nota: este endpoint NO requiere token/cookie porque suele usarse en <iframe>.
    # Para privacidad, si no hay token válido o no corresponde al pedido_id, retornamos 404.
    token_firma = request.GET.get('token')
    if not token_firma:
        raise Http404("No encontrado.")

    # Token expira rápido para minimizar riesgo si alguien lo comparte/filtra.
    # Ajustable: 5-15 minutos es un rango razonable para vista previa y descarga.
    PDF_TOKEN_MAX_AGE_SECONDS = 10 * 60
    signer = signing.TimestampSigner(salt='comprobante_pdf')

    try:
        unsigned_value = signer.unsign(token_firma, max_age=PDF_TOKEN_MAX_AGE_SECONDS)
    except signing.BadSignature:
        raise Http404("No encontrado.")

    if str(unsigned_value) != str(pedido_id):
        raise Http404("No encontrado.")

    # Obtener el objeto Pedido o retornar un 404 si no existe
    pedido = get_object_or_404(Pedido, id=pedido_id)
    
    # Intentar obtener el Comprobante asociado al Pedido
    try:
        comprobante = pedido.comprobante # Accedemos al Comprobante a través del related_name por defecto
    except Comprobante.DoesNotExist:
        return HttpResponse("No se encontró un comprobante para este pedido.", status=404)

    # Cargar la plantilla HTML
    template_path = 'project_core/factura_pdf.html'
    template = get_template(template_path)

    # Crear el contexto para la plantilla (pasamos el objeto comprobante)
    context = {'comprobante': comprobante}
    html = template.render(context)

    # Crear el objeto HttpResponse con el tipo de contenido PDF
    response = HttpResponse(content_type='application/pdf')

    # Configurar el encabezado para:
    # - mostrar embebido (iframe) por defecto (inline)
    # - forzar descarga si viene ?download=1
    download = request.GET.get('download')
    disposition = 'attachment' if str(download).lower() in ('1', 'true', 'yes') else 'inline'
    response['Content-Disposition'] = f'{disposition}; filename="factura_{comprobante.numero_factura}.pdf"'

    # Generar el PDF usando xhtml2pdf
    pisa_status = pisa.CreatePDF(
        html, dest=response) # El HTML a convertir y dónde se guardará el PDF (en la respuesta HTTP)

    # Si hubo errores durante la generación del PDF
    if pisa_status.err:
        return HttpResponse('Tuvimos algunos errores al generar el PDF: <pre>' + html + '</pre>')
    return response

#------------------
# ViewSet para el modelo Producto (API REST)
# Maneja las peticiones GET, POST, PUT, DELETE para productos
#------------------

class ProductoPagination(PageNumberPagination):
    # Paginación estándar DRF: {count,next,previous,results}
    page_size = 9


class ProductoViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer
    pagination_class = ProductoPagination
    filter_backends = [DjangoFilterBackend] # Añadir backends de filtro y búsqueda
    filterset_fields = ['categoria', 'marca', 'SKU'] # Filtrar por categoría, marca y SKU
    search_fields = ['nombre', 'marca'] # Campos para búsqueda de texto
    ordering_fields = ['SKU', 'nombre', 'pvp', 'pvm'] # Campos para ordenar resultados

    # Para filtrar por rango de precio, podemos sobrescribir el método get_queryset
    def get_queryset(self):
        queryset = super().get_queryset()

        # ----------------
        # Catálogo reactivo para mayoristas:
        # Si viene token de Empresa ACTIVO, ocultamos productos marcados como no disponibles para mayorista.
        # ----------------
        try:
            user = getattr(self.request, 'user', None)
            cliente = getattr(user, 'cliente_profile', None) if user and getattr(user, 'is_authenticated', False) else None
            is_mayorista_activo = bool(
                cliente
                and cliente.tipo_cliente == Cliente.EMPRESA
                and cliente.estado_cuenta == Cliente.ACTIVO
            )
        except Exception:
            is_mayorista_activo = False

        if is_mayorista_activo:
            queryset = queryset.filter(disponible_mayorista=True)

        # Anotar precios (desde el OneToOne `precios`) para:
        # - permitir ordering=pvp / ordering=pvm aunque no sean campos físicos en Producto
        # - mantener compatibilidad con el frontend
        queryset = queryset.annotate(
            pvp=F('precios__pvp'),
            pvm=F('precios__pvm'),
        )

        # Búsqueda custom (equivalente a SearchFilter, con tolerancia simple a plurales):
        # Ej: "cuadernos" también prueba "cuaderno" (quitando 's' / 'es')
        search = self.request.query_params.get('search')
        if search:
            terms = [t.strip() for t in str(search).split() if t.strip()]
            for term in terms:
                term_lower = term.lower()
                variantes = {term_lower}

                # Heurística simple de singularización (ES):
                # - "cuadernos" -> "cuaderno"
                # - "lápices"   -> "lápic" (ojo: no perfecto, pero ayuda en varios casos)
                if len(term_lower) > 3 and term_lower.endswith('es'):
                    variantes.add(term_lower[:-2])
                if len(term_lower) > 3 and term_lower.endswith('s'):
                    variantes.add(term_lower[:-1])

                term_q = Q()
                for v in variantes:
                    term_q |= Q(nombre__icontains=v) | Q(marca__icontains=v)

                queryset = queryset.filter(term_q)

        precio_min = self.request.query_params.get('precio_min')
        precio_max = self.request.query_params.get('precio_max')

        # Para mayorista ACTIVO filtramos por precio base mayorista (PVM).
        # Para público / Persona filtramos por precio base público (PVP).
        precio_base_field = 'precios__pvm' if is_mayorista_activo else 'precios__pvp'

        if precio_min:
            # Asumimos que `precios` es el related_name del OneToOneField del Precio
            # que apunta a Producto. Para filtrar por precio en el modelo Precio,
            # necesitamos acceder a `precios__pvp` o `precios__pvm`.
            # Vamos a usar `precios__pvp` para este ejemplo.
            queryset = queryset.filter(**{f"{precio_base_field}__gte": precio_min})
        if precio_max:
            queryset = queryset.filter(**{f"{precio_base_field}__lte": precio_max})
            
        # Filtrar por nombre de subcategoría (case-insensitive)
        subcategoria_nombre = self.request.query_params.get('subcategoria')
        if subcategoria_nombre:
            queryset = queryset.filter(subcategoria__nombre_subcategoria__iexact=subcategoria_nombre)

        # Filtrar por descuento mínimo y por descuento máximo.
        descuento_min = self.request.query_params.get('descuento_min')
        descuento_max = self.request.query_params.get('descuento_max') 

        # Para mayorista ACTIVO filtramos/ordenamos por descuento mayorista.
        # Para público / Persona filtramos/ordenamos por descuento público.
        descuento_field = 'precios__descuento_mayorista' if is_mayorista_activo else 'precios__descuento_publico'

        if descuento_min and descuento_max:
            try:
                descuento_min = float(descuento_min)
                descuento_max = float(descuento_max)
                queryset = queryset.filter(**{f"{descuento_field}__gte": descuento_min, f"{descuento_field}__lte": descuento_max})
            except ValueError:
                pass
        elif descuento_min:
            try:
                descuento_min = float(descuento_min)
                queryset = queryset.filter(**{f"{descuento_field}__gte": descuento_min})
            except ValueError:
                pass # Ignorar si el valor no es un número válido
        elif descuento_max:
            try:
                descuento_max = float(descuento_max)
                queryset = queryset.filter(**{f"{descuento_field}__lte": descuento_max})
            except ValueError:
                pass

        # Ordering “custom” para el frontend (aliases):
        # - ordering=total_vendidos  -> más vendidos primero
        # - ordering=descuento       -> mayor descuento primero (público o mayorista según el usuario)
        # - ordering=alphabet        -> nombre A-Z
        #
        # Nota: lo hacemos aquí (y NO vía OrderingFilter) porque OrderingFilter:
        # - no soporta aliases personalizados
        # - y ordering_fields no permite definir el sentido default (ej. desc por defecto)
        ordering = self.request.query_params.get('ordering')
        if ordering:
            ordering = str(ordering).strip()
            is_desc = ordering.startswith('-')
            key = ordering[1:] if is_desc else ordering

            # Aliases del frontend
            if key == 'total_vendidos':
                # default: DESC (más vendidos primero)
                queryset = queryset.order_by('total_vendidos' if is_desc else '-total_vendidos')
            elif key == 'descuento':
                # default: DESC (mayor descuento primero)
                queryset = queryset.order_by(f"{descuento_field}" if is_desc else f"-{descuento_field}")
            elif key == 'alphabet':
                # default: ASC (A-Z)
                queryset = queryset.order_by('-nombre' if is_desc else 'nombre')

            # Campos directos (compatibilidad con DRF OrderingFilter anterior)
            elif key in ('SKU', 'nombre', 'pvp', 'pvm'):
                queryset = queryset.order_by(f"-{key}" if is_desc else key)

        # Default ordering (lista plana, sin agrupaciones visuales):
        # - primero más vendidos (destacados)
        # - luego SKU para estabilidad
        # Nota: solo aplica si el frontend NO envía ordering.
        if not ordering:
            queryset = queryset.order_by('-total_vendidos', 'SKU')

        return queryset

    def list(self, request, *args, **kwargs):
        """
        Soporta ?limite=X sin romper búsqueda/filtros/ordering.
        (Importante: no se puede re-ordenar un queryset ya "cortado" con [:X].)
        """
        queryset = self.filter_queryset(self.get_queryset())

        # Aplicar límite al FINAL (después de filter_backends)
        limite = request.query_params.get('limite')
        if limite:
            try:
                limite = int(limite)
                queryset = queryset[:limite]
            except ValueError:
                pass # Ignorar si el valor no es un número entero válido

            # Compatibilidad: si el caller usa `limite`, devolvemos lista plana (sin paginar).
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)

        # Paginación: solo aplicarla cuando el frontend envía ?page=X
        # (Esto evita romper pantallas existentes que esperan lista completa.)
        if 'page' in request.query_params:
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def destacados(self, request):
        """ Retorna una lista de los productos más vendidos (destacados). """
        limite = self.request.query_params.get('limite', 50) # Permitir un límite configurable, por defecto 50
        try:
            limite = int(limite)
        except ValueError:
            return Response({'error': 'El parámetro limite debe ser un número entero.'}, status=status.HTTP_400_BAD_REQUEST)
        
        productos_destacados = Producto.objects.all()

        # Catálogo reactivo para mayoristas (ver get_queryset)
        try:
            user = getattr(self.request, 'user', None)
            cliente = getattr(user, 'cliente_profile', None) if user and getattr(user, 'is_authenticated', False) else None
            is_mayorista_activo = bool(
                cliente
                and cliente.tipo_cliente == Cliente.EMPRESA
                and cliente.estado_cuenta == Cliente.ACTIVO
            )
        except Exception:
            is_mayorista_activo = False

        if is_mayorista_activo:
            productos_destacados = productos_destacados.filter(disponible_mayorista=True)

        # Aplicar filtro por subcategoría si se proporciona
        subcategoria_nombre = self.request.query_params.get('subcategoria')
        if subcategoria_nombre:
            productos_destacados = productos_destacados.filter(subcategoria__nombre_subcategoria__iexact=subcategoria_nombre)

        productos_destacados = productos_destacados.order_by('-total_vendidos')[:limite]
        serializer = self.get_serializer(productos_destacados, many=True)
        return Response(serializer.data)


# -------------------
# AUTH - Registro en 2 pasos (OTP por email)
# -------------------
def _generate_otp_code():
    return str(secrets.randbelow(10**6)).zfill(6)


def _generate_unique_username(email, first_name=None):
    # Username debe ser único en Django User.
    base = slugify((first_name or '').strip()) or slugify(email.split('@')[0])
    base = (base or 'user')[:120]

    candidate = base
    i = 0
    while User.objects.filter(username=candidate).exists():
        i += 1
        suffix = str(secrets.randbelow(10**6)).zfill(6)
        candidate = f"{base}-{suffix}"[:150]
        if i > 10:
            # fallback súper conservador
            candidate = f"user-{suffix}"
            break
    return candidate


def _send_otp_email(to_email, otp_code):
    subject = "Tu código de verificación - Papelería Santiago"
    message = f"Tu código de verificación es: {otp_code}\n\nSi no solicitaste este registro, ignora este correo."
    from_email = getattr(settings, 'DEFAULT_FROM_EMAIL', None) or settings.EMAIL_HOST_USER
    sent = send_mail(subject, message, from_email, [to_email], fail_silently=False)
    return sent


def _send_password_reset_otp_email(to_email, otp_code):
    subject = "Tu código para recuperar contraseña - Papelería Santiago"
    message = (
        f"Tu código de verificación para recuperar tu contraseña es: {otp_code}\n\n"
        f"Si no solicitaste este cambio, ignora este correo."
    )
    from_email = getattr(settings, 'DEFAULT_FROM_EMAIL', None) or settings.EMAIL_HOST_USER
    sent = send_mail(subject, message, from_email, [to_email], fail_silently=False)
    return sent


def _send_empresa_pending_email(to_email):
    """
    Correo informativo para cuentas mayoristas (Empresa) que quedan en estado PENDIENTE.
    Nota: no contiene OTP, es solo comunicación post-registro.
    """
    subject = "Cuenta mayorista en revisión - Papelería Santiago"
    message = (
        "Tu cuenta ha sido creada exitosamente.\n\n"
        "Te enviaremos un correo cuando sea aprobada por nuestro equipo de administración.\n\n"
        "Atentamente:\n"
        "Papelería Santiago"
    )
    from_email = getattr(settings, 'DEFAULT_FROM_EMAIL', None) or settings.EMAIL_HOST_USER
    sent = send_mail(subject, message, from_email, [to_email], fail_silently=False)
    return sent


def _send_persona_verified_email(to_email):
    """
    Correo informativo para cuentas Persona que quedan ACTIVO al verificar OTP.
    """
    subject = "Cuenta verificada - Papelería Santiago"
    message = (
        "Tu cuenta ha sido verificada, ya puedes iniciar sesión dentro de la tienda virtual Papelería Santiago."
    )
    from_email = getattr(settings, 'DEFAULT_FROM_EMAIL', None) or settings.EMAIL_HOST_USER
    sent = send_mail(subject, message, from_email, [to_email], fail_silently=False)
    return sent


class InitRegisterAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = InitRegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']
        first_name = serializer.validated_data.get('first_name') or ''
        password = serializer.validated_data['password']
        celular = serializer.validated_data.get('celular') or ''
        ciudad = serializer.validated_data.get('ciudad') or ''
        tipo_cliente = serializer.validated_data.get('tipo_cliente') or Cliente.PERSONA
        url_validacion = serializer.validated_data.get('url_validacion') or None

        # Seguridad: no permitir iniciar registro si ya existe usuario real (doble check)
        if User.objects.filter(email=email).exists():
            return Response({'error': 'Este correo ya está registrado.'}, status=status.HTTP_400_BAD_REQUEST)

        otp_code = _generate_otp_code()
        hashed_password = make_password(password)

        prereg, created = PreRegistroUser.objects.update_or_create(
            email=email,
            defaults={
                'first_name': first_name,
                'password': hashed_password,
                'celular': celular,
                'ciudad': ciudad,
                'tipo_cliente': tipo_cliente,
                'url_validacion': url_validacion,
                'otp_code': otp_code,
                'intentos': 0,
            }
        )

        try:
            _send_otp_email(email, otp_code)
        except Exception:
            # Si el envío falla, mantenemos el preregistro, pero avisamos
            return Response(
                {'error': 'No se pudo enviar el correo de verificación. Revisa la configuración SMTP.'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        return Response(
            {'message': 'Código enviado al correo. Verifica tu bandeja de entrada.', 'email': prereg.email},
            status=status.HTTP_200_OK
        )


class VerifyOtpAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = VerifyOtpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']
        otp = serializer.validated_data['otp']

        prereg = PreRegistroUser.objects.filter(email=email).first()
        if not prereg:
            return Response({'error': 'No existe un pre-registro para este correo.'}, status=status.HTTP_404_NOT_FOUND)

        if prereg.intentos >= 3:
            prereg.delete()
            return Response({'error': 'Bloqueado por seguridad.'}, status=status.HTTP_403_FORBIDDEN)

        if str(prereg.otp_code) != str(otp):
            prereg.intentos = (prereg.intentos or 0) + 1
            prereg.save(update_fields=['intentos', 'password', 'otp_code', 'first_name', 'celular', 'ciudad'])

            if prereg.intentos >= 3:
                prereg.delete()
                return Response({'error': 'Bloqueado por seguridad.'}, status=status.HTTP_403_FORBIDDEN)

            remaining = 3 - prereg.intentos
            return Response(
                {'error': f'Código incorrecto. Te quedan {remaining} intento(s).'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # OTP correcto: crear usuario real + perfil Cliente + carrito + token
        with transaction.atomic():
            if User.objects.filter(email=email).exists():
                prereg.delete()
                return Response({'error': 'Este correo ya está registrado.'}, status=status.HTTP_400_BAD_REQUEST)

            username = _generate_unique_username(email, prereg.first_name)
            tipo_cliente = getattr(prereg, 'tipo_cliente', Cliente.PERSONA) or Cliente.PERSONA
            is_empresa = tipo_cliente == Cliente.EMPRESA

            # Si es Empresa: nace PENDIENTE y NO puede logearse hasta aprobación (User.is_active=False)
            user = User.objects.create(
                username=username,
                email=email,
                first_name=prereg.first_name or '',
                password=prereg.password,  # ya está hasheada
                is_active=(not is_empresa),
            )

            cliente = Cliente.objects.create(
                user=user,
                nombre=(prereg.first_name or username),
                email=email,
                telefono=prereg.celular or '',
                ciudad=prereg.ciudad or '',
                tipo_cliente=tipo_cliente,
                url_validacion=(getattr(prereg, 'url_validacion', None) if is_empresa else None),
                estado_cuenta=(Cliente.PENDIENTE if is_empresa else Cliente.ACTIVO),
            )

            Carrito.objects.create(cliente=cliente)

            prereg.delete()

        # Respuesta: Persona -> token; Empresa -> mensaje sin token (queda en revisión)
        if is_empresa:
            # Enviar correo informativo (no bloquea el flujo si falla el envío)
            try:
                _send_empresa_pending_email(email)
            except Exception:
                pass
            return Response(
                {
                    'message': 'Cuenta en revisión. Te informaremos por correo cuando tu empresa sea validada.',
                    'email': email,
                },
                status=status.HTTP_200_OK
            )

        token, _ = Token.objects.get_or_create(user=user)

        # Correo informativo para Persona (no bloquea el flujo si falla el envío)
        try:
            _send_persona_verified_email(email)
        except Exception:
            pass

        return Response(
            {
                'message': 'Cuenta verificada exitosamente.',
                'token': token.key,
                'username': user.username,
                'email': user.email,
            },
            status=status.HTTP_200_OK
        )


class ResendOtpAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = ResendOtpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']
        prereg = PreRegistroUser.objects.filter(email=email).first()
        if not prereg:
            return Response({'error': 'No existe un pre-registro para este correo.'}, status=status.HTTP_404_NOT_FOUND)

        otp_code = _generate_otp_code()
        prereg.otp_code = otp_code
        prereg.intentos = 0
        prereg.save(update_fields=['otp_code', 'intentos', 'password', 'first_name', 'celular', 'ciudad'])

        try:
            _send_otp_email(email, otp_code)
        except Exception:
            return Response(
                {'error': 'No se pudo reenviar el correo de verificación. Revisa la configuración SMTP.'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        return Response(
            {'message': 'Se envió un nuevo código de verificación.', 'email': email},
            status=status.HTTP_200_OK
        )


# -------------------
# Recuperación de contraseña (OTP por email, 2 pasos)
# -------------------
PASSWORD_RESET_OTP_TTL_SECONDS = 10 * 60  # 10 minutos
PASSWORD_RESET_MAX_RESENDS = 3            # máximo 3 reenvíos (no incluye el envío inicial)
PASSWORD_RESET_BLOCK_MINUTES = 15         # bloqueo temporal si excede reenvíos


class SolicitarRecuperacionAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = SolicitarRecuperacionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']

        # Respuesta genérica por seguridad (NO filtrar existencia de email)
        generic_message = "Si el correo existe, se ha enviado un código de verificación."

        user = User.objects.filter(email=email).first()
        if not user:
            # Importante: NO generar ni enviar OTP si el correo no existe
            return Response({'message': generic_message}, status=status.HTTP_200_OK)

        # Solo permitir recuperación si la cuenta está ACTIVA (Persona o Empresa)
        if not user.is_active:
            return Response({'message': generic_message}, status=status.HTTP_200_OK)
        try:
            cliente = user.cliente_profile
        except Cliente.DoesNotExist:
            cliente = None
        if cliente and getattr(cliente, 'estado_cuenta', None) and cliente.estado_cuenta != Cliente.ACTIVO:
            return Response({'message': generic_message}, status=status.HTTP_200_OK)

        now = timezone.now()

        # Si existe OTP previo, evaluar expiración y bloqueo
        existing = PasswordResetOtp.objects.filter(email=email).first()
        if existing:
            # Bloqueo temporal por exceso de reenvíos
            if existing.blocked_until and now < existing.blocked_until:
                return Response({'message': generic_message}, status=status.HTTP_200_OK)

            # Expiración basada en último envío (sent_at) o created_at como fallback
            last_sent_at = existing.sent_at or existing.created_at
            if last_sent_at and (now - last_sent_at).total_seconds() > PASSWORD_RESET_OTP_TTL_SECONDS:
                existing.delete()
                existing = None

        otp_code = _generate_otp_code()

        if not existing:
            # Primer envío: contador inicia en 0
            PasswordResetOtp.objects.update_or_create(
                email=email,
                defaults={
                    'otp_code': otp_code,
                    'resend_count': 0,
                    'sent_at': now,
                    'blocked_until': None,
                }
            )
        else:
            # Reenvío: máximo 3 reenvíos
            if (existing.resend_count or 0) >= PASSWORD_RESET_MAX_RESENDS:
                existing.blocked_until = now + timedelta(minutes=PASSWORD_RESET_BLOCK_MINUTES)
                existing.save(update_fields=['blocked_until'])
                return Response({'message': generic_message}, status=status.HTTP_200_OK)

            existing.otp_code = otp_code
            existing.resend_count = (existing.resend_count or 0) + 1
            existing.sent_at = now
            existing.blocked_until = None
            existing.save(update_fields=['otp_code', 'resend_count', 'sent_at', 'blocked_until'])

        try:
            _send_password_reset_otp_email(email, otp_code)
        except Exception:
            return Response(
                {'error': 'No se pudo enviar el correo de recuperación. Revisa la configuración SMTP.'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        return Response({'message': generic_message}, status=status.HTTP_200_OK)


class ConfirmarRecuperacionAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = ConfirmarRecuperacionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']
        otp_code = serializer.validated_data['otp_code']
        new_password = serializer.validated_data['new_password']
        confirm_password = serializer.validated_data['confirm_password']

        if new_password != confirm_password:
            return Response({'error': 'Las contraseñas no coinciden.'}, status=status.HTTP_400_BAD_REQUEST)

        otp_obj = PasswordResetOtp.objects.filter(email=email).first()
        if not otp_obj:
            return Response({'error': 'Código inválido o expirado.'}, status=status.HTTP_400_BAD_REQUEST)

        now = timezone.now()
        last_sent_at = otp_obj.sent_at or otp_obj.created_at
        if last_sent_at and (now - last_sent_at).total_seconds() > PASSWORD_RESET_OTP_TTL_SECONDS:
            otp_obj.delete()
            return Response({'error': 'Código inválido o expirado.'}, status=status.HTTP_400_BAD_REQUEST)

        # Coincidencia exacta del OTP (prioridad de seguridad)
        if str(otp_obj.otp_code) != str(otp_code):
            return Response({'error': 'Código inválido o expirado.'}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.filter(email=email).first()
        if not user:
            # Caso raro: usuario eliminado tras generar OTP
            otp_obj.delete()
            return Response({'error': 'Código inválido o expirado.'}, status=status.HTTP_400_BAD_REQUEST)

        # Bloquear recuperación si la cuenta no está ACTIVA
        if not user.is_active:
            otp_obj.delete()
            return Response({'error': 'Código inválido o expirado.'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            cliente = user.cliente_profile
        except Cliente.DoesNotExist:
            cliente = None
        if cliente and getattr(cliente, 'estado_cuenta', None) and cliente.estado_cuenta != Cliente.ACTIVO:
            otp_obj.delete()
            return Response({'error': 'Código inválido o expirado.'}, status=status.HTTP_400_BAD_REQUEST)

        with transaction.atomic():
            user.set_password(new_password)
            user.save(update_fields=['password'])
            otp_obj.delete()

        return Response({'message': 'Contraseña actualizada exitosamente.'}, status=status.HTTP_200_OK)


#------------------
# ViewSet para el modelo Carrito (API REST)
# Maneja las peticiones GET, POST, PUT, DELETE para carritos
#------------------
class CarritoViewSet(viewsets.ModelViewSet):
    queryset = Carrito.objects.all()
    serializer_class = CarritoSerializer

    @action(detail=True, methods=['post'])
    def pagar(self, request, pk=None):
        carrito = self.get_object() # Obtiene el carrito basado en el pk de la URL

        # --- 1. Autorización (simplificada por ahora, asumiendo usuario autenticado) ---
        # TODO: Implementar un sistema de autenticación y permisos más robusto.
        # Por ahora, verificamos si el cliente del carrito está asociado a un usuario
        #!!if not request.user.is_authenticated:
            #!!return Response({'error': 'Autenticación requerida para realizar el pago.'}, status=status.HTTP_403_FORBIDDEN)
        
        # Si el carrito no tiene un cliente asociado, o si el cliente no está vinculado a un User
        # o si el usuario autenticado no coincide con el cliente del carrito.
        #!!if not carrito.cliente or not carrito.cliente.user or carrito.cliente.user != request.user:
        #!!    return Response({'error': 'No tienes permiso para pagar este carrito.'}, status=status.HTTP_403_FORBIDDEN)


        # --- 2. Validar Carrito --- 
        #!!if not carrito.detalles_carrito.exists():
        #!!    return Response({'error': 'El carrito está vacío, no se puede realizar el pago.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            with transaction.atomic():
                # Datos de envío (snapshot): aceptar del body, fallback a Cliente para compatibilidad.
                ciudad_envio = (request.data.get('ciudad_envio') or carrito.cliente.ciudad or '').strip() or None
                direccion_envio = (request.data.get('direccion_envio') or carrito.cliente.direccion or '').strip() or None
                numero_casa_envio = (request.data.get('numero_casa_envio') or '').strip() or None
                codigo_postal_envio = (request.data.get('codigo_postal_envio') or '').strip() or None
                cedula_envio = (request.data.get('cedula_envio') or carrito.cliente.cedula or '').strip() or None
                telefono_envio = (request.data.get('telefono_envio') or carrito.cliente.telefono or '').strip() or None
                referencia_envio = (request.data.get('referencia_envio') or '').strip() or None

                metodo_pago = (request.data.get('metodo_pago') or 'Tarjeta').strip()
                if metodo_pago not in ('Tarjeta', 'Transferencia bancaria'):
                    return Response(
                        {'error': 'Método de pago inválido. Opciones: Tarjeta, Transferencia bancaria.'},
                        status=status.HTTP_400_BAD_REQUEST
                    )

                # Costo de envío (Decimal >= 0). No asumimos 3.00: si no viene, usamos 0.00 por compatibilidad.
                raw_costo_envio = request.data.get('costo_envio')
                if raw_costo_envio is None or str(raw_costo_envio).strip() == '':
                    costo_envio = Decimal('0.00')
                else:
                    try:
                        costo_envio = Decimal(str(raw_costo_envio))
                    except (InvalidOperation, ValueError):
                        return Response({'error': 'costo_envio debe ser un número válido.'}, status=status.HTTP_400_BAD_REQUEST)
                    if costo_envio < 0:
                        return Response({'error': 'costo_envio no puede ser negativo.'}, status=status.HTTP_400_BAD_REQUEST)
                    costo_envio = costo_envio.quantize(Decimal('0.01'))

                is_transfer = metodo_pago == 'Transferencia bancaria'

                # Transferencia: requiere archivo (multipart/form-data)
                comprobante_file = None
                if is_transfer:
                    # Soporta ambos nombres por si el frontend varía
                    comprobante_file = request.FILES.get('comprobante_transferencia') or request.FILES.get('comprobante')
                    if not comprobante_file:
                        return Response(
                            {'error': 'Debes subir el comprobante de transferencia.'},
                            status=status.HTTP_400_BAD_REQUEST
                        )

                # --- 3. Crear Pedido ---
                pedido = Pedido.objects.create(
                    cliente=carrito.cliente,
                    estado_pedido=('En revisión' if is_transfer else 'Pagado'),
                    ciudad_envio=ciudad_envio,
                    direccion_envio=direccion_envio,
                    numero_casa_envio=numero_casa_envio,
                    codigo_postal_envio=codigo_postal_envio,
                    cedula_envio=cedula_envio,
                    telefono_envio=telefono_envio,
                    referencia_envio=referencia_envio,
                    metodo_pago=metodo_pago,
                    costo_envio=costo_envio,
                    comprobante_transferencia=(comprobante_file if is_transfer else None),
                )

                # --- 4. Crear DetallePedido a partir de DetalleCarrito ---
                for detalle_carrito in carrito.detalles_carrito.all():
                    DetallePedido.objects.create(
                        pedido=pedido,
                        producto=detalle_carrito.producto,
                        cantidad=detalle_carrito.cantidad,
                        precio_unitario=detalle_carrito.precio_unitario,
                        # Subtotal = antes de descuento (para que el desglose Subtotal/Descuento/IVA cuadre)
                        subtotal_detalle_pedido=detalle_carrito.subtotal_antes_descuento,
                        iva_detalle_pedido=detalle_carrito.iva_detalle_carrito, # Asegurarse de que este campo tenga valor en DetalleCarrito
                        descuento_detalle_pedido=detalle_carrito.descuento_detalle_carrito,
                        total_detalle_pedido=detalle_carrito.total_detalle_carrito,
                    )

                # --- 5. Comprobante + Envío ---
                # Tarjeta: se generan inmediatamente (flujo actual).
                # Transferencia: NO generar comprobante fiscal ni transportista hasta aprobación admin.
                if not is_transfer:
                    # --- 5.1 Crear Transportista (entrega) asociado al pedido ---
                    Transportista.objects.create(
                        pedido=pedido,
                        estado_entrega='Pendiente',
                    )

                    # --- 5.2 Crear Comprobante después de que todos los DetallePedido estén creados ---
                    Comprobante.objects.create(
                        pedido=pedido,
                        numero_factura=f"FAC-{pedido.id}-{pedido.fecha_pedido.strftime('%Y%m%d')}",
                        # Si no hay cédula, guardar NULL (evita strings largos y respeta blank/null)
                        cedula_cliente=(pedido.cedula_envio or pedido.cliente.cedula or None),
                        direccion_cliente=(pedido.direccion_envio or pedido.cliente.direccion),
                        email_cliente=pedido.cliente.email,
                        subtotal=pedido.subtotal_general_comprobante,
                        descuento=pedido.descuento_general_comprobante,
                        iva=pedido.iva_general_comprobante,
                        total=pedido.total_general_comprobante,
                        costo_envio=pedido.costo_envio,
                        metodo_pago=pedido.metodo_pago,
                        estado_fiscal='Emitido',
                    )
                
                # --- 6. Borrar DetalleCarrito del carrito original ---
                # Esto también hará que el carrito.estado_dinamico pase a 'Inactivo'
                carrito.detalles_carrito.all().delete()
                carrito.save() # Guarda el carrito para actualizar la fecha_actualizacion

            # TODO: DEVOLVER UNA RESPUESTA DETALLADA DEL PEDIDO CREADO EXITOSAMENTE
            if is_transfer:
                return Response(
                    {'message': 'Pedido creado. Pago en revisión (transferencia).', 'pedido_id': pedido.id},
                    status=status.HTTP_201_CREATED
                )
            return Response({'message': 'Carrito pagado y pedido creado exitosamente.', 'pedido_id': pedido.id}, status=status.HTTP_201_CREATED)

        except Exception as e:
            # Si ocurre un error, puedes considerar revertir la creación del pedido
            # o manejarlo de forma específica. Por simplicidad, por ahora solo lo reportamos.
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


#------------------
# ViewSet para el modelo DetalleCarrito (API REST)
# Maneja las peticiones GET, POST, PUT, DELETE para detalles de carrito
#------------------
class DetalleCarritoViewSet(viewsets.ModelViewSet):
    serializer_class = DetalleCarritoSerializer
    # Usaremos el SKU del producto como campo de búsqueda para DELETE y GET por detalle
    lookup_field = 'producto__SKU'

    def get_queryset(self):
        # Asegurarse de que solo se muestren los detalles del carrito padre
        return DetalleCarrito.objects.filter(carrito_id=self.kwargs['carrito_pk'])

    def create(self, request, *args, **kwargs):
        carrito_id = self.kwargs['carrito_pk']
        producto_sku = request.data.get('producto_sku')
        cantidad = request.data.get('cantidad')

        if not producto_sku or not cantidad:
            return Response({'error': 'Producto SKU y cantidad son requeridos.'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            carrito = Carrito.objects.get(id=carrito_id)
            producto = Producto.objects.get(SKU=producto_sku)
        except Carrito.DoesNotExist:
            return Response({'error': 'Carrito no encontrado.'}, status=status.HTTP_404_NOT_FOUND)
        except Producto.DoesNotExist:
            return Response({'error': 'Producto no encontrado.'}, status=status.HTTP_404_NOT_FOUND)
        
        # Validación de stock
        try:
            inventario = producto.inventario # Asumiendo related_name 'inventario' en Producto a Inventario
        except Inventario.DoesNotExist:
            return Response({'error': 'Producto sin registro de inventario.'}, status=status.HTTP_404_NOT_FOUND)

        # Buscar si el DetalleCarrito ya existe para este producto en este carrito
        try:
            detalle_carrito_existente = DetalleCarrito.objects.get(
                carrito=carrito,
                producto=producto
            )
            cantidad_previa = detalle_carrito_existente.cantidad
            
            # Validar el cambio de cantidad
            cambio_stock = cantidad - cantidad_previa
            if inventario.stock - cambio_stock < 0:
                return Response(
                    {'error': f'No hay suficiente stock para el producto {producto.nombre}. Stock disponible: {inventario.stock + cantidad_previa} (ya tienes {cantidad_previa} en el carrito)'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Actualizar el DetalleCarrito existente
            detalle_carrito_existente.cantidad = cantidad
            detalle_carrito_existente.save()
            inventario.stock -= cambio_stock # Restar el cambio neto del stock
            inventario.save()
            detalle_carrito = detalle_carrito_existente
            created = False
        except DetalleCarrito.DoesNotExist:
            # Si el DetalleCarrito no existe, es un nuevo item en el carrito
            if inventario.stock - cantidad < 0:
                 return Response(
                    {'error': f'No hay suficiente stock para el producto {producto.nombre}. Stock disponible: {inventario.stock}'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            detalle_carrito = DetalleCarrito.objects.create(
                carrito=carrito,
                producto=producto,
                cantidad=cantidad
            )
            inventario.stock -= cantidad # Restar la cantidad completa del stock
            inventario.save()
            created = True

        serializer = self.get_serializer(detalle_carrito)
        return Response(serializer.data, status=status.HTTP_200_OK if not created else status.HTTP_201_CREATED)

    def destroy(self, request, *args, **kwargs):
        carrito_id = self.kwargs['carrito_pk']
        producto_sku = self.kwargs['producto__SKU'] # Usamos el lookup_field

        try:
            carrito = Carrito.objects.get(id=carrito_id)
            detalle_carrito = DetalleCarrito.objects.get(carrito=carrito, producto__SKU=producto_sku)
        except Carrito.DoesNotExist:
            return Response({'error': 'Carrito no encontrado.'}, status=status.HTTP_404_NOT_FOUND)
        except DetalleCarrito.DoesNotExist:
            return Response({'error': 'Detalle de carrito no encontrado con ese producto.'}, status=status.HTTP_404_NOT_FOUND)
        
        # Antes de eliminar el DetalleCarrito, devolver la cantidad al stock
        producto = detalle_carrito.producto
        try:
            inventario = producto.inventario
            inventario.stock += detalle_carrito.cantidad
            inventario.save()
        except Inventario.DoesNotExist:
            # Si no hay inventario, se registra o se maneja como un error, pero no bloquea la eliminación del detalle
            print(f"Advertencia: Producto {producto.SKU} sin registro de inventario al eliminar detalle.")

        self.perform_destroy(detalle_carrito)
        return Response(status=status.HTTP_204_NO_CONTENT)

#-------------------
# Los ViewSet que se presentan a continuación son los usados para producción
# Requieren que se envíen los token de autenticación en la cabecera
#
#------------------
# ViewSet para el carrito del usuario autenticado (API REST)
#------------------
class MiCarritoViewSet(mixins.RetrieveModelMixin, viewsets.GenericViewSet): # Quitar mixins.ListModelMixin
    serializer_class = CarritoSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [JSONParser, FormParser, MultiPartParser]

    def get_object(self):
        user = self.request.user
        try:
            cliente = user.cliente_profile
            carrito = cliente.carritos.filter(detalles_carrito__isnull=False).first()
            if not carrito:
                carrito = cliente.carritos.first()
                if not carrito:
                    carrito = Carrito.objects.create(cliente=cliente)
            return carrito
        except Cliente.DoesNotExist:
            # Nota: levantar un Http404 (no un status code) para que DRF lo convierta a respuesta válida.
            raise Http404("Perfil de cliente no encontrado para este usuario.")

    @action(detail=False, methods=['get'], url_path='obtener') # Nueva acción para GET /api/mi-carrito/obtener/
    def retrieve_my_cart(self, request):
        carrito = self.get_object()
        serializer = self.get_serializer(carrito)
        return Response(serializer.data)

    @action(detail=False, methods=['post'], url_path='pagar')
    def pagar(self, request):
        carrito = self.get_object() # Obtiene el carrito del usuario autenticado

        # --- 1. Autorización (ya manejada por permission_classes = [permissions.IsAuthenticated]) ---
        # Asegurarse de que el carrito realmente pertenezca al usuario autenticado (doble chequeo)
        if not carrito.cliente or not carrito.cliente.user or carrito.cliente.user != request.user:
            return Response({'error': 'No tienes permiso para pagar este carrito.'}, status=status.HTTP_403_FORBIDDEN)

        # --- 2. Validar Carrito ---
        if not carrito.detalles_carrito.exists():
            return Response({'error': 'El carrito está vacío, no se puede realizar el pago.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            with transaction.atomic():
                # ----------------
                # Datos de envío (snapshot)
                # - MVP: el frontend puede enviarlos en el body
                # - Compatibilidad: si no vienen, copiamos desde Cliente (para no romper el flujo actual)
                # ----------------
                ciudad_envio = (request.data.get('ciudad_envio') or carrito.cliente.ciudad or '').strip() or None
                direccion_envio = (request.data.get('direccion_envio') or carrito.cliente.direccion or '').strip() or None
                numero_casa_envio = (request.data.get('numero_casa_envio') or '').strip() or None
                codigo_postal_envio = (request.data.get('codigo_postal_envio') or '').strip() or None
                cedula_envio = (request.data.get('cedula_envio') or carrito.cliente.cedula or '').strip() or None
                telefono_envio = (request.data.get('telefono_envio') or carrito.cliente.telefono or '').strip() or None
                referencia_envio = (request.data.get('referencia_envio') or '').strip() or None

                metodo_pago = (request.data.get('metodo_pago') or 'Tarjeta').strip()
                if metodo_pago not in ('Tarjeta', 'Transferencia bancaria'):
                    return Response(
                        {'error': 'Método de pago inválido. Opciones: Tarjeta, Transferencia bancaria.'},
                        status=status.HTTP_400_BAD_REQUEST
                    )

                # Costo de envío (Decimal >= 0). No asumimos 3.00: si no viene, usamos 0.00 por compatibilidad.
                raw_costo_envio = request.data.get('costo_envio')
                if raw_costo_envio is None or str(raw_costo_envio).strip() == '':
                    costo_envio = Decimal('0.00')
                else:
                    try:
                        costo_envio = Decimal(str(raw_costo_envio))
                    except (InvalidOperation, ValueError):
                        return Response({'error': 'costo_envio debe ser un número válido.'}, status=status.HTTP_400_BAD_REQUEST)
                    if costo_envio < 0:
                        return Response({'error': 'costo_envio no puede ser negativo.'}, status=status.HTTP_400_BAD_REQUEST)
                    costo_envio = costo_envio.quantize(Decimal('0.01'))

                is_transfer = metodo_pago == 'Transferencia bancaria'

                # Transferencia: requiere archivo (multipart/form-data)
                comprobante_file = None
                if is_transfer:
                    comprobante_file = request.FILES.get('comprobante_transferencia') or request.FILES.get('comprobante')
                    if not comprobante_file:
                        return Response(
                            {'error': 'Debes subir el comprobante de transferencia.'},
                            status=status.HTTP_400_BAD_REQUEST
                        )

                # --- 3. Crear Pedido ---
                pedido = Pedido.objects.create(
                    cliente=carrito.cliente,
                    estado_pedido=('En revisión' if is_transfer else 'Pagado'),
                    ciudad_envio=ciudad_envio,
                    direccion_envio=direccion_envio,
                    numero_casa_envio=numero_casa_envio,
                    codigo_postal_envio=codigo_postal_envio,
                    cedula_envio=cedula_envio,
                    telefono_envio=telefono_envio,
                    referencia_envio=referencia_envio,
                    metodo_pago=metodo_pago,
                    costo_envio=costo_envio,
                    comprobante_transferencia=(comprobante_file if is_transfer else None),
                )

                # --- 4. Crear DetallePedido a partir de DetalleCarrito ---
                for detalle_carrito in carrito.detalles_carrito.all():
                    DetallePedido.objects.create(
                        pedido=pedido,
                        producto=detalle_carrito.producto,
                        cantidad=detalle_carrito.cantidad,
                        precio_unitario=detalle_carrito.precio_unitario,
                        # Subtotal = antes de descuento (para que el desglose Subtotal/Descuento/IVA cuadre)
                        subtotal_detalle_pedido=detalle_carrito.subtotal_antes_descuento,
                        iva_detalle_pedido=detalle_carrito.iva_detalle_carrito,
                        descuento_detalle_pedido=detalle_carrito.descuento_detalle_carrito,
                        total_detalle_pedido=detalle_carrito.total_detalle_carrito,
                    )

                # --- 5. Comprobante + Envío ---
                # Tarjeta: se generan inmediatamente (flujo actual).
                # Transferencia: NO generar comprobante fiscal ni transportista hasta aprobación admin.
                if not is_transfer:
                    Transportista.objects.create(
                        pedido=pedido,
                        estado_entrega='Pendiente',
                    )

                    Comprobante.objects.create(
                        pedido=pedido,
                        numero_factura=f"FAC-{pedido.id}-{pedido.fecha_pedido.strftime('%Y%m%d')}",
                        # Si no hay cédula, guardar NULL (evita strings largos y respeta blank/null)
                        cedula_cliente=(pedido.cedula_envio or pedido.cliente.cedula or None),
                        # Usar snapshot de envío del pedido (histórico)
                        direccion_cliente=(pedido.direccion_envio or pedido.cliente.direccion),
                        email_cliente=pedido.cliente.email,
                        subtotal=pedido.subtotal_general_comprobante,
                        descuento=pedido.descuento_general_comprobante,
                        iva=pedido.iva_general_comprobante,
                        total=pedido.total_general_comprobante,
                        costo_envio=pedido.costo_envio,
                        metodo_pago=pedido.metodo_pago,
                        estado_fiscal='Emitido',
                    )

                # --- 6. Borrar DetalleCarrito del carrito original ---
                carrito.detalles_carrito.all().delete()
                carrito.save() # Guarda el carrito para actualizar la fecha_actualizacion

            if is_transfer:
                return Response(
                    {'message': 'Pedido creado. Pago en revisión (transferencia).', 'pedido_id': pedido.id},
                    status=status.HTTP_201_CREATED
                )
            return Response({'message': 'Carrito pagado y pedido creado exitosamente.', 'pedido_id': pedido.id}, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['get'], url_path='conteo')
    def conteo(self, request):
        """
        Retorna el número total de ítems distintos en el carrito del usuario autenticado.
        """
        carrito = self.get_object() # Obtiene el carrito del usuario autenticado
        # `detalles_carrito.count()` cuenta cuántos objetos DetalleCarrito hay.
        # Cada DetalleCarrito representa un tipo de producto distinto en el carrito.
        item_count = carrito.detalles_carrito.count()
        return Response({'conteo_items_carrito': item_count}, status=status.HTTP_200_OK)

#------------------
# ViewSet para los detalles del carrito del usuario autenticado (API REST)
#------------------
class MiCarritoDetalleViewSet(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet
):
    serializer_class = DetalleCarritoSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'producto__SKU'

    def get_queryset(self):
        user = self.request.user
        try:
            cliente = user.cliente_profile
            carrito = cliente.carritos.first() # Obtener el primer carrito del cliente
            if not carrito:
                raise Carrito.DoesNotExist("No active cart found for this user.")
            return DetalleCarrito.objects.filter(carrito=carrito)
        except Cliente.DoesNotExist:
            return DetalleCarrito.objects.none() # No hay cliente, no hay detalles de carrito
        except Carrito.DoesNotExist:
            return DetalleCarrito.objects.none() # No hay carrito, no hay detalles de carrito

    def create(self, request, *args, **kwargs):
        user = self.request.user
        try:
            cliente = user.cliente_profile
            carrito = cliente.carritos.first()
            if not carrito:
                carrito = Carrito.objects.create(cliente=cliente) # Crear carrito si no existe
        except Cliente.DoesNotExist:
            return Response({'error': 'Perfil de cliente no encontrado para este usuario.'}, status=status.HTTP_404_NOT_FOUND)
        
        producto_sku = request.data.get('producto_sku')
        cantidad = request.data.get('cantidad')

        if not producto_sku or not cantidad:
            return Response({'error': 'Producto SKU y cantidad son requeridos.'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            producto = Producto.objects.get(SKU=producto_sku)
        except Producto.DoesNotExist:
            return Response({'error': 'Producto no encontrado.'}, status=status.HTTP_404_NOT_FOUND)

        # ----------------
        # Validaciones mayoristas:
        # - Si el usuario es Empresa ACTIVO:
        #   - bloquear productos no disponibles para mayorista
        #   - bloquear cantidades menores al bulto mínimo (cantidad es total acumulado del SKU en carrito)
        # ----------------
        try:
            is_mayorista_activo = bool(
                cliente.tipo_cliente == Cliente.EMPRESA
                and cliente.estado_cuenta == Cliente.ACTIVO
            )
        except Exception:
            is_mayorista_activo = False

        if is_mayorista_activo:
            if not getattr(producto, 'disponible_mayorista', True):
                return Response(
                    {'error': 'Producto no disponible para mayorista.'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            requerido = getattr(producto, 'bulto_minimo_mayorista', 1) or 1
            try:
                requerido = int(requerido)
            except Exception:
                requerido = 1

            try:
                cantidad_int = int(cantidad)
            except Exception:
                return Response(
                    {'error': 'La cantidad debe ser un número entero.'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            if cantidad_int < requerido:
                return Response(
                    {'error': f'Bulto mínimo no alcanzado. Requerido: {requerido}, enviado: {cantidad_int}'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            # normalizamos cantidad para el resto del flujo (stock/guardar)
            cantidad = cantidad_int
        
        # Validación de stock
        try:
            inventario = producto.inventario
        except Inventario.DoesNotExist:
            return Response({'error': 'Producto sin registro de inventario.'}, status=status.HTTP_404_NOT_FOUND)

        try:
            detalle_carrito_existente = DetalleCarrito.objects.get(
                carrito=carrito,
                producto=producto
            )
            cantidad_previa = detalle_carrito_existente.cantidad
            
            cambio_stock = cantidad - cantidad_previa
            if inventario.stock - cambio_stock < 0:
                return Response(
                    {'error': f'No hay suficiente stock para el producto {producto.nombre}. Stock disponible: {inventario.stock + cantidad_previa} (ya tienes {cantidad_previa} en el carrito)'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            detalle_carrito_existente.cantidad = cantidad
            detalle_carrito_existente.save()
            inventario.stock -= cambio_stock
            inventario.save()
            detalle_carrito = detalle_carrito_existente
            created = False
        except DetalleCarrito.DoesNotExist:
            if inventario.stock - cantidad < 0:
                 return Response(
                    {'error': f'No hay suficiente stock para el producto {producto.nombre}. Stock disponible: {inventario.stock}'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            detalle_carrito = DetalleCarrito.objects.create(
                carrito=carrito,
                producto=producto,
                cantidad=cantidad
            )
            inventario.stock -= cantidad
            inventario.save()
            created = True

        serializer = self.get_serializer(detalle_carrito)
        return Response(serializer.data, status=status.HTTP_200_OK if not created else status.HTTP_201_CREATED)

    def destroy(self, request, *args, **kwargs):
        user = self.request.user
        try:
            cliente = user.cliente_profile
            carrito = cliente.carritos.first()
            if not carrito:
                raise Carrito.DoesNotExist("No active cart found for this user.")
        except Cliente.DoesNotExist:
            return Response({'error': 'Perfil de cliente no encontrado para este usuario.'}, status=status.HTTP_404_NOT_FOUND)
        except Carrito.DoesNotExist:
            return Response({'error': 'Carrito no encontrado para este usuario.'}, status=status.HTTP_404_NOT_FOUND)
        
        producto_sku = self.kwargs['producto__SKU']

        try:
            detalle_carrito = DetalleCarrito.objects.get(carrito=carrito, producto__SKU=producto_sku)
        except DetalleCarrito.DoesNotExist:
            return Response({'error': 'Detalle de carrito no encontrado con ese producto en tu carrito.'}, status=status.HTTP_404_NOT_FOUND)
        
        producto = detalle_carrito.producto
        try:
            inventario = producto.inventario
            inventario.stock += detalle_carrito.cantidad
            inventario.save()
        except Inventario.DoesNotExist:
            print(f"Advertencia: Producto {producto.SKU} sin registro de inventario al eliminar detalle.")

        self.perform_destroy(detalle_carrito)
        return Response(status=status.HTTP_204_NO_CONTENT)


#-------------------
# ViewSet para los pedidos del usuario autenticado (API REST)
# Devuelve solo pedidos pertenecientes al usuario y permite generar links firmados para PDF
#-------------------
class MisPedidosViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet
):
    serializer_class = PedidoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        try:
            cliente = user.cliente_profile
        except Cliente.DoesNotExist:
            return Pedido.objects.none()

        # Solo pedidos del usuario autenticado
        qs = Pedido.objects.filter(cliente=cliente)

        # Filtro opcional por estado de entrega:
        # - entrega=en_proceso  -> Pendiente/Preparando/Despachado (todo menos Entregado)
        # - entrega=entregados  -> solo Entregado
        entrega = (self.request.query_params.get('entrega') or '').strip().lower()
        if entrega == 'en_proceso':
            # Solo pedidos que YA tienen envío creado (excluye transferencias en revisión)
            qs = qs.filter(transportista__isnull=False).exclude(transportista__estado_entrega='Entregado')
        elif entrega == 'entregados':
            qs = qs.filter(transportista__estado_entrega='Entregado')

        return qs.order_by('-fecha_pedido', '-id')

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

    @action(detail=True, methods=['get'], url_path='comprobante/link')
    def comprobante_link(self, request, pk=None):
        """
        Retorna un URL firmado (temporal) para ver el PDF en iframe y otro para descargar.
        Si el pedido no pertenece al usuario, se retorna 404 (por el queryset filtrado).
        """
        pedido = self.get_object()  # 404 si no existe o no pertenece al usuario

        # Token de firma con expiración (debe coincidir con la validación en generar_factura_pdf)
        PDF_TOKEN_MAX_AGE_SECONDS = 10 * 60
        signer = signing.TimestampSigner(salt='comprobante_pdf')
        token_firma = signer.sign(str(pedido.id))

        base_path = reverse('generar_factura_pdf', kwargs={'pedido_id': pedido.id})
        token_qs = f"token={quote(token_firma)}"

        pdf_url = request.build_absolute_uri(f"{base_path}?{token_qs}")
        pdf_url_download = request.build_absolute_uri(f"{base_path}?{token_qs}&download=1")

        return Response(
            {
                'pedido_id': pedido.id,
                'pdf_url': pdf_url,
                'pdf_url_download': pdf_url_download,
                'expires_in_seconds': PDF_TOKEN_MAX_AGE_SECONDS,
            },
            status=status.HTTP_200_OK
        )


#-------------------
# ViewSet para el perfil del usuario autenticado (API REST)
# Devuelve los datos del modelo Cliente asociado al token
#-------------------
class MiPerfilViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = ClientePerfilSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        user = self.request.user
        try:
            return user.cliente_profile
        except Cliente.DoesNotExist:
            raise Http404("Perfil de cliente no encontrado para este usuario.")

    def list(self, request, *args, **kwargs):
        """
        Retorna el perfil (Cliente) del usuario autenticado.
        Nota: usamos endpoint de colección /api/mi-perfil/ (sin pk) por conveniencia de frontend.
        """
        cliente = self.get_object()
        serializer = self.get_serializer(cliente)
        return Response(serializer.data, status=status.HTTP_200_OK)


#-------------------
# Endpoint para el perfil del usuario autenticado (GET + PATCH) sin pk
# Nota: usamos una vista explícita porque el DefaultRouter no soporta PATCH en la ruta de colección.
#-------------------
class MiPerfilAPIView(generics.RetrieveUpdateAPIView):
    serializer_class = ClientePerfilSerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ['get', 'patch', 'put', 'options', 'head']

    def get_object(self):
        user = self.request.user
        try:
            return user.cliente_profile
        except Cliente.DoesNotExist:
            raise Http404("Perfil de cliente no encontrado para este usuario.")

#-------------------
# ViewSet para los favoritos del usuario autenticado (API REST)
#-------------------
class FavoritosClienteViewSet(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    serializer_class = FavoritosClienteSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'producto__SKU' # Para DELETE por SKU

    def get_queryset(self):
        user = self.request.user
        if not user.is_authenticated:
            return FavoritosCliente.objects.none()
        try:
            cliente = user.cliente_profile
            queryset = FavoritosCliente.objects.filter(cliente=cliente)

            subcategoria_nombre = self.request.query_params.get('subcategoria')
            if subcategoria_nombre:
                queryset = queryset.filter(producto__subcategoria__nombre_subcategoria__iexact=subcategoria_nombre)

            return queryset
        except Cliente.DoesNotExist:
            return FavoritosCliente.objects.none()

    def create(self, request, *args, **kwargs):
        user = self.request.user
        try:
            cliente = user.cliente_profile
        except Cliente.DoesNotExist:
            return Response({"error": "Perfil de cliente no encontrado para este usuario."}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # El serializador ahora maneja la resolución del producto a través de SlugRelatedField
        producto_instance = serializer.validated_data['producto'] # Obtener la instancia de Producto del validated_data
        
        # Verificar si el favorito ya existe
        if FavoritosCliente.objects.filter(cliente=cliente, producto=producto_instance).exists():
            return Response({'message': 'Este producto ya está en tus favoritos.'}, status=status.HTTP_200_OK)
        
        # Si no, guardarlo
        serializer.save(cliente=cliente) # Pasar la instancia del cliente
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object() # Esto intentará recuperar el objeto basado en lookup_field
        except Http404:
            return Response({'error': 'Este producto no está en tus favoritos.'}, status=status.HTTP_404_NOT_FOUND)

        user = self.request.user
        try:
            cliente = user.cliente_profile
        except Cliente.DoesNotExist:
            return Response({"error": "Perfil de cliente no encontrado para este usuario."}, status=status.HTTP_404_NOT_FOUND)
        
        # Asegurarse de que el favorito a eliminar pertenece al usuario autenticado
        if instance.cliente != cliente:
            return Response({"error": "No tienes permiso para eliminar este favorito."}, status=status.HTTP_403_FORBIDDEN)
            
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['get'], url_path='is_favorite')
    def is_favorite(self, request, producto__SKU=None):
        """ Verifica si un producto específico es favorito para el usuario autenticado. """
        user = request.user
        if not user.is_authenticated:
            return Response({'is_favorite': False, 'error': 'Autenticación requerida.'}, status=status.HTTP_401_UNAUTHORIZED)
        
        try:
            cliente = user.cliente_profile
        except Cliente.DoesNotExist:
            return Response({'is_favorite': False, 'error': 'Perfil de cliente no encontrado para este usuario.'}, status=status.HTTP_404_NOT_FOUND)
        
        # El pk en este caso será el SKU del producto
        producto_sku = producto__SKU
        if not producto_sku:
            return Response({'is_favorite': False, 'error': 'SKU del producto es requerido.'}, status=status.HTTP_400_BAD_REQUEST)
        
        is_fav = FavoritosCliente.objects.filter(cliente=cliente, producto__SKU=producto_sku).exists()
        return Response({'is_favorite': is_fav}, status=status.HTTP_200_OK)


class SubcategoriaViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Subcategoria.objects.all()
    serializer_class = SubcategoriaSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        limite = self.request.query_params.get('limite')
        if limite:
            try:
                limite = int(limite)
                queryset = queryset[:limite]
            except ValueError:
                pass
        return queryset

