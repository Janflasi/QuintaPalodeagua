# reservas/models.py
from django.db import models
from django.contrib.auth.models import User
from django.core.mail import send_mail # Importar para enviar correos

class Reserva(models.Model):
    # ... (tus campos existentes como usuario, fecha_reserva, etc.) ...
    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('confirmada', 'Confirmada'),
        ('cancelada', 'Cancelada'),
    ]

    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    fecha_reserva = models.DateField()
    numero_personas = models.PositiveIntegerField()
    tipo_evento = models.CharField(max_length=100)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='pendiente')
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    # --- NUEVOS CAMPOS ---
    precio_cotizado = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def calcular_precio(self):
        precio_por_persona = 50000
        total = self.numero_personas * precio_por_persona
        
        # Lógica de descuento: si son 20 personas o más
        if self.numero_personas >= 20:
            # Aplicamos un descuento (ej. un precio fijo o un porcentaje)
            # Aquí usamos el ejemplo de precio fijo de $500.000
            total_con_descuento = 500000
            # Asegurémonos de que el descuento realmente beneficie
            if total_con_descuento < total:
                return total_con_descuento
        
        return total

    def save(self, *args, **kwargs):
        # Cada vez que se guarde una reserva, calculamos su precio
        self.precio_cotizado = self.calcular_precio()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Reserva de {self.usuario.username} para el {self.fecha_reserva}"
    
class Pago(models.Model):
    ESTADO_PAGO = [
        ('pendiente', 'Pendiente'),
        ('pagado', 'Pagado'),
        ('reembolsado', 'Reembolsado'),
    ]
    METODO_PAGO = [
        ('transferencia', 'Transferencia'),
        ('efectivo', 'Efectivo'),
        ('otro', 'Otro'),
    ]

    reserva = models.OneToOneField(Reserva, on_delete=models.CASCADE)
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    estado = models.CharField(max_length=20, choices=ESTADO_PAGO, default='pendiente')
    metodo = models.CharField(max_length=20, choices=METODO_PAGO, default='transferencia')
    fecha_pago = models.DateTimeField(null=True, blank=True)
    comprobante = models.FileField(upload_to='comprobantes/', null=True, blank=True)

    def __str__(self):
        return f"Pago de {self.monto} para la {self.reserva}"