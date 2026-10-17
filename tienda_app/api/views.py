from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, status
from tienda_app.models import Libro
from .serializers import LibroSerializer, OrdenInputSerializer
from tienda_app.services import CompraService # <--- REUTILIZACION
from tienda_app.infra.factories import PaymentFactory

class CompraAPIView(APIView):
    """
    Endpoint para procesar compras via JSON.
    POST /api/v1/comprar/
    Payload: { "libro_id": 1, "direccion_envio": "Calle 123" }
    """

    def post(self, request):
        # 1. Validacion de datos de entrada (Adapter)
        serializer = OrdenInputSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        datos = serializer.validated_data

        try:
            # 2. Inyeccion de Dependencias (Factory)
            gateway = PaymentFactory.get_processor()

            # 3. Ejecucion de Logica de Negocio (Service Layer)
            servicio = CompraService(procesador_pago=gateway)
            # Noten como el servicio NO cambia, solo cambia quien lo llama.
            resultado = servicio.ejecutar_compra(
                libro_id=datos['libro_id'],
                direccion=datos['direccion_envio'],
                # Sin sesion iniciada, request.user es AnonymousUser y no puede
                # guardarse en la Orden: en ese caso la orden queda sin usuario.
                usuario=request.user if request.user.is_authenticated else None
            )

            return Response({
                "estado": "exito",
                "mensaje": f"Orden creada. Total: {resultado}"
            }, status=status.HTTP_201_CREATED)

        except ValueError as e:
            # Errores de negocio (ej: Sin stock)
            return Response({"error": str(e)}, status=status.HTTP_409_CONFLICT)
        except Exception as e:
            # Errores inesperados
            return Response({"error": "Error interno"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ProductosAPIView(generics.ListAPIView):
    """
    Catalogo de libros con su stock (monolito Django, v1).
    GET /api/v1/productos/
    """
    queryset = Libro.objects.all().order_by('id')
    serializer_class = LibroSerializer
