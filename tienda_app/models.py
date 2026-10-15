from django.conf import settings
from django.db import models

class Libro(models.Model):
    titulo = models.CharField(max_length=200)
    precio = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.titulo

    @property
    def stock_actual(self):
        # Tutorial 03: campo calculado que expone el LibroSerializer
        inventario = Inventario.objects.filter(libro=self).first()
        return inventario.cantidad if inventario else 0

class Inventario(models.Model):
    libro = models.OneToOneField(Libro, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()

class Orden(models.Model):
    # Tutorial 02: el OrdenBuilder arma ordenes de varios productos,
    # por eso el libro deja de ser obligatorio.
    libro = models.ForeignKey(Libro, null=True, blank=True, on_delete=models.CASCADE)
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL
    )
    total = models.DecimalField(max_digits=10, decimal_places=2)
    direccion_envio = models.CharField(max_length=200, blank=True, default="")
    fecha_creacion = models.DateTimeField(auto_now_add=True)
