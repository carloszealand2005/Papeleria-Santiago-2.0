from django.db.models.signals import post_save, post_delete, pre_save
from django.dispatch import receiver
from .models import DetallePedido, Pedido, Comprobante, Cliente, Carrito, DetalleCarrito, Producto, Transportista # Importamos Producto para la nueva señal
import datetime
from django.core.mail import send_mail
from django.conf import settings


#------------------
# Clase Djando Signals
# Esta clase sirve para reaccionar a cambios en la base de datos, modificando otras tablas. 
#------------------

# ------------------
# Email automático al aprobar una cuenta mayorista (Empresa):
# cuando Cliente.estado_cuenta cambia a ACTIVO (por ejemplo, desde Django Admin)
# ------------------

@receiver(pre_save, sender=Cliente)
def _cliente_capture_estado_previo(sender, instance, **kwargs):
    """
    Guardamos el estado previo para detectar transiciones (ej: PENDIENTE -> ACTIVO).
    """
    if not instance.pk:
        instance._estado_cuenta_anterior = None
        return
    try:
        instance._estado_cuenta_anterior = Cliente.objects.filter(pk=instance.pk).values_list('estado_cuenta', flat=True).first()
    except Exception:
        instance._estado_cuenta_anterior = None


@receiver(post_save, sender=Cliente)
def enviar_correo_aprobacion_empresa(sender, instance, created, **kwargs):
    """
    Enviar email SOLO para cuentas Empresa cuando pasan a ACTIVO.
    No bloquea el guardado si el SMTP falla.
    """
    try:
        if instance.tipo_cliente != Cliente.EMPRESA:
            return

        estado_anterior = getattr(instance, '_estado_cuenta_anterior', None)
        if instance.estado_cuenta != Cliente.ACTIVO:
            return
        if estado_anterior == Cliente.ACTIVO:
            return

        # Determinar email destino
        to_email = None
        if getattr(instance, 'user_id', None) and getattr(instance.user, 'email', None):
            to_email = instance.user.email
        elif getattr(instance, 'email', None):
            to_email = instance.email
        if not to_email:
            return

        # Determinar "Nombre de usuario" solicitado
        nombre_usuario = None
        if getattr(instance, 'user_id', None) and getattr(instance.user, 'username', None):
            nombre_usuario = instance.user.username
        else:
            nombre_usuario = instance.nombre or "tu usuario"

        subject = "Cuenta de empresa verificada - Papelería Santiago"
        message = (
            f"Tu cuenta de empresa para {nombre_usuario} ha sido verificada, ya puedes iniciar sesión dentro de la tienda virtual Papelería Santiago."
        )
        from_email = getattr(settings, 'DEFAULT_FROM_EMAIL', None) or settings.EMAIL_HOST_USER
        send_mail(subject, message, from_email, [to_email], fail_silently=False)
    except Exception:
        # No interrumpir el guardado del Cliente por fallos de email
        return


# ------------------
# Automatización post-aprobación de transferencias:
# cuando Pedido pasa de "Pendiente" -> "Pagado" (y es transferencia), crear Comprobante + Transportista.
# ------------------

@receiver(pre_save, sender=Pedido)
def _pedido_capture_estado_previo(sender, instance, **kwargs):
    """
    Guardamos el estado previo para detectar transiciones (ej: Pendiente -> Pagado).
    """
    if not instance.pk:
        instance._estado_pedido_anterior = None
        return
    try:
        instance._estado_pedido_anterior = Pedido.objects.filter(pk=instance.pk).values_list('estado_pedido', flat=True).first()
    except Exception:
        instance._estado_pedido_anterior = None


@receiver(post_save, sender=Pedido)
def crear_factura_y_envio_al_aprobar_transferencia(sender, instance, created, **kwargs):
    """
    Si un admin aprueba el pago manualmente cambiando el estado del pedido:
    - SOLO cuando pasa de 'Pendiente' a 'Pagado' (para transferencias)
    - y SOLO si aún no existe Comprobante/Transportista

    Esto evita romper el flujo de tarjeta (que ya crea comprobante/envío en checkout).
    """
    try:
        if created:
            return

        estado_anterior = getattr(instance, '_estado_pedido_anterior', None)
        # Solo aplica a transferencias (tarjeta ya crea comprobante/envío en checkout).
        if instance.metodo_pago != 'Transferencia bancaria':
            return

        if estado_anterior != 'Pendiente':
            return
        if instance.estado_pedido != 'Pagado':
            return

        # Idempotencia: crear solo lo faltante.
        if not Transportista.objects.filter(pedido=instance).exists():
            Transportista.objects.create(
                pedido=instance,
                estado_entrega='Pendiente',
            )

        if Comprobante.objects.filter(pedido=instance).exists():
            return  # ya hay comprobante

        Comprobante.objects.create(
            pedido=instance,
            numero_factura=f"FAC-{instance.id}-{instance.fecha_pedido.strftime('%Y%m%d')}",
            cedula_cliente=(instance.cedula_envio or instance.cliente.cedula or None),
            direccion_cliente=(instance.direccion_envio or instance.cliente.direccion),
            email_cliente=instance.cliente.email,
            subtotal=instance.subtotal_general_comprobante,
            descuento=instance.descuento_general_comprobante,
            iva=instance.iva_general_comprobante,
            total=instance.total_general_comprobante,
            costo_envio=instance.costo_envio,
            metodo_pago=instance.metodo_pago,
            estado_fiscal='Emitido',
        )
    except Exception:
        # No bloquear el guardado del Pedido por fallos en automatización
        return

# Receiver: Cuándo Pedido se guarda (post_save) reaccionará este método
# @receiver(post_save, sender=Pedido)
# # Función que se ejecuta cuándo un pedido cambia su estado a 'Pagado' (Crear un comprobante para el pedido)
# def crear_comprobante_al_pagar_pedido(sender, instance, created, **kwargs):
#     # Solo actuar si el pedido fue actualizado (no creado por primera vez)
#     # y si el estado es 'Pagado'
#     if instance.estado_pedido == 'Pagado': # Eliminado 'not created' de la condición
#         # Verificar si ya existe un comprobante para este pedido
#         if not Comprobante.objects.filter(pedido=instance).exists():
#             # El Comprobante necesita campos requeridos. Vamos a popularlos desde el Pedido y Cliente.
#             # Algunas de estos campos son null=True, blank=True, por lo que podemos dejarlos en blanco
#             # si no tenemos un valor directo aún.

#             # Obtener el cliente asociado al pedido
#             cliente = instance.cliente

#             Comprobante.objects.create(
#                 pedido=instance,
#                 numero_factura=f"FAC-{instance.id}-{instance.fecha_pedido.strftime('%Y%m%d')}", # Generar número de factura
#                 cedula_cliente=cliente.cedula if cliente.cedula else 'NO ESPECIFICADO', 
#                 direccion_cliente=cliente.direccion,
#                 email_cliente=cliente.email,
#                 subtotal=instance.subtotal_general_comprobante,
#                 descuento=instance.descuento_general_comprobante,
#                 iva=instance.iva_general_comprobante,
#                 total=instance.total_general_comprobante,
#                 metodo_pago='Tarjeta de crédito', # Por defecto, ajustar según lógica
#                 estado_fiscal='Emitido',
#                 # url_factura en blanco. TODO(PENDIENTE: GUARDAR URL DE LA FACTURA EN PRODUCCIÓN)
#             )
#             print(f"Comprobante creado para el Pedido {instance.id}")


# Señal para actualizar la fecha_actualizacion del Carrito cuando cambia un DetalleCarrito
@receiver([post_save, post_delete], sender=DetalleCarrito)
def actualizar_fecha_carrito(sender, instance, **kwargs):
    carrito = instance.carrito
    carrito.save() # Al guardar el carrito, auto_now=True actualizará fecha_actualizacion


#------------------
# Señales para actualizar total_vendidos en Producto
#------------------

# Señal para incrementar total_vendidos cuando se crea un DetallePedido
@receiver(post_save, sender=DetallePedido)
def incrementar_total_vendidos(sender, instance, created, **kwargs):
    # SOLO FUNCIONA AL CREARSE EL REGISTRO
    if created:
        producto = instance.producto
        producto.total_vendidos += instance.cantidad
        producto.save()

# Señal para decrementar total_vendidos cuando se elimina un DetallePedido
@receiver(post_delete, sender=DetallePedido)
def decrementar_total_vendidos(sender, instance, **kwargs):
    producto = instance.producto
    producto.total_vendidos -= instance.cantidad
    producto.save()
