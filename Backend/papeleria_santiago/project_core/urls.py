from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Crear un router y registrar nuestros viewsets con él
router = DefaultRouter()
router.register(r'productos', views.ProductoViewSet, basename='producto')

urlpatterns = [
    path('pedidos/<int:pedido_id>/comprobante/pdf/', views.generar_factura_pdf, name='generar_factura_pdf'),
    path('api/', include(router.urls)),
]
