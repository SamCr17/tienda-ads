from django.urls import path
from .views import CompraView, CompraRapidaView, compra_rapida_fbv
from tienda_app.api.views import CompraAPIView, ProductosAPIView

urlpatterns = [
    # Usamos .as_view() para habilitar la CBV
    path('compra/<int:libro_id>/', CompraView.as_view(), name='finalizar_compra'),
    # Tutorial 01: versión spaghetti (referencia) y versión con Service Layer
    path('compra-rapida-fbv/<int:libro_id>/', compra_rapida_fbv, name='compra_rapida_fbv'),
    path('compra-rapida/<int:libro_id>/', CompraRapidaView.as_view(), name='compra_rapida'),
    # Tutorial 03: API REST
    path('api/v1/comprar/', CompraAPIView.as_view(), name='api_comprar'),
    # Tutorial 06: catalogo que sigue respondiendo el monolito (v1)
    path('api/v1/productos/', ProductosAPIView.as_view(), name='api_productos'),
]
