from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Reserva(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    fecha_reserva = models.DateField()
    numero_personas = models.PositiveIntegerField()
    tipo_evento = models.CharField(max_length=100)
    estado = models.CharField(max_length=20, choices=[
        ('pendiente', 'Pendiente'),
        ('confirmada', 'Confirmada'),
        ('cancelada', 'Cancelada'),
    ], default='pendiente')
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Reserva de {self.usuario.username} para {self.fecha_reserva}'


class Resena(models.Model):
    reserva = models.OneToOneField(Reserva, on_delete=models.CASCADE, related_name='resena')
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    calificacion = models.PositiveIntegerField(choices=[(i, f'{i} estrellas') for i in range(1, 6)])
    comentario = models.TextField(max_length=500)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    aprobada = models.BooleanField(default=False)

    def __str__(self):
        return f'Reseña de {self.usuario.username} para la reserva del {self.reserva.fecha_reserva}'

    class Meta:
        ordering = ['-fecha_creacion']