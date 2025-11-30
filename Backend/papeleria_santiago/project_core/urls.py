from django.urls import path
from . import views

urlpatterns = [
    path('pedidos/<int:pedido_id>/comprobante/pdf/', views.generar_factura_pdf, name='generar_factura_pdf'),
]
