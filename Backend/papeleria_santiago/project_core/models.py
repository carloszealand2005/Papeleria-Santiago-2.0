from django.db import models
from django.db.models import Sum



# @UTPL
#-----------
# Este modelo físico esta basado en lo discutido en la reunión de Papelería Santiago
# Se tomó como referencia el archivo excel que contiene los diferentes productos
# Así mismo con un ejemplo de producto vendido
#-----------


#----------------
# Tabla producto:

class Producto(models.Model):
    SKU = models.CharField(max_length=20, primary_key=True)
    codigo_barras = models.CharField(max_length=30, blank=True, null=True)
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)
    marca = models.CharField(max_length=50, blank=True, null=True)


    categoria = models.CharField(max_length=50, blank=True, null=True)
    subcategoria = models.CharField(max_length=50, blank=True, null=True)
    variante = models.CharField(max_length=50, blank=True, null=True)

    imagen_url = models.URLField(blank=True, null=True)


    def __str__(self):
        return f"{self.SKU} - {self.nombre}"


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

    
    def __str__(self):
        return f"Precio {self.pvp} para {self.producto.SKU} \n El precio al por mayor para este producto es: {self.pvm}"

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
    nombre = models.CharField(max_length=100)
    cedula = models.CharField(max_length=20, blank=True, null=True)
    telefono = models.CharField(max_length=30, blank=True, null=True)
    email = models.CharField(max_length=100, blank=True, null=True)
    direccion = models.TextField(blank=True, null=True)

    PERSONA = 'Persona'
    EMPRESA = 'Empresa'
    TIPOS_CLIENTES_CHOICES = [
        (PERSONA, 'Persona'),
        (EMPRESA, 'Empresa'),
    ]

    tipo_cliente = models.CharField(max_length=20, choices=TIPOS_CLIENTES_CHOICES)


    def __str__(self):
        return f"{self.nombre} - {self.email}. \n Este cliente es una {self.tipo_cliente}."


#-----------
# Tabla pedido:
class Pedido(models.Model):

  

    ESTADO_PEDIDO_CHOICES = [
        ('Pendiente', 'Pendiente'),
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

    @property
    def monto_total(self):
        # Suma el campo 'total' de todos los DetallePedido relacionados con este Pedido
        total_agregado = self.detalles.aggregate(total_sum=Sum('total'))['total_sum']
        return total_agregado if total_agregado is not None else 0.00


    def __str__(self):
        return f"Pedido {self.id} de {self.cliente.nombre} - Total: {self.monto_total}"

# ----------
# Tabla detalle pedido:
class DetallePedido(models.Model):


    pedido = models.ForeignKey(
        Pedido,
        on_delete=models.CASCADE,    # borrar pedido → borrar sus detalles
        related_name="detalles"
    )
    producto = models.ForeignKey(
        Producto,
        on_delete=models.RESTRICT,   # no eliminar productos que tengan ventas históricas
    )
    
    cantidad = models.IntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    descuento = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    total = models.DecimalField(max_digits=10, decimal_places=2)

    def save(self, *args, **kwargs):
        self.subtotal = self.cantidad * self.precio_unitario
        self.total = self.subtotal - self.descuento
        super().save(*args, **kwargs)


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

    empresa = models.CharField(max_length=100)
    ESTADO_ENTREGA_CHOICES = [
        ('Pendiente', 'Pendiente'),
        ('Preparando', 'Preparando'),
        ('Despachado', 'Despachado'),
        ('Entregado', 'Entregado'),
    ]

    numero_guia = models.CharField(max_length=50, blank=True, null=True)
    estado_entrega = models.CharField(max_length=20, choices=ESTADO_ENTREGA_CHOICES)
    fecha_actualizacion = models.DateField(blank=True, null=True)

