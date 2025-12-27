from rest_framework import serializers
from .models import Producto, Precio, Carrito, DetalleCarrito, Cliente # Importa tus modelos

#------------------
# Serializador para el modelo Producto
#------------------
class ProductoSerializer(serializers.ModelSerializer):
    categoria = serializers.StringRelatedField(read_only=True)
    subcategoria = serializers.StringRelatedField(read_only=True)
    variante = serializers.StringRelatedField(read_only=True)

    pvp = serializers.DecimalField(max_digits=10, decimal_places=2, source='precios.pvp', read_only=True)
    pvm = serializers.DecimalField(max_digits=10, decimal_places=2, source='precios.pvm', read_only=True)

    class Meta:
        model = Producto
        fields = [
            'SKU', 'codigo_barras', 'nombre', 'descripcion',
            'marca', 'categoria', 'subcategoria', 'variante',
            'caracteristica1', 'caracteristica2', 'caracteristica3', 'caracteristica4', 'caracteristica5',
            'imagen_url', 'imagen_url2', 'imagen_url3', 'imagen_url4', 'pvp', 'pvm'
        ]


class DetalleCarritoSerializer(serializers.ModelSerializer):
    # Campo para recibir el SKU del producto al añadir/actualizar en el carrito
    producto_sku = serializers.CharField(write_only=True, required=True)
    # Campo para representar el producto completo al leer el detalle del carrito
    producto = ProductoSerializer(read_only=True)

    class Meta:
        model = DetalleCarrito
        fields = ['id', 'producto_sku', 'producto', 'cantidad', 'precio_unitario', 'subtotal_detalle_carrito', 'descuento_detalle_carrito', 'iva_detalle_carrito', 'total_detalle_carrito', 'carrito']
        read_only_fields = ['precio_unitario', 'subtotal_detalle_carrito', 'total_detalle_carrito', 'carrito']

class CarritoSerializer(serializers.ModelSerializer):
    detalles_carrito = DetalleCarritoSerializer(many=True, read_only=True) # Anidar detalles del carrito
    cliente_nombre = serializers.CharField(source='cliente.nombre', read_only=True)
    cliente_tipo = serializers.CharField(source='cliente.tipo_cliente', read_only=True)

    class Meta:
        model = Carrito
        fields = ['id', 'cliente', 'cliente_nombre', 'cliente_tipo', 'fecha_creacion', 'fecha_actualizacion', 'estado_dinamico', 'subtotal_carrito', 'descuento_carrito', 'iva_carrito', 'total_carrito', 'detalles_carrito']
        read_only_fields = ['cliente', 'fecha_creacion', 'fecha_actualizacion', 'estado_dinamico', 'subtotal_carrito', 'descuento_carrito', 'iva_carrito', 'total_carrito']
