from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Reserva(models.Model):
    # --- CAMPOS EXISTENTES ---
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reservas')
    fecha_reserva = models.DateField(verbose_name="Fecha del Evento")
    numero_personas = models.PositiveIntegerField(verbose_name="Número de Personas")
    tipo_evento = models.CharField(max_length=100, verbose_name="Tipo de Evento")
    
    # --- SISTEMA DE ESTADO MEJORADO ---
    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('esperando_pago', 'Esperando Pago'), # Nuevo estado
        ('confirmada', 'Confirmada'),
        ('cancelada', 'Cancelada'),
    ]
    estado = models.CharField(max_length=15, choices=ESTADO_CHOICES, default='pendiente')
    
    # --- NUEVOS CAMPOS DETALLADOS ---
    precio = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name="Precio de la Reserva")
    hora_ingreso = models.TimeField(null=True, blank=True, verbose_name="Hora de Ingreso")
    hora_salida = models.TimeField(null=True, blank=True, verbose_name="Hora de Salida")
    detalles_privilegios = models.TextField(blank=True, verbose_name="Privilegios Incluidos", help_text="Ej: Acceso a piscina, 2 habitaciones, uso de la cocina.")
    penalizacion_tardia = models.DecimalField(max_digits=10, decimal_places=2, default=50000.00, verbose_name="Penalización por Hora Extra")
    
    # --- CAMPO PARA LA REGLA DE LAS 24 HORAS ---
    fecha_esperando_pago = models.DateTimeField(null=True, blank=True, editable=False)

    def __str__(self):
        return f"Reserva de {self.usuario.username} para el {self.fecha_reserva}"

    class Meta:
        ordering = ['-fecha_reserva']

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