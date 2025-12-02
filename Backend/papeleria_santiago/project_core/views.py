from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.template.loader import get_template
from io import BytesIO
from xhtml2pdf import pisa
from .models import Comprobante, Pedido, Producto # Importamos Producto
from rest_framework import viewsets, filters # Importar filters
from django_filters.rest_framework import DjangoFilterBackend # Importar DjangoFilterBackend
from .serializers import ProductoSerializer # Importar el serializador

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
    filterset_fields = ['categoria', 'marca'] # Filtrar por categoría y marca
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
            
        return queryset

