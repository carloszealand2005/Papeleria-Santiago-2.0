from rest_framework import serializers
from .models import FavoritosCliente, Producto, Precio, Carrito, DetalleCarrito, Cliente, Subcategoria, Pedido # Importa tus modelos
from django.contrib.auth.models import User

#------------------
# Serializador para el modelo Producto
#------------------
class ProductoSerializer(serializers.ModelSerializer):
    categoria = serializers.StringRelatedField(read_only=True)
    subcategoria = serializers.StringRelatedField(read_only=True)
    variante = serializers.StringRelatedField(read_only=True)

    pvp = serializers.DecimalField(max_digits=10, decimal_places=2, source='precios.pvp', read_only=True)
    pvm = serializers.DecimalField(max_digits=10, decimal_places=2, source='precios.pvm', read_only=True)
    descuento_publico = serializers.DecimalField(max_digits=5, decimal_places=2, source='precios.descuento_publico', read_only=True)
    descuento_mayorista = serializers.DecimalField(max_digits=5, decimal_places=2, source='precios.descuento_mayorista', read_only=True)
    precio_con_descuento_publico = serializers.DecimalField(max_digits=10, decimal_places=2, source='precios.precio_con_descuento_publico', read_only=True)
    precio_con_descuento_mayorista = serializers.DecimalField(max_digits=10, decimal_places=2, source='precios.precio_con_descuento_mayorista', read_only=True)
    precio_con_iva_publico = serializers.DecimalField(max_digits=10, decimal_places=2, source='precios.precio_con_iva_publico', read_only=True)
    precio_con_iva_mayorista = serializers.DecimalField(max_digits=10, decimal_places=2, source='precios.precio_con_iva_mayorista', read_only=True)
    iva = serializers.DecimalField(max_digits=4, decimal_places=2, source='precios.iva', read_only=True) # Incluir el porcentaje de IVA

    # Solo se expone a mayoristas (Empresa ACTIVO) - ver to_representation
    bulto_minimo_mayorista = serializers.IntegerField(read_only=True)

    # ------------------
    # Campos "activos" (fuente de verdad para el frontend):
    # Dependen del tipo de usuario autenticado:
    # - Público / Persona: usa PVP + descuento_publico
    # - Empresa ACTIVO: usa PVM + descuento_mayorista
    # ------------------
    tipo_precio_activo = serializers.SerializerMethodField()
    precio_base_activo = serializers.SerializerMethodField()
    descuento_activo = serializers.SerializerMethodField()
    precio_con_descuento_activo = serializers.SerializerMethodField()
    precio_con_iva_activo = serializers.SerializerMethodField()

    class Meta:
        model = Producto
        fields = [
            'SKU', 'codigo_barras', 'nombre', 'descripcion',
            'marca', 'categoria', 'subcategoria', 'variante',
            'caracteristica1', 'caracteristica2', 'caracteristica3', 'caracteristica4', 'caracteristica5',
            'imagen_url', 'imagen_url2', 'imagen_url3', 'imagen_url4', 'pvp', 'pvm',
            'descuento_publico', 'descuento_mayorista', 'precio_con_descuento_publico', 'precio_con_descuento_mayorista', 'iva', 'precio_con_iva_publico', 'precio_con_iva_mayorista',
            'bulto_minimo_mayorista', # Mayoristas
            'tipo_precio_activo',
            'precio_base_activo',
            'descuento_activo',
            'precio_con_descuento_activo',
            'precio_con_iva_activo',
        ]

    def _is_mayorista_activo(self):
        request = self.context.get('request')
        if not request:
            return False
        user = getattr(request, 'user', None)
        if not user or not getattr(user, 'is_authenticated', False):
            return False
        cliente = getattr(user, 'cliente_profile', None)
        if not cliente:
            return False
        return cliente.tipo_cliente == Cliente.EMPRESA and cliente.estado_cuenta == Cliente.ACTIVO

    def get_tipo_precio_activo(self, obj):
        return "MAYORISTA" if self._is_mayorista_activo() else "PUBLICO"

    def get_precio_base_activo(self, obj):
        precios = getattr(obj, 'precios', None)
        if not precios:
            return None
        return precios.pvm if self._is_mayorista_activo() else precios.pvp

    def get_descuento_activo(self, obj):
        precios = getattr(obj, 'precios', None)
        if not precios:
            return None
        return precios.descuento_mayorista if self._is_mayorista_activo() else precios.descuento_publico

    def get_precio_con_descuento_activo(self, obj):
        precios = getattr(obj, 'precios', None)
        if not precios:
            return None
        return precios.precio_con_descuento_mayorista if self._is_mayorista_activo() else precios.precio_con_descuento_publico

    def get_precio_con_iva_activo(self, obj):
        precios = getattr(obj, 'precios', None)
        if not precios:
            return None
        return precios.precio_con_iva_mayorista if self._is_mayorista_activo() else precios.precio_con_iva_publico

    def to_representation(self, instance):
        data = super().to_representation(instance)
        # Si NO es mayorista activo, ocultamos el bulto mínimo
        if not self._is_mayorista_activo():
            data.pop('bulto_minimo_mayorista', None)
        return data


class DetalleCarritoSerializer(serializers.ModelSerializer):
    # Campo para recibir el SKU del producto al añadir/actualizar en el carrito
    producto_sku = serializers.CharField(write_only=True, required=True)
    # Campo para representar el producto completo al leer el detalle del carrito
    producto = ProductoSerializer(read_only=True)

    class Meta:
        model = DetalleCarrito
        fields = ['id', 'producto_sku', 'producto', 'cantidad', 'precio_unitario', 'subtotal_antes_descuento', 'descuento_detalle_carrito', 'subtotal_detalle_carrito', 'iva_detalle_carrito', 'total_detalle_carrito', 'carrito']
        read_only_fields = ['precio_unitario', 'subtotal_antes_descuento', 'descuento_detalle_carrito', 'subtotal_detalle_carrito',  'iva_detalle_carrito', 'total_detalle_carrito', 'carrito']

class CarritoSerializer(serializers.ModelSerializer):
    detalles_carrito = DetalleCarritoSerializer(many=True, read_only=True) # Anidar detalles del carrito
    cliente_nombre = serializers.CharField(source='cliente.nombre', read_only=True)
    cliente_tipo = serializers.CharField(source='cliente.tipo_cliente', read_only=True)

    class Meta:
        model = Carrito
        fields = ['id', 'cliente', 'cliente_nombre', 'cliente_tipo', 'fecha_creacion', 'fecha_actualizacion', 'estado_dinamico', 'subtotal_carrito', 'descuento_carrito', 'iva_carrito', 'total_carrito', 'detalles_carrito']
        read_only_fields = ['cliente', 'fecha_creacion', 'fecha_actualizacion', 'estado_dinamico', 'subtotal_carrito', 'descuento_carrito', 'iva_carrito', 'total_carrito']

class FavoritosClienteSerializer(serializers.ModelSerializer):
    producto_sku = serializers.SlugRelatedField(
        source='producto',
        slug_field='SKU',
        queryset=Producto.objects.all(),
        write_only=True,
        required=True
    )
    producto_detail = ProductoSerializer(source='producto', read_only=True)

    class Meta:
        model = FavoritosCliente
        fields = ['id', 'producto_sku', 'producto_detail', 'cliente', 'fecha_creacion']
        read_only_fields = ['cliente', 'fecha_creacion', 'producto_detail']

class SubcategoriaSerializer(serializers.ModelSerializer):
    categoria = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Subcategoria
        fields = ['id', 'nombre_subcategoria', 'descripcion_categoria', 'foto_categoria_url', 'categoria']


#------------------
# Serializador para el modelo Pedido (para listar pedidos del usuario autenticado)
#------------------
class PedidoSerializer(serializers.ModelSerializer):
    subtotal = serializers.DecimalField(max_digits=10, decimal_places=2, source='subtotal_general_comprobante', read_only=True)
    descuento = serializers.DecimalField(max_digits=10, decimal_places=2, source='descuento_general_comprobante', read_only=True)
    iva = serializers.DecimalField(max_digits=10, decimal_places=2, source='iva_general_comprobante', read_only=True)
    total = serializers.DecimalField(max_digits=10, decimal_places=2, source='total_general_comprobante', read_only=True)
    # Entrega (Transportista) - puede no existir en casos antiguos; por eso usamos getters seguros.
    estado_entrega = serializers.SerializerMethodField()
    transportista_empresa = serializers.SerializerMethodField()
    transportista_numero_guia = serializers.SerializerMethodField()
    transportista_fecha_actualizacion = serializers.SerializerMethodField()
    # Snapshot de envío
    ciudad_envio = serializers.CharField(read_only=True)
    direccion_envio = serializers.CharField(read_only=True)
    numero_casa_envio = serializers.CharField(read_only=True)
    codigo_postal_envio = serializers.CharField(read_only=True)
    cedula_envio = serializers.CharField(read_only=True)
    telefono_envio = serializers.CharField(read_only=True)
    referencia_envio = serializers.CharField(read_only=True)
    metodo_pago = serializers.CharField(read_only=True)
    costo_envio = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    comprobante_transferencia_url = serializers.SerializerMethodField()
    motivo_cancelacion = serializers.CharField(read_only=True, allow_blank=True, allow_null=True)

    class Meta:
        model = Pedido
        fields = [
            'id', 'fecha_pedido', 'estado_pedido',
            'subtotal', 'descuento', 'iva', 'total',
            'estado_entrega', 'transportista_empresa', 'transportista_numero_guia', 'transportista_fecha_actualizacion',
            'ciudad_envio', 'direccion_envio', 'numero_casa_envio', 'codigo_postal_envio',
            'cedula_envio', 'telefono_envio', 'referencia_envio', 'metodo_pago',
            'costo_envio',
            'comprobante_transferencia_url',
            'motivo_cancelacion',
        ]

    def get_estado_entrega(self, obj):
        try:
            return obj.transportista.estado_entrega
        except Exception:
            return None

    def get_transportista_empresa(self, obj):
        try:
            return obj.transportista.empresa
        except Exception:
            return None

    def get_transportista_numero_guia(self, obj):
        try:
            return obj.transportista.numero_guia
        except Exception:
            return None

    def get_transportista_fecha_actualizacion(self, obj):
        try:
            return obj.transportista.fecha_actualizacion
        except Exception:
            return None

    def get_comprobante_transferencia_url(self, obj):
        """
        Para pagos por transferencia: exponer el URL del archivo para que el frontend
        pueda abrirlo (nueva pestaña / modal).
        """
        try:
            field = getattr(obj, 'comprobante_transferencia', None)
            if not field:
                return None
            request = self.context.get('request')
            url = field.url
            return request.build_absolute_uri(url) if request else url
        except Exception:
            return None


#------------------
# Serializador para el perfil del usuario (modelo Cliente)
# Nota: no expone el modelo User (dato interno)
#------------------
class ClientePerfilSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = [
            'id',
            'nombre',
            'cedula',
            'telefono',
            'email',
            'ciudad',
            'direccion',
            'tipo_cliente',
        ]
        read_only_fields = ['id', 'nombre', 'tipo_cliente']


# ------------------
# OTP - Registro en 2 pasos
# ------------------
class InitRegisterSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    first_name = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    password = serializers.CharField(required=True, write_only=True)
    celular = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    ciudad = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    tipo_cliente = serializers.ChoiceField(
        choices=Cliente.TIPOS_CLIENTES_CHOICES,
        required=False,
        default=Cliente.PERSONA,
    )
    url_validacion = serializers.URLField(required=False, allow_null=True, allow_blank=True)

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Este correo electrónico ya está registrado.")
        return value

    def validate(self, attrs):
        # Si se registra como Empresa, para MVP pedimos el link de validación.
        tipo_cliente = attrs.get('tipo_cliente') or Cliente.PERSONA
        url_validacion = (attrs.get('url_validacion') or '').strip()
        if tipo_cliente == Cliente.EMPRESA and not url_validacion:
            raise serializers.ValidationError({'url_validacion': 'Este campo es requerido para registro de empresa.'})
        return attrs


class VerifyOtpSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    otp = serializers.CharField(required=True, min_length=6, max_length=6)

    def validate_otp(self, value):
        if not str(value).isdigit():
            raise serializers.ValidationError("El código debe ser numérico.")
        return value


class ResendOtpSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)


# ------------------
# OTP - Recuperación de contraseña (2 pasos)
# ------------------
class SolicitarRecuperacionSerializer(serializers.Serializer):
    # Importante: NO validar existencia del correo aquí (para no filtrar).
    email = serializers.EmailField(required=True)


class ConfirmarRecuperacionSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    otp_code = serializers.CharField(required=True, min_length=6, max_length=6)
    new_password = serializers.CharField(required=True, write_only=True)
    confirm_password = serializers.CharField(required=True, write_only=True)

    def validate_otp_code(self, value):
        if not str(value).isdigit():
            raise serializers.ValidationError("El código debe ser numérico.")
        return value