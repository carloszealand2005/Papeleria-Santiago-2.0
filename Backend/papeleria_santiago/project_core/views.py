from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.template.loader import get_template
from io import BytesIO
from xhtml2pdf import pisa
from .models import Comprobante, Pedido # Importamos el modelo Comprobante


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

