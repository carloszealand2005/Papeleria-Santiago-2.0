from django.db import models
from django.db.models import Sum
from django.contrib.auth.models import User # Necesario para vincular con Cliente
from django.contrib.auth.hashers import make_password
from decimal import Decimal # Necesario para cálculos precisos



# @UTPL
#-----------
# Este modelo físico esta basado en lo discutido en la reunión de Papelería Santiago
# Se tomó como referencia el archivo excel que contiene los diferentes productos
# Así mismo con un ejemplo de producto vendido
#-----------

#------
# Tablas de categoría, subcategoría y variantes
class Categoria(models.Model):
    nombre_categoria = models.CharField(max_length=50)
    descripcion_categoria = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.nombre_categoria}"

class Subcategoria(models.Model):
    nombre_subcategoria = models.CharField(max_length=50) # Fixed typo: charField -> CharField
    descripcion_categoria = models.TextField(blank=True, null=True)
    foto_categoria_url = models.URLField(blank=True, null=True) # URL de imagen para mostrar en frontend
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.nombre_subcategoria}"

class Variante(models.Model):
    nombre_variante = models.CharField(max_length=50)
    descripcion_variante = models.TextField(blank=True, null=True)
    subcategoria = models.ForeignKey(Subcategoria, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.nombre_variante}"

#----------------
# Tabla producto:

class Producto(models.Model):
    SKU = models.CharField(max_length=20, primary_key=True)
    codigo_barras = models.CharField(max_length=30, blank=True, null=True)
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)
    marca = models.CharField(max_length=50, blank=True, null=True)


    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, blank=True, null=True)
    subcategoria = models.ForeignKey(Subcategoria, on_delete=models.SET_NULL, blank=True, null=True)
    variante = models.ForeignKey(Variante, on_delete=models.SET_NULL, blank=True, null=True)

    caracteristica1 = models.CharField(max_length=50, blank=True, null=True)
    caracteristica2 = models.CharField(max_length=50, blank=True, null=True)
    caracteristica3 = models.CharField(max_length=50, blank=True, null=True)
    caracteristica4 = models.CharField(max_length=50, blank=True, null=True)
    caracteristica5 = models.CharField(max_length=50, blank=True, null=True)

    imagen_url = models.URLField(blank=True, null=True)
    imagen_url2 = models.URLField(blank=True, null=True)
    imagen_url3 = models.URLField(blank=True, null=True)
    imagen_url4 = models.URLField(blank=True, null=True)

    total_vendidos = models.IntegerField(default=0)

    # ----------------
    # Mayoristas (Empresa)
    # - disponible_mayorista: permite excluir productos del catálogo mayorista sin depender del bulto mínimo
    # - bulto_minimo_mayorista: cantidad mínima por SKU (se valida por total acumulado en carrito)
    # ----------------
    disponible_mayorista = models.BooleanField(default=True)
    bulto_minimo_mayorista = models.PositiveIntegerField(default=1)


    def __str__(self):
        return f"{self.SKU} - {self.nombre}. Se han vendido {self.total_vendidos} unidades."

#----------------
# Tabla precio: 

class Precio(models.Model):

    # Un producto solo tendrá un precio. Razón para usar @OneToOneField
    producto = models.OneToOneField(
        Producto,
        on_delete=models.CASCADE,    # si se borra producto → borrar precio asociado
        related_name="precios"
    )
    pvp = models.DecimalField(max_digits=10, decimal_places=2) # Precio de venta al público
    pvm = models.DecimalField(max_digits=10, decimal_places=2) # Precio de venta al mayor
    iva = models.DecimalField(max_digits=4, decimal_places=2)  # porcentaje de IVA

    descuento_publico = models.DecimalField(max_digits= 5, decimal_places=2, default=Decimal(0.00))
    descuento_mayorista = models.DecimalField(max_digits= 5, decimal_places=2, default=Decimal(0.00))
    
    @property
    def precio_con_descuento_publico(self):
        # Precio con descuento (sin IVA) = PVP * (1 - descuento_publico/100)
        precio_con_descuento = self.pvp * (Decimal('1.00') - (self.descuento_publico / Decimal('100.00')))
        return precio_con_descuento.quantize(Decimal('0.01'))

    @property
    def precio_con_descuento_mayorista(self):
        # Precio con descuento (sin IVA) = PVM * (1 - descuento_mayorista/100)
        precio_con_descuento = self.pvm * (Decimal('1.00') - (self.descuento_mayorista / Decimal('100.00')))
        return precio_con_descuento.quantize(Decimal('0.01'))

    @property
    def precio_con_iva_publico(self):
        # Precio con descuento E IVA = (precio_con_descuento_publico) * (1 + IVA/100)
        precio_con_descuento = self.precio_con_descuento_publico
        precio_final = precio_con_descuento * (Decimal('1.00') + (self.iva / Decimal('100.00')))
        return precio_final.quantize(Decimal('0.01'))

    @property
    def precio_con_iva_mayorista(self):
        # Precio con descuento E IVA = (precio_con_descuento_mayorista) * (1 + IVA/100)
        precio_con_descuento = self.precio_con_descuento_mayorista
        precio_final = precio_con_descuento * (Decimal('1.00') + (self.iva / Decimal('100.00')))
        return precio_final.quantize(Decimal('0.01'))
    
    def __str__(self):
        return f"Precio {self.pvp} para {self.producto.SKU} \n El precio al por mayor para este producto es: {self.pvm}. -> Descuento publico: {self.descuento_publico}% -> Descuento mayorista: {self.descuento_mayorista}%"

#----------------
# Tabla inventaio:

class Inventario(models.Model):

    # Un producto solo tendrá un inventario. Razón para usar @OneToOneField
    producto = models.OneToOneField(
        Producto,
        on_delete=models.CASCADE,   # si se borra producto → borrar inventario
        primary_key=False
    )
    stock = models.IntegerField(default=0)
    ubicacion_bodega = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"Inventario de {self.producto.SKU}: {self.stock}"
    

#----------------
# Tabla cliente:

class Cliente(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True, related_name='cliente_profile') # <-- Nueva línea para vincular con User
    nombre = models.CharField(max_length=100)
    cedula = models.CharField(max_length=20, blank=True, null=True)
    telefono = models.CharField(max_length=30, blank=True, null=True)
    email = models.CharField(max_length=100, blank=True, null=True)
    ciudad = models.CharField(max_length=100, blank=True, null=True)
    direccion = models.TextField(blank=True, null=True)

    PERSONA = 'Persona'
    EMPRESA = 'Empresa'
    TIPOS_CLIENTES_CHOICES = [
        (PERSONA, 'Persona'),
        (EMPRESA, 'Empresa'),
    ]

    tipo_cliente = models.CharField(max_length=20, choices=TIPOS_CLIENTES_CHOICES)
    url_validacion = models.URLField(blank=True, null=True)

    # ----------------
    # Estado de cuenta (aplica a Persona y Empresa)
    # - Persona: nace ACTIVO tras verificar OTP
    # - Empresa: nace PENDIENTE tras verificar OTP y no puede logear hasta ACTIVO
    # ----------------
    ACTIVO = 'ACTIVO'
    PENDIENTE = 'PENDIENTE'
    INACTIVO = 'INACTIVO'
    ELIMINADO = 'ELIMINADO'
    ESTADOS_CUENTA_CHOICES = [
        (ACTIVO, 'ACTIVO'),
        (PENDIENTE, 'PENDIENTE'),
        (INACTIVO, 'INACTIVO'),
        (ELIMINADO, 'ELIMINADO'),
    ]
    estado_cuenta = models.CharField(
        max_length=20,
        choices=ESTADOS_CUENTA_CHOICES,
        default=ACTIVO,
    )
  


    def __str__(self):
        return f"{self.nombre} - {self.email}. \n Este cliente es una {self.tipo_cliente}."

    def save(self, *args, **kwargs):
        """
        Mantiene sincronizado el estado de negocio (Cliente.estado_cuenta) con la capacidad
        de autenticarse en el sistema (User.is_active).
        """
        super().save(*args, **kwargs)

        # Si no hay usuario asociado, no hay nada que sincronizar
        if not self.user_id:
            return

        should_be_active = self.estado_cuenta == self.ACTIVO
        if self.user.is_active != should_be_active:
            self.user.is_active = should_be_active
            self.user.save(update_fields=['is_active'])


# ----------------
# Pre-registro (staging) para verificación OTP por email (2 pasos)
class PreRegistroUser(models.Model):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=150, blank=True, null=True)
    # NUNCA guardar en texto plano. Se guarda el hash (make_password).
    password = models.CharField(max_length=128)
    celular = models.CharField(max_length=30, blank=True, null=True)
    ciudad = models.CharField(max_length=100, blank=True, null=True)
    # Campos adicionales para soportar registro mayorista (staging antes del OTP correcto)
    tipo_cliente = models.CharField(
        max_length=20,
        choices=Cliente.TIPOS_CLIENTES_CHOICES,
        default=Cliente.PERSONA
    )
    url_validacion = models.URLField(blank=True, null=True)
    otp_code = models.CharField(max_length=6)
    intentos = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # Si accidentalmente llega un password sin hashear, lo hasheamos.
        # (No re-hashear si ya parece hash de Django.)
        if self.password and not str(self.password).startswith('pbkdf2_'):
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"PreRegistroUser<{self.email}>"

# ----------------
# OTP - Recuperación de contraseña (6 dígitos por email)
#
# Notas de seguridad:
# - No se revela si un email existe o no en el endpoint de solicitud (eso se maneja en la vista).
# - Se guarda el OTP en DB y se invalida al usarse.
# - Se controla el reenvío con contador y bloqueo temporal.
class PasswordResetOtp(models.Model):
    email = models.EmailField(unique=True)
    otp_code = models.CharField(max_length=6)
    resend_count = models.IntegerField(default=0)  # número de reenvíos (no incluye el envío inicial)
    sent_at = models.DateTimeField(blank=True, null=True)  # último envío/generación del OTP
    blocked_until = models.DateTimeField(blank=True, null=True)  # bloqueo temporal por reenvíos
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"PasswordResetOtp<{self.email}>"

#----------------
#Tabla favoritos cliente: 

class FavoritosCliente(models.Model):
    producto = models.ForeignKey(
        Producto,
        on_delete=models.RESTRICT, # No borrar producto si se borra el favorito asociado
        related_name="favoritos_cliente"
    )
    cliente = models.ForeignKey(
        Cliente,
        on_delete=models.RESTRICT, # No borrar cliente si se borra el favorito asociado
        related_name="favoritos_cliente"
    )

    fecha_creacion = models.DateField(auto_now_add=True)

    class Meta:
        unique_together = ('cliente', 'producto')

    def __str__(self):
        return f"<3 --> {self.cliente.nombre} - {self.producto.nombre} de marca {self.producto.marca}"
   
  
#----------------
# Tabla carrito:
class Carrito(models.Model):
    ESTADO_CARRITO_CHOICES = [
        ('Activo', 'Activo'),
        ('Inactivo', 'Inactivo'),
        ('Convertido a pedido', 'Convertido a pedido'),
        ('Abandonado', 'Abandonado'),
    ]
    cliente = models.ForeignKey(
        Cliente,
        on_delete=models.RESTRICT, # No borrar cliente si tiene carrito
        related_name="carritos"
    )
    fecha_creacion = models.DateField(auto_now_add=True) # Solo cuando se crea este registro
    fecha_actualizacion = models.DateField(auto_now=True) # Cada vez que se hay un cambio en sus detalles. 
   


    @property
    def estado_dinamico(self):
        if self.detalles_carrito.exists(): #Verificar si existen DetalleCarrito asociados. 
            return 'Activo'
        return 'Inactivo'
    
    @property
    def subtotal_carrito(self):
        subtotal_agregado = self.detalles_carrito.aggregate(subtotal_sum=Sum('subtotal_antes_descuento'))['subtotal_sum']
        return subtotal_agregado if subtotal_agregado is not None else Decimal('0.00')

    @property
    def descuento_carrito(self):
        descuento_agregado = self.detalles_carrito.aggregate(descuento_sum=Sum('descuento_detalle_carrito'))['descuento_sum']
        return descuento_agregado if descuento_agregado is not None else Decimal('0.00')
    
    @property
    def iva_carrito(self):
        iva_agregado = self.detalles_carrito.aggregate(iva_sum=Sum('iva_detalle_carrito'))['iva_sum']
        return iva_agregado if iva_agregado is not None else Decimal('0.00')

    @property
    def total_carrito(self):
        # Suma el campo 'total_detalle_carrito' de todos los DetalleCarrito relacionados con este Carrito
        total_agregado = self.detalles_carrito.aggregate(total_sum=Sum('total_detalle_carrito'))['total_sum']
        return total_agregado if total_agregado is not None else Decimal('0.00')

   


    def __str__(self):
        return f"Carrito de {self.cliente.nombre} - Estado: {self.estado_dinamico} - Total: {self.total_carrito}"

class DetalleCarrito(models.Model):
    carrito = models.ForeignKey(
        Carrito,
        on_delete=models.CASCADE, # Borrar detalle carrito si se borra el carrito asociado
        related_name="detalles_carrito"
    )
    producto = models.ForeignKey(
        Producto,
        on_delete=models.RESTRICT, # No borrar producto si se borra el detalle carrito asociado
    )

    cantidad = models.IntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    subtotal_antes_descuento = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True) # Nuevo campo
    subtotal_detalle_carrito = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    iva_detalle_carrito = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    descuento_detalle_carrito = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    total_detalle_carrito = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)



    # Método para calcular el subtotal y el total del detalle del carrito
    def save(self, *args, **kwargs):

        if self.producto and self.carrito:
            try:
                precio_obj = self.producto.precios

                # Determinar el precio unitario base (antes de descuento) y el porcentaje de descuento
                base_precio_unitario = Decimal('0.00')
                descuento_porcentaje = Decimal('0.00')

                # Mayorista SOLO si es Empresa y su cuenta está ACTIVA
                if (
                    self.carrito.cliente.tipo_cliente == 'Empresa'
                    and getattr(self.carrito.cliente, 'estado_cuenta', None) == Cliente.ACTIVO
                ):
                    base_precio_unitario = precio_obj.pvm
                    descuento_porcentaje = precio_obj.descuento_mayorista
                else:
                    base_precio_unitario = precio_obj.pvp
                    descuento_porcentaje = precio_obj.descuento_publico

                # Calcular el subtotal antes de aplicar cualquier descuento
                self.subtotal_antes_descuento = self.cantidad * base_precio_unitario

                # Aplicar descuento al precio unitario
                if descuento_porcentaje > Decimal('0.00'):
                    descuento_factor = descuento_porcentaje / Decimal('100.00')
                    self.precio_unitario = base_precio_unitario * (Decimal('1.00') - descuento_factor)
                    # Almacenar el monto del descuento aplicado en este detalle
                    self.descuento_detalle_carrito = (base_precio_unitario - self.precio_unitario) * self.cantidad
                else:
                    self.precio_unitario = base_precio_unitario
                    self.descuento_detalle_carrito = Decimal('0.00')

            except Precio.DoesNotExist:
                raise ValueError("Producto sin precio asociado")

        if self.precio_unitario is not None:
            # El subtotal se calcula con el precio unitario YA con descuento aplicado
            self.subtotal_detalle_carrito = self.cantidad * self.precio_unitario

            # Calcular IVA del detalle del carrito sobre el subtotal ya con descuento
            if self.producto.precios and self.producto.precios.iva is not None:
                iva_porcentaje = self.producto.precios.iva / Decimal('100.00')
                self.iva_detalle_carrito = self.subtotal_detalle_carrito * iva_porcentaje
            else:
                self.iva_detalle_carrito = Decimal('0.00')

            # El total_detalle_carrito ya no necesita restar self.descuento_detalle_carrito aquí
            # porque self.precio_unitario ya tiene el descuento aplicado.
            # Simplemente suma el subtotal y el IVA.
            self.total_detalle_carrito = self.subtotal_detalle_carrito + self.iva_detalle_carrito
        else:
            self.subtotal_antes_descuento = None # Asegurar que también sea None si no hay precio
            self.subtotal_detalle_carrito = None
            self.iva_detalle_carrito = None
            self.descuento_detalle_carrito = Decimal('0.00')
            self.total_detalle_carrito = None
        super().save(*args, **kwargs)


    def __str__(self):
        return f"{self.cantidad} x {self.producto.SKU} en Carrito {self.carrito.id} que pertenece a {self.carrito.cliente.nombre}"


#-----------
# Tabla pedido:
class Pedido(models.Model):

  

    ESTADO_PEDIDO_CHOICES = [
        ('Pendiente', 'Pendiente'),
        # Pago por transferencia: pedido creado pero esperando validación manual.
        ('En revisión', 'En revisión'),
        ('Pagado', 'Pagado'),
        ('Cancelado', 'Cancelado'),
    ]


    # Un pedido solo estará asociado por un cliente. Razón para usar @ForeignKey
    cliente = models.ForeignKey(
        Cliente,
        on_delete=models.RESTRICT,   # no borrar cliente si tiene pedidos
        related_name="pedidos"
    )

    fecha_pedido = models.DateField(auto_now_add=True)
    estado_pedido = models.CharField(max_length=20, choices=ESTADO_PEDIDO_CHOICES)

    # ----------------
    # Snapshot de datos de envío (domicilio) al momento de pagar.
    # Importante: NO deben depender del perfil del cliente, porque el cliente puede cambiar su dirección en el futuro.
    # Estos campos se pueden enviar desde el frontend al pagar, o (por compatibilidad) copiarse desde Cliente si faltan.
    # ----------------
    ciudad_envio = models.CharField(max_length=100, blank=True, null=True)
    direccion_envio = models.TextField(blank=True, null=True)
    numero_casa_envio = models.CharField(max_length=50, blank=True, null=True)
    codigo_postal_envio = models.CharField(max_length=20, blank=True, null=True)

    # Snapshot adicional (contacto y pago) al momento de pagar:
    cedula_envio = models.CharField(max_length=20, blank=True, null=True)
    telefono_envio = models.CharField(max_length=20, blank=True, null=True)
    referencia_envio = models.TextField(blank=True, null=True)
    METODO_PAGO_CHOICES = [
        ('Tarjeta', 'Tarjeta'),
        ('Transferencia bancaria', 'Transferencia bancaria'),
    ]
    metodo_pago = models.CharField(max_length=50, choices=METODO_PAGO_CHOICES, blank=True, null=True, default='Tarjeta')
    costo_envio = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, default=Decimal('0.00'))

    # Evidencia de pago por transferencia (imagen). Para pagos con tarjeta será NULL.
    comprobante_transferencia = models.ImageField(
        upload_to='comprobantes_transferencia/',
        blank=True,
        null=True,
    )

    @property
    def subtotal_general_comprobante(self):
        # Suma los subtotales de todos los DetallePedido asociados a este Pedido
        subtotal_agregado = self.detalles_pedido.aggregate(subtotal_sum=Sum('subtotal_detalle_pedido'))['subtotal_sum']
        return subtotal_agregado if subtotal_agregado is not None else Decimal('0.00')

    @property
    def descuento_general_comprobante(self):
        # Suma los descuentos de todos los DetallePedido asociados a este Pedido
        descuento_agregado = self.detalles_pedido.aggregate(descuento_sum=Sum('descuento_detalle_pedido'))['descuento_sum']
        return descuento_agregado if descuento_agregado is not None else Decimal('0.00')

    @property
    def iva_general_comprobante(self):
        # Calcula el IVA sumando el IVA de cada detalle. 
        # NOTA: Si el IVA se calcula por item en DetallePedido, es más complejo que una simple suma de IVA de cada producto.
        # Aquí, estamos asumiendo que el campo 'iva' en DetallePedido representaría el IVA de ese ítem.
        # Si IVA es un porcentaje en DetallePedido, la lógica de cálculo aquí sería diferente (aplicar porcentaje al subtotal de cada detalle y sumar).
        # Por ahora, haremos una suma directa si existiera un campo iva en DetallePedido.
        # Dado que Precio tiene iva, podríamos calcularlo aquí o si cada DetallePedido ya lo tiene.
        # Para simplificar y seguir el patrón de tus campos, vamos a asumir que cada DetallePedido podría tener un 'iva' explícito si lo hubieras definido.
        # Si el IVA es un porcentaje del precio unitario en DetallePedido (o de Precio), la lógica debería ser:
        # SUM(detalle.cantidad * detalle.precio_unitario * (detalle.producto.precios.iva / 100))
  
        # WARNING:
        # POR AHORA, EL IVA SE CALCULA CON LA SUMA DE TODOS LOS IVA DE DETALLE_PEDIDO
        iva_agregado = self.detalles_pedido.aggregate(iva_sum=Sum('iva_detalle_pedido'))['iva_sum']
        return iva_agregado if iva_agregado is not None else Decimal('0.00')

    @property
    def total_general_comprobante(self):
        # Suma los totales de todos los DetallePedido asociados a este Pedido
        total_agregado = self.detalles_pedido.aggregate(total_sum=Sum('total_detalle_pedido'))['total_sum']
        total_items = total_agregado if total_agregado is not None else Decimal('0.00')
        costo_envio = self.costo_envio if self.costo_envio is not None else Decimal('0.00')
        return total_items + costo_envio

    @property
    def monto_total(self):
        # Suma el campo 'total' de todos los DetallePedido relacionados con este Pedido
        total_agregado = self.detalles_pedido.aggregate(total_sum=Sum('total_detalle_pedido'))['total_sum']
        total_items = total_agregado if total_agregado is not None else Decimal('0.00')
        costo_envio = self.costo_envio if self.costo_envio is not None else Decimal('0.00')
        return total_items + costo_envio


    def __str__(self):
        return f"Pedido {self.id} de {self.cliente.nombre} - Total: {self.monto_total}"

# ----------
# Tabla detalle pedido:
class DetallePedido(models.Model):
    pedido = models.ForeignKey(
        Pedido,
        on_delete=models.CASCADE,    # borrar pedido → borrar sus detalles
        related_name="detalles_pedido"
    )
    producto = models.ForeignKey(
        Producto,
        on_delete=models.RESTRICT,   # no eliminar productos que tengan ventas históricas
    )
    
    cantidad = models.IntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal_detalle_pedido = models.DecimalField(max_digits=10, decimal_places=2)
    iva_detalle_pedido = models.DecimalField(max_digits=10, decimal_places=2)
    descuento_detalle_pedido = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00')) # Asegurarse de que el default sea un objeto Decimal
    total_detalle_pedido = models.DecimalField(max_digits=10, decimal_places=2)

    

    def __str__(self):
        return f"{self.cantidad} x {self.producto.SKU} en Pedido {self.pedido.id}"


# ------------
# Tabla Transportista:
# NOTA: Un pedido solo estará asociado por un transportista. Razón para usar @OneToOneField 
class Transportista(models.Model):
    pedido = models.OneToOneField(
        Pedido,
        on_delete=models.CASCADE,   # borrar pedido → borrar transportista
        primary_key=False
    )

    # Puede quedar vacío al crear el pedido (se asigna luego por admin/operador)
    empresa = models.CharField(max_length=100, blank=True, null=True)
    ESTADO_ENTREGA_CHOICES = [
        ('Pendiente', 'Pendiente'),
        ('Preparando', 'Preparando'),
        ('Despachado', 'Despachado'),
        ('Entregado', 'Entregado'),
    ]

    numero_guia = models.CharField(max_length=50, blank=True, null=True)
    estado_entrega = models.CharField(max_length=20, choices=ESTADO_ENTREGA_CHOICES, default='Pendiente')
    # DateTime para tracking real; auto_now actualiza cada vez que se guarda el registro.
    fecha_actualizacion = models.DateTimeField(blank=True, null=True, auto_now=True)


# ------------
# Tabla Comprobante:
# NOTA: Un pedido solo tendrá un comprobante. Razón para usar @OneToOneField
class Comprobante(models.Model):
    pedido = models.OneToOneField(
        Pedido,
        on_delete=models.DO_NOTHING,   # borrar pedido → NO BORRAR COMPROBANTE
        primary_key=False)


    # Nota: mantenemos opciones legacy para no romper comprobantes existentes en admin.
    # Para nuevos pedidos (MVP), el backend usará: 'Tarjeta' o 'Transferencia bancaria'.
    METODO_PAGO_CHOICES = [
        ('Tarjeta', 'Tarjeta'),
        ('Transferencia bancaria', 'Transferencia bancaria'),
        # Legacy:
        ('Tarjeta de crédito', 'Tarjeta de crédito'),
        ('Tarjeta de débito', 'Tarjeta de débito'),
        ('Cheque', 'Cheque'),
    ]

    ESTADO_FISCAL_CHOICES = [
        ('Emitido', 'Emitido'),
        ('Cancelado', 'Cancelado'),
        ('Pendiente', 'Pendiente'),
        ('Reembolsado', 'Reembolsado'),
    ]

    numero_factura = models.CharField(max_length=50)
    cedula_cliente = models.CharField(max_length=20, blank=True, null=True)
    direccion_cliente = models.TextField(blank=True, null=True)
    email_cliente = models.EmailField(blank=True, null=True)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    descuento = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    iva = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    costo_envio = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, default=Decimal('0.00'))
    metodo_pago = models.CharField(max_length=50, choices=METODO_PAGO_CHOICES, blank=True, null=True)
    fecha_emision = models.DateField(auto_now_add=True)
    # Evidencia de pago por transferencia (archivo/imagen). Para MVP usamos FileField (no requiere Pillow).
    comprobante_transferencia_archivo = models.FileField(
        upload_to='comprobantes_transferencia/',
        blank=True,
        null=True,
        max_length=500,
    )
    estado_fiscal = models.CharField(max_length=20, choices=ESTADO_FISCAL_CHOICES, blank=True, null=True)

    def __str__(self):
        return f"Comprobante {self.numero_factura} para Pedido {self.pedido.id}"
