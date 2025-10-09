# reservas/signals.py

from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User

from .models import Reserva
from notificaciones.models import Notificacion
from contabilidad.models import Movimiento


# --- SEÑAL #1: Se activa CUANDO SE ACTUALIZA una reserva (para notificar al CLIENTE) ---
@receiver(pre_save, sender=Reserva)
def notificar_cambio_estado_reserva(sender, instance, **kwargs):
    if not instance.pk:
        return

    try:
        reserva_anterior = Reserva.objects.get(pk=instance.pk)
    except Reserva.DoesNotExist:
        return

    estado_anterior = reserva_anterior.estado
    estado_nuevo = instance.estado

    # Cuando el admin cambia de 'Pendiente' a 'Esperando Pago'
    if estado_anterior == 'pendiente' and estado_nuevo == 'esperando_pago':
        user = instance.usuario
        subject = 'Tu Reserva en Quinta Palo de Agua está Pre-Aprobada'
        html_message = render_to_string('emails/confirmacion_reserva.html', {'reserva': instance})
        
        send_mail(subject, '', None, [user.email], html_message=html_message)
        
        mensaje_notificacion = f"¡Tu reserva para el {instance.fecha_reserva.strftime('%d/%m/%Y')} fue pre-aprobada!"
        Notificacion.objects.create(usuario=user, mensaje=mensaje_notificacion, url="#")
        
        instance.fecha_esperando_pago = timezone.now()

    # Cuando el admin pasa la reserva a 'Confirmada' (después del pago)
    if estado_nuevo == 'confirmada' and estado_anterior != 'confirmada':
         # Si la reserva tiene un precio, crea el movimiento de ingreso
        if instance.precio > 0:
            # Evita crear duplicados si ya existe un movimiento para esta reserva
            if not Movimiento.objects.filter(reserva_asociada=instance).exists():
                Movimiento.objects.create(
                    tipo='ingreso',
                    monto=instance.precio,
                    descripcion=f"Ingreso por reserva confirmada para '{instance.usuario.username}'",
                    reserva_asociada=instance,
                    usuario=instance.usuario
                )


# --- SEÑAL #2: Se activa CUANDO SE CREA una reserva nueva (para notificar al ADMIN) ---
@receiver(post_save, sender=Reserva)
def notificar_admin_nueva_reserva(sender, instance, created, **kwargs):
    """
    Si la reserva es nueva (created=True), busca a todos los administradores
    y les crea una notificación en el sistema.
    """
    if created:
        admins = User.objects.filter(is_staff=True)
        mensaje = f"Nueva solicitud de reserva de {instance.usuario.username} para el {instance.fecha_reserva.strftime('%d/%m/%Y')}."
        url_notificacion = reverse('lista_reservas_admin')

        for admin in admins:
            Notificacion.objects.create(
                usuario=admin,
                mensaje=mensaje,
                url=url_notificacion
            )