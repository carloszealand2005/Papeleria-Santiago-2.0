from django.contrib import admin
from .models import (
    Categoria, Cliente, FavoritosCliente, Comprobante, Producto, Pedido, Precio,
    Inventario, DetallePedido, Subcategoria, Transportista, Carrito, DetalleCarrito, Variante
)

# Registra tus modelos aquí.
admin.site.register(Cliente)
# admin.site.register(FavoritosCliente) # Se moverá debajo para personalización
admin.site.register(Producto)
admin.site.register(Precio)
admin.site.register(Inventario)
admin.site.register(DetallePedido)
admin.site.register(DetalleCarrito)

admin.site.register(Categoria)
admin.site.register(Subcategoria)
admin.site.register(Variante)

@admin.register(FavoritosCliente)
class FavoritosClienteAdmin(admin.ModelAdmin):
    list_display = ('id', 'cliente', 'producto', 'fecha_creacion')
    list_filter = ('fecha_creacion', 'cliente', 'producto')
    search_fields = ('cliente__nombre', 'producto__nombre', 'producto__SKU')
    readonly_fields = ('fecha_creacion',)


@admin.register(Carrito)
class CarritoAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'cliente', 'fecha_creacion', 'fecha_actualizacion', 'estado_dinamico',
        'total_carrito_display' # Incluimos la propiedad calculada
    )

    def total_carrito_display(self, obj):
        # Accede a la propiedad @property total_carrito del modelo Carrito
        return f"${obj.total_carrito:,.2f}" # Formateado como moneda
    total_carrito_display.short_description = "Total del Carrito"


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

@admin.register(Comprobante)
class ComprobanteAdmin(admin.ModelAdmin):
    list_display = ('id', 'pedido', 'numero_factura', 'fecha_emision', 'estado_fiscal')
    search_fields = ('numero_factura', 'fecha_emision', 'estado_fiscal')
    list_filter = ('fecha_emision', 'estado_fiscal')
