from rest_framework import serializers
from .models import Producto, Precio # Importa tus modelos

#------------------
# Serializador para el modelo Producto
#------------------
class ProductoSerializer(serializers.ModelSerializer):
    # Para incluir campos relacionados (precio), podemos usar SerializerMethodField o anidarlos
    # Aquí, queremos el precio de venta al público (pvp) y al por mayor (pvm) directamente.
    # Como Precio es OneToOneField en Producto, podemos accederlo directamente.
    # Si Precio fuera ManyToOne, necesitaríamos un campo anidado o un SerializerMethodField.

    # Añadir un campo para el precio del producto
    pvp = serializers.DecimalField(max_digits=10, decimal_places=2, source='precios.pvp', read_only=True)
    pvm = serializers.DecimalField(max_digits=10, decimal_places=2, source='precios.pvm', read_only=True)

    class Meta:
        model = Producto
        fields = [
            'SKU', 'codigo_barras', 'nombre', 'descripcion',
            'marca', 'categoria', 'subcategoria', 'variante',
            'imagen_url', 'pvp', 'pvm' # Incluimos los campos de precio aquí
        ]
