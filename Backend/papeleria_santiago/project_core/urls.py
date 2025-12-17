from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_nested.routers import NestedDefaultRouter
from . import views
from .auth_views import RegistroView, LoginView # Importar la vista de registro y la vista de Login

# Crear un router y registrar nuestros viewsets con él
router = DefaultRouter()
router.register(r'productos', views.ProductoViewSet, basename='producto')
router.register(r'carritos', views.CarritoViewSet, basename='carrito') # Registrar CarritoViewSet

# Crear un router anidado para DetalleCarrito dentro de Carrito
carrito_router = NestedDefaultRouter(router, r'carritos', lookup='carrito')
carrito_router.register(r'detalles', views.DetalleCarritoViewSet, basename='carrito-detalle')

urlpatterns = [
    path('pedidos/<int:pedido_id>/comprobante/pdf/', views.generar_factura_pdf, name='generar_factura_pdf'),
    path('api/autenticacion/registro/', RegistroView.as_view(), name='registro'), # Nueva URL para el registro
    path('api/autenticacion/login/', LoginView.as_view(), name='login'), # Nueva URL para el login
    path('api/', include(router.urls)),
    path('api/', include(carrito_router.urls)), # Incluir las URLs del router anidado
]
