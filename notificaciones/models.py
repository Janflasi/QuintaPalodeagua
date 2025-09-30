# notificaciones/models.py
from django.db import models
from django.contrib.auth.models import User

class Notificacion(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    mensaje = models.CharField(max_length=255)
    leida = models.BooleanField(default=False)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    url = models.URLField(blank=True, null=True) # Enlace para redirigir al usuario

    def __str__(self):
        return self.mensaje

    class Meta:
        ordering = ['-fecha_creacion']