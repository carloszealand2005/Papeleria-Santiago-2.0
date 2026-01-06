from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from .auth_views import RegistroView, LoginView # Importar la vista de registro y la vista de Login

# Crear un router y registrar nuestros viewsets con él
router = DefaultRouter()
router.register(r'productos', views.ProductoViewSet, basename='producto')
router.register(r'carritos', views.CarritoViewSet, basename='carrito') # Mantener si se necesitan rutas por ID de carrito
router.register(r'mi-carrito', views.MiCarritoViewSet, basename='mi-carrito') # Nuevo ViewSet para el carrito del usuario
router.register(r'mi-carrito-detalles', views.MiCarritoDetalleViewSet, basename='mi-carrito-detalle') # Nuevo ViewSet para los detalles del carrito del usuario
router.register(r'mis-pedidos', views.MisPedidosViewSet, basename='mis-pedidos')
router.register(r'favoritos', views.FavoritosClienteViewSet, basename='favorito')
router.register(r'subcategorias', views.SubcategoriaViewSet, basename='subcategoria')

urlpatterns = [
    path('pedidos/<int:pedido_id>/comprobante/pdf/', views.generar_factura_pdf, name='generar_factura_pdf'),
    path('api/mi-perfil/', views.MiPerfilAPIView.as_view(), name='mi_perfil'),
    path('api/autenticacion/registro/', RegistroView.as_view(), name='registro'),
    path('api/autenticacion/login/', LoginView.as_view(), name='login'),
    path('api/', include(router.urls)),
]
