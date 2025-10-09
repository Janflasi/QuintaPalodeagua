# contabilidad/signals.py

from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Venta, Movimiento

@receiver(post_save, sender=Venta)
def crear_movimiento_por_venta(sender, instance, created, **kwargs):
    """
    Cuando se crea una nueva Venta, crea automáticamente un Movimiento de tipo 'ingreso'.
    """
    if created:
        Movimiento.objects.create(
            tipo='ingreso',
            monto=instance.precio_total,
            descripcion=f'Ingreso por venta de: {instance.cantidad} x {instance.producto.nombre}',
            # El usuario que registra podría ser el admin que está logueado,
            # pero para una señal es más complejo. Lo dejamos simple por ahora.
        )