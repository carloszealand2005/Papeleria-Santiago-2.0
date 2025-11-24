from django.contrib import admin
from .models import (
    Cliente, Producto, Pedido, Precio,
    Inventario, DetallePedido, Transportista
)

# Registra tus modelos aquí.
admin.site.register(Cliente)
admin.site.register(Producto)
admin.site.register(Precio)
admin.site.register(Inventario)
admin.site.register(DetallePedido)
admin.site.register(Transportista)


# Personalizables: 
# Mostrar el coste total de pedidos en tiempo real:
@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'cliente', 'fecha_pedido', 'estado_pedido',
        'monto_total_display' # Aquí incluimos la propiedad calculada
    )
   
    # Calcular el monto total basado en los detalle_pedidos existentes que pertenezcan a este pedido. 
    def monto_total_display(self, obj):
        return f"${obj.monto_total:,.2f}" # Formateado como moneda
    monto_total_display.short_description = "Monto Total" # Nombre de la columna en el admin

