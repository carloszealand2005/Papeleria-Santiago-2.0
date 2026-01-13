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

    class Meta:
        model = Producto
        fields = [
            'SKU', 'codigo_barras', 'nombre', 'descripcion',
            'marca', 'categoria', 'subcategoria', 'variante',
            'caracteristica1', 'caracteristica2', 'caracteristica3', 'caracteristica4', 'caracteristica5',
            'imagen_url', 'imagen_url2', 'imagen_url3', 'imagen_url4', 'pvp', 'pvm',
            'descuento_publico', 'descuento_mayorista', 'precio_con_descuento_publico', 'precio_con_descuento_mayorista', 'iva', 'precio_con_iva_publico', 'precio_con_iva_mayorista' # Nuevos campos
        ]


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

    class Meta:
        model = Pedido
        fields = ['id', 'fecha_pedido', 'estado_pedido', 'subtotal', 'descuento', 'iva', 'total']


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

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Este correo electrónico ya está registrado.")
        return value


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