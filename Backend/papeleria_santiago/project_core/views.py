from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404
from django.template.loader import get_template
from io import BytesIO
from xhtml2pdf import pisa
from django.core import signing
from django.urls import reverse
from urllib.parse import quote
from django.views.decorators.clickjacking import xframe_options_exempt
from django.db.models import Q, F
from .models import Comprobante, Pedido, Producto, Carrito, DetalleCarrito, Cliente, DetallePedido, Inventario, Subcategoria # Importamos DetallePedido, Inventario y Subcategoria
from rest_framework import viewsets, filters, status, mixins, permissions, serializers # Importar filters, status, mixins, permissions y serializers
from rest_framework import generics
from rest_framework.decorators import action # Importar action
from django_filters.rest_framework import DjangoFilterBackend # Importar DjangoFilterBackend
from .serializers import ProductoSerializer, CarritoSerializer, DetalleCarritoSerializer, FavoritosClienteSerializer, SubcategoriaSerializer, PedidoSerializer, ClientePerfilSerializer # Importar el serializador
from rest_framework.response import Response # Importar Response
from .models import FavoritosCliente # Importar el modelo FavoritosCliente

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


class ProductoViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer
    filter_backends = [DjangoFilterBackend] # Añadir backends de filtro y búsqueda
    filterset_fields = ['categoria', 'marca', 'SKU'] # Filtrar por categoría, marca y SKU
    search_fields = ['nombre', 'marca'] # Campos para búsqueda de texto
    ordering_fields = ['SKU', 'nombre', 'pvp', 'pvm'] # Campos para ordenar resultados

    # Para filtrar por rango de precio, podemos sobrescribir el método get_queryset
    def get_queryset(self):
        queryset = super().get_queryset()

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

        if precio_min:
            # Asumimos que `precios` es el related_name del OneToOneField del Precio
            # que apunta a Producto. Para filtrar por precio en el modelo Precio,
            # necesitamos acceder a `precios__pvp` o `precios__pvm`.
            # Vamos a usar `precios__pvp` para este ejemplo.
            queryset = queryset.filter(precios__pvp__gte=precio_min)
        if precio_max:
            queryset = queryset.filter(precios__pvp__lte=precio_max)
            
        # Filtrar por nombre de subcategoría (case-insensitive)
        subcategoria_nombre = self.request.query_params.get('subcategoria')
        if subcategoria_nombre:
            queryset = queryset.filter(subcategoria__nombre_subcategoria__iexact=subcategoria_nombre)

        # Filtrar por descuento mínimo y por descuento máximo.
        descuento_min = self.request.query_params.get('descuento_min')
        descuento_max = self.request.query_params.get('descuento_max') 

        if descuento_min and descuento_max:
            try:
                descuento_min = float(descuento_min)
                descuento_max = float(descuento_max)
                queryset = queryset.filter(
                    (Q(precios__descuento_publico__gte=descuento_min) & Q(precios__descuento_publico__lte=descuento_max)) |
                    (Q(precios__descuento_mayorista__gte=descuento_min) & Q(precios__descuento_mayorista__lte=descuento_max))
                )
            except ValueError:
                pass
        elif descuento_min:
            try:
                descuento_min = float(descuento_min)
                queryset = queryset.filter(
                    Q(precios__descuento_publico__gte=descuento_min) |
                    Q(precios__descuento_mayorista__gte=descuento_min)
                )
            except ValueError:
                pass # Ignorar si el valor no es un número válido
        elif descuento_max:
            try:
                descuento_max = float(descuento_max)
                queryset = queryset.filter(
                    Q(precios__descuento_publico__lte=descuento_max) |
                    Q(precios__descuento_mayorista__lte=descuento_max)
                )
            except ValueError:
                pass

        # Ordering “custom” para el frontend (aliases):
        # - ordering=total_vendidos  -> más vendidos primero
        # - ordering=descuento       -> mayor descuento_publico primero
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
                # default: DESC (mayor descuento_publico primero)
                queryset = queryset.order_by('precios__descuento_publico' if is_desc else '-precios__descuento_publico')
            elif key == 'alphabet':
                # default: ASC (A-Z)
                queryset = queryset.order_by('-nombre' if is_desc else 'nombre')

            # Campos directos (compatibilidad con DRF OrderingFilter anterior)
            elif key in ('SKU', 'nombre', 'pvp', 'pvm'):
                queryset = queryset.order_by(f"-{key}" if is_desc else key)

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

        # Aplicar filtro por subcategoría si se proporciona
        subcategoria_nombre = self.request.query_params.get('subcategoria')
        if subcategoria_nombre:
            productos_destacados = productos_destacados.filter(subcategoria__nombre_subcategoria__iexact=subcategoria_nombre)

        productos_destacados = productos_destacados.order_by('-total_vendidos')[:limite]
        serializer = self.get_serializer(productos_destacados, many=True)
        return Response(serializer.data)


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
            # --- 3. Crear Pedido (estado inicial 'Pagado') ---
            pedido = Pedido.objects.create(
                cliente=carrito.cliente,
                estado_pedido='Pagado',
                # Otros campos del pedido se llenarán automáticamente o por señales si es necesario
            )

            # --- 4. Crear DetallePedido a partir de DetalleCarrito ---
            for detalle_carrito in carrito.detalles_carrito.all():
                DetallePedido.objects.create(
                    pedido=pedido,
                    producto=detalle_carrito.producto,
                    cantidad=detalle_carrito.cantidad,
                    precio_unitario=detalle_carrito.precio_unitario,
                    subtotal_detalle_pedido=detalle_carrito.subtotal_detalle_carrito,
                    iva_detalle_pedido=detalle_carrito.iva_detalle_carrito, # Asegurarse de que este campo tenga valor en DetalleCarrito
                    descuento_detalle_pedido=detalle_carrito.descuento_detalle_carrito,
                    total_detalle_pedido=detalle_carrito.total_detalle_carrito,
                )

            # --- 5. Crear Comprobante después de que todos los DetallePedido estén creados ---
            # Ahora las propiedades del Pedido (subtotal, descuento, iva, total) deberían ser correctas
            Comprobante.objects.create(
                pedido=pedido,
                numero_factura=f"FAC-{pedido.id}-{pedido.fecha_pedido.strftime('%Y%m%d')}",
                cedula_cliente=pedido.cliente.cedula if pedido.cliente.cedula else 'NO ESPECIFICADO',
                direccion_cliente=pedido.cliente.direccion,
                email_cliente=pedido.cliente.email,
                subtotal=pedido.subtotal_general_comprobante,
                descuento=pedido.descuento_general_comprobante,
                iva=pedido.iva_general_comprobante,
                total=pedido.total_general_comprobante,
                metodo_pago='Tarjeta de crédito', # Se mantiene el valor por defecto
                estado_fiscal='Emitido',
                # url_factura en blanco. TODO(PENDIENTE: GUARDAR URL DE LA FACTURA EN PRODUCCIÓN)
            )
            
            # --- 6. Borrar DetalleCarrito del carrito original ---
            # Esto también hará que el carrito.estado_dinamico pase a 'Inactivo'
            carrito.detalles_carrito.all().delete()
            carrito.save() # Guarda el carrito para actualizar la fecha_actualizacion

            # TODO: DEVOLVER UNA RESPUESTA DETALLADA DEL PEDIDO CREADO EXITOSAMENTE
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
            # --- 3. Crear Pedido (estado inicial 'Pagado') ---
            pedido = Pedido.objects.create(
                cliente=carrito.cliente,
                estado_pedido='Pagado',
            )

            # --- 4. Crear DetallePedido a partir de DetalleCarrito ---
            for detalle_carrito in carrito.detalles_carrito.all():
                DetallePedido.objects.create(
                    pedido=pedido,
                    producto=detalle_carrito.producto,
                    cantidad=detalle_carrito.cantidad,
                    precio_unitario=detalle_carrito.precio_unitario,
                    subtotal_detalle_pedido=detalle_carrito.subtotal_detalle_carrito,
                    iva_detalle_pedido=detalle_carrito.iva_detalle_carrito,
                    descuento_detalle_pedido=detalle_carrito.descuento_detalle_carrito,
                    total_detalle_pedido=detalle_carrito.total_detalle_carrito,
                )

            # --- 5. Crear Comprobante después de que todos los DetallePedido estén creados ---
            Comprobante.objects.create(
                pedido=pedido,
                numero_factura=f"FAC-{pedido.id}-{pedido.fecha_pedido.strftime('%Y%m%d')}",
                cedula_cliente=pedido.cliente.cedula if pedido.cliente.cedula else 'NO ESPECIFICADO',
                direccion_cliente=pedido.cliente.direccion,
                email_cliente=pedido.cliente.email,
                subtotal=pedido.subtotal_general_comprobante,
                descuento=pedido.descuento_general_comprobante,
                iva=pedido.iva_general_comprobante,
                total=pedido.total_general_comprobante,
                metodo_pago='Tarjeta de crédito',
                estado_fiscal='Emitido',
            )

            # --- 6. Borrar DetalleCarrito del carrito original ---
            carrito.detalles_carrito.all().delete()
            carrito.save() # Guarda el carrito para actualizar la fecha_actualizacion

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
        return Pedido.objects.filter(cliente=cliente).order_by('-fecha_pedido', '-id')

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

