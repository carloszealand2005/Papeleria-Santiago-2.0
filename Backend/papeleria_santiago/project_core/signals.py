from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Pedido, Comprobante, Cliente


#------------------
# Clase Djando Signals
# Esta clase sirve para reaccionar a cambios en la base de datos, modificando otras tablas. 
#------------------

# Receiver: Cuándo Pedido se guarda (post_save) reaccionará este método
@receiver(post_save, sender=Pedido)
# Función que se ejecuta cuándo un pedido cambia su estado a 'Pagado' (Crear un comprobante para el pedido)
def crear_comprobante_al_pagar_pedido(sender, instance, created, **kwargs):
    # Solo actuar si el pedido fue actualizado (no creado por primera vez)
    # y si el estado es 'Pagado'
    if not created and instance.estado_pedido == 'Pagado':
        # Verificar si ya existe un comprobante para este pedido
        if not Comprobante.objects.filter(pedido=instance).exists():
            # El Comprobante necesita campos requeridos. Vamos a popularlos desde el Pedido y Cliente.
            # Algunas de estos campos son null=True, blank=True, por lo que podemos dejarlos en blanco
            # si no tenemos un valor directo aún.

            # Obtener el cliente asociado al pedido
            cliente = instance.cliente

            Comprobante.objects.create(
                pedido=instance,
                numero_factura=f"FAC-{instance.id}-{instance.fecha_pedido.strftime('%Y%m%d')}", # Generar número de factura
                cedula_cliente=cliente.cedula if cliente.cedula else 'NO ESPECIFICADO', 
                direccion_cliente=cliente.direccion,
                email_cliente=cliente.email,
                subtotal=instance.subtotal_general_comprobante,
                descuento=instance.descuento_general_comprobante,
                iva=instance.iva_general_comprobante,
                total=instance.total_general_comprobante,
                metodo_pago='Tarjeta de crédito', # Por defecto, ajustar según lógica
                estado_fiscal='Emitido',
                # url_factura se dejaría en blanco inicialmente o se generaría después
            )
            print(f"Comprobante creado para el Pedido {instance.id}")
