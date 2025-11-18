from django.contrib import admin
from .models import (
    Cliente, Producto, Pedido, Precio,
    Inventario, DetallePedido, Transportista
)

# Registra tus modelos aquí.
admin.site.register(Cliente)
admin.site.register(Producto)
admin.site.register(Pedido)
admin.site.register(Precio)
admin.site.register(Inventario)
admin.site.register(DetallePedido)
admin.site.register(Transportista)
