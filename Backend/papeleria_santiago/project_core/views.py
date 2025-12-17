from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.template.loader import get_template
from io import BytesIO
from xhtml2pdf import pisa
from .models import Comprobante, Pedido, Producto, Carrito, DetalleCarrito, Cliente, DetallePedido, Inventario # Importamos DetallePedido e Inventario
from rest_framework import viewsets, filters, status # Importar filters y status
from rest_framework.decorators import action # Importar action
from django_filters.rest_framework import DjangoFilterBackend # Importar DjangoFilterBackend
from .serializers import ProductoSerializer, CarritoSerializer, DetalleCarritoSerializer # Importar el serializador
from rest_framework.response import Response # Importar Response

# Create your views here.

# ------------------
# Aquí es en dónde se generará el comprobante de pago mediante un canal HTTP hacia la interfaz
#------------------

# La factura se genera a partir del ID del pedido; caso de no existir factura retornar 404. 
def generar_factura_pdf(request, pedido_id):
    # Obtener el objeto Pedido o retornar un 404 si no existe
    pedido = get_object_or_404(Pedido, id=pedido_id)
    
    # Intentar obtener el Comprobante asociado al Pedido
    try:
        comprobante = pedido.comprobante # Accedemos al Comprobante a través del related_name por defecto
    except Comprobante.DoesNotExist:
        return HttpResponse("No se encontró un comprobante para este pedido.", status=404)

    # Cargar la plantilla HTML
    template_path = 'project_core/factura_pdf.html'
    template = get_template(template_path)

    # Crear el contexto para la plantilla (pasamos el objeto comprobante)
    context = {'comprobante': comprobante}
    html = template.render(context)

    # Crear el objeto HttpResponse con el tipo de contenido PDF
    response = HttpResponse(content_type='application/pdf')
    # Configurar el encabezado para forzar la descarga del archivo
    response['Content-Disposition'] = f'attachment; filename="factura_{comprobante.numero_factura}.pdf"'

    # Generar el PDF usando xhtml2pdf
    pisa_status = pisa.CreatePDF(
        html, dest=response) # El HTML a convertir y dónde se guardará el PDF (en la respuesta HTTP)

    # Si hubo errores durante la generación del PDF
    if pisa_status.err:
        return HttpResponse('Tuvimos algunos errores al generar el PDF: <pre>' + html + '</pre>')
    return response

#------------------
# ViewSet para el modelo Producto (API REST)
# Maneja las peticiones GET, POST, PUT, DELETE para productos
#------------------


class ProductoViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter] # Añadir backends de filtro y búsqueda
    filterset_fields = ['categoria', 'marca', 'SKU'] # Filtrar por categoría, marca y SKU
    search_fields = ['nombre', 'descripcion', 'SKU', 'codigo_barras'] # Campos para búsqueda de texto
    ordering_fields = ['SKU', 'nombre', 'pvp', 'pvm'] # Campos para ordenar resultados

    # Para filtrar por rango de precio, podemos sobrescribir el método get_queryset
    def get_queryset(self):
        queryset = super().get_queryset()

        precio_min = self.request.query_params.get('precio_min')
        precio_max = self.request.query_params.get('precio_max')

        if precio_min:
            # Asumimos que `precios` es el related_name del OneToOneField del Precio
            # que apunta a Producto. Para filtrar por precio en el modelo Precio,
            # necesitamos acceder a `precios__pvp` o `precios__pvm`.
            # Vamos a usar `precios__pvp` para este ejemplo.
            queryset = queryset.filter(precios__pvp__gte=precio_min)
        if precio_max:
            queryset = queryset.filter(precios__pvp__lte=precio_max)
            
        # Filtrar por nombre de subcategoría (case-insensitive)
        subcategoria_nombre = self.request.query_params.get('subcategoria')
        if subcategoria_nombre:
            queryset = queryset.filter(subcategoria__nombre_subcategoria__iexact=subcategoria_nombre)

        return queryset
    
    @action(detail=False, methods=['get'])
    def destacados(self, request):
        """ Retorna una lista de los productos más vendidos (destacados). """
        limite = self.request.query_params.get('limite', 50) # Permitir un límite configurable, por defecto 50
        try:
            limite = int(limite)
        except ValueError:
            return Response({'error': 'El parámetro limite debe ser un número entero.'}, status=status.HTTP_400_BAD_REQUEST)
        
        productos_destacados = self.get_queryset()

        # Aplicar filtro por subcategoría si se proporciona
        subcategoria_nombre = self.request.query_params.get('subcategoria')
        if subcategoria_nombre:
            productos_destacados = productos_destacados.filter(subcategoria__nombre_subcategoria__iexact=subcategoria_nombre)

        productos_destacados = productos_destacados.order_by('-total_vendidos')[:limite]
        serializer = self.get_serializer(productos_destacados, many=True)
        return Response(serializer.data)


#------------------
# ViewSet para el modelo Carrito (API REST)
# Maneja las peticiones GET, POST, PUT, DELETE para carritos
#------------------
class CarritoViewSet(viewsets.ModelViewSet):
    queryset = Carrito.objects.all()
    serializer_class = CarritoSerializer

    @action(detail=True, methods=['post'])
    def pagar(self, request, pk=None):
        carrito = self.get_object() # Obtiene el carrito basado en el pk de la URL

        # --- 1. Autorización (simplificada por ahora, asumiendo usuario autenticado) ---
        # TODO: Implementar un sistema de autenticación y permisos más robusto.
        # Por ahora, verificamos si el cliente del carrito está asociado a un usuario
        #!!if not request.user.is_authenticated:
            #!!return Response({'error': 'Autenticación requerida para realizar el pago.'}, status=status.HTTP_403_FORBIDDEN)
        
        # Si el carrito no tiene un cliente asociado, o si el cliente no está vinculado a un User
        # o si el usuario autenticado no coincide con el cliente del carrito.
        #!!if not carrito.cliente or not carrito.cliente.user or carrito.cliente.user != request.user:
        #!!    return Response({'error': 'No tienes permiso para pagar este carrito.'}, status=status.HTTP_403_FORBIDDEN)


        # --- 2. Validar Carrito --- 
        #!!if not carrito.detalles_carrito.exists():
        #!!    return Response({'error': 'El carrito está vacío, no se puede realizar el pago.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # --- 3. Crear Pedido (estado inicial 'Pagado') ---
            pedido = Pedido.objects.create(
                cliente=carrito.cliente,
                estado_pedido='Pagado',
                # Otros campos del pedido se llenarán automáticamente o por señales si es necesario
            )

            # --- 4. Crear DetallePedido a partir de DetalleCarrito ---
            for detalle_carrito in carrito.detalles_carrito.all():
                DetallePedido.objects.create(
                    pedido=pedido,
                    producto=detalle_carrito.producto,
                    cantidad=detalle_carrito.cantidad,
                    precio_unitario=detalle_carrito.precio_unitario,
                    subtotal_detalle_pedido=detalle_carrito.subtotal_detalle_carrito,
                    iva_detalle_pedido=detalle_carrito.iva_detalle_carrito, # Asegurarse de que este campo tenga valor en DetalleCarrito
                    descuento_detalle_pedido=detalle_carrito.descuento_detalle_carrito,
                    total_detalle_pedido=detalle_carrito.total_detalle_carrito,
                )

            # --- 5. Crear Comprobante después de que todos los DetallePedido estén creados ---
            # Ahora las propiedades del Pedido (subtotal, descuento, iva, total) deberían ser correctas
            Comprobante.objects.create(
                pedido=pedido,
                numero_factura=f"FAC-{pedido.id}-{pedido.fecha_pedido.strftime('%Y%m%d')}",
                cedula_cliente=pedido.cliente.cedula if pedido.cliente.cedula else 'NO ESPECIFICADO',
                direccion_cliente=pedido.cliente.direccion,
                email_cliente=pedido.cliente.email,
                subtotal=pedido.subtotal_general_comprobante,
                descuento=pedido.descuento_general_comprobante,
                iva=pedido.iva_general_comprobante,
                total=pedido.total_general_comprobante,
                metodo_pago='Tarjeta de crédito', # Se mantiene el valor por defecto
                estado_fiscal='Emitido',
                # url_factura en blanco. TODO(PENDIENTE: GUARDAR URL DE LA FACTURA EN PRODUCCIÓN)
            )
            
            # --- 6. Borrar DetalleCarrito del carrito original ---
            # Esto también hará que el carrito.estado_dinamico pase a 'Inactivo'
            carrito.detalles_carrito.all().delete()
            carrito.save() # Guarda el carrito para actualizar la fecha_actualizacion

            # TODO: DEVOLVER UNA RESPUESTA DETALLADA DEL PEDIDO CREADO EXITOSAMENTE
            return Response({'message': 'Carrito pagado y pedido creado exitosamente.', 'pedido_id': pedido.id}, status=status.HTTP_201_CREATED)

        except Exception as e:
            # Si ocurre un error, puedes considerar revertir la creación del pedido
            # o manejarlo de forma específica. Por simplicidad, por ahora solo lo reportamos.
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


#------------------
# ViewSet para el modelo DetalleCarrito (API REST)
# Maneja las peticiones GET, POST, PUT, DELETE para detalles de carrito
#------------------
class DetalleCarritoViewSet(viewsets.ModelViewSet):
    serializer_class = DetalleCarritoSerializer
    # Usaremos el SKU del producto como campo de búsqueda para DELETE y GET por detalle
    lookup_field = 'producto__SKU'

    def get_queryset(self):
        # Asegurarse de que solo se muestren los detalles del carrito padre
        return DetalleCarrito.objects.filter(carrito_id=self.kwargs['carrito_pk'])

    def create(self, request, *args, **kwargs):
        carrito_id = self.kwargs['carrito_pk']
        producto_sku = request.data.get('producto_sku')
        cantidad = request.data.get('cantidad')

        if not producto_sku or not cantidad:
            return Response({'error': 'Producto SKU y cantidad son requeridos.'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            carrito = Carrito.objects.get(id=carrito_id)
            producto = Producto.objects.get(SKU=producto_sku)
        except Carrito.DoesNotExist:
            return Response({'error': 'Carrito no encontrado.'}, status=status.HTTP_404_NOT_FOUND)
        except Producto.DoesNotExist:
            return Response({'error': 'Producto no encontrado.'}, status=status.HTTP_404_NOT_FOUND)
        
        # Validación de stock
        try:
            inventario = producto.inventario # Asumiendo related_name 'inventario' en Producto a Inventario
        except Inventario.DoesNotExist:
            return Response({'error': 'Producto sin registro de inventario.'}, status=status.HTTP_404_NOT_FOUND)

        # Buscar si el DetalleCarrito ya existe para este producto en este carrito
        try:
            detalle_carrito_existente = DetalleCarrito.objects.get(
                carrito=carrito,
                producto=producto
            )
            cantidad_previa = detalle_carrito_existente.cantidad
            
            # Validar el cambio de cantidad
            cambio_stock = cantidad - cantidad_previa
            if inventario.stock - cambio_stock < 0:
                return Response(
                    {'error': f'No hay suficiente stock para el producto {producto.nombre}. Stock disponible: {inventario.stock + cantidad_previa} (ya tienes {cantidad_previa} en el carrito)'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Actualizar el DetalleCarrito existente
            detalle_carrito_existente.cantidad = cantidad
            detalle_carrito_existente.save()
            inventario.stock -= cambio_stock # Restar el cambio neto del stock
            inventario.save()
            detalle_carrito = detalle_carrito_existente
            created = False
        except DetalleCarrito.DoesNotExist:
            # Si el DetalleCarrito no existe, es un nuevo item en el carrito
            if inventario.stock - cantidad < 0:
                 return Response(
                    {'error': f'No hay suficiente stock para el producto {producto.nombre}. Stock disponible: {inventario.stock}'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            detalle_carrito = DetalleCarrito.objects.create(
                carrito=carrito,
                producto=producto,
                cantidad=cantidad
            )
            inventario.stock -= cantidad # Restar la cantidad completa del stock
            inventario.save()
            created = True

        serializer = self.get_serializer(detalle_carrito)
        return Response(serializer.data, status=status.HTTP_200_OK if not created else status.HTTP_201_CREATED)

    def destroy(self, request, *args, **kwargs):
        carrito_id = self.kwargs['carrito_pk']
        producto_sku = self.kwargs['producto__SKU'] # Usamos el lookup_field

        try:
            carrito = Carrito.objects.get(id=carrito_id)
            detalle_carrito = DetalleCarrito.objects.get(carrito=carrito, producto__SKU=producto_sku)
        except Carrito.DoesNotExist:
            return Response({'error': 'Carrito no encontrado.'}, status=status.HTTP_404_NOT_FOUND)
        except DetalleCarrito.DoesNotExist:
            return Response({'error': 'Detalle de carrito no encontrado con ese producto.'}, status=status.HTTP_404_NOT_FOUND)
        
        # Antes de eliminar el DetalleCarrito, devolver la cantidad al stock
        producto = detalle_carrito.producto
        try:
            inventario = producto.inventario
            inventario.stock += detalle_carrito.cantidad
            inventario.save()
        except Inventario.DoesNotExist:
            # Si no hay inventario, se registra o se maneja como un error, pero no bloquea la eliminación del detalle
            print(f"Advertencia: Producto {producto.SKU} sin registro de inventario al eliminar detalle.")

        self.perform_destroy(detalle_carrito)
        return Response(status=status.HTTP_204_NO_CONTENT)

