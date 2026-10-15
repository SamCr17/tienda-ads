from rest_framework import serializers
from tienda_app.models import Libro, Orden

class LibroSerializer(serializers.ModelSerializer):
    class Meta:
        model = Libro
        fields = ['id', 'titulo', 'precio', 'stock_actual']
        # Nota: 'stock_actual' puede ser un campo calculado o propiedad del modelo

class OrdenInputSerializer(serializers.Serializer):
    """
    Serializer para VALIDAR la entrada de datos, no necesariamente ligado a un modelo.
    Actua como un DTO (Data Transfer Object).
    """
    libro_id = serializers.IntegerField()
    direccion_envio = serializers.CharField(max_length=200)
    # Validaciones extras aqui si fueran necesarias
