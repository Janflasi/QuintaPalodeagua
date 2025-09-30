# reservas/signals.py
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from django.urls import reverse
from .models import Reserva
from notificaciones.models import Notificacion # <-- Importa el modelo de notificación
from django.contrib.auth.models import User

# --- SEÑAL PARA NOTIFICAR AL CLIENTE (CUANDO EL ADMIN CAMBIA EL ESTADO) ---
@receiver(pre_save, sender=Reserva)
def notificar_cambio_estado_reserva(sender, instance, **kwargs):
    if instance.pk:
        try:
            reserva_anterior = Reserva.objects.get(pk=instance.pk)
        except Reserva.DoesNotExist:
            return

        estado_anterior = reserva_anterior.estado
        estado_nuevo = instance.estado
        
        if estado_anterior == 'pendiente' and estado_anterior != estado_nuevo:
            user = instance.usuario
            subject = ''
            html_message = ''
            mensaje_notificacion = ''
            url_notificacion = reverse('panel_usuario') # Enlace al panel del usuario

            if estado_nuevo == 'confirmada':
                subject = '¡Tu Reserva en Quinta Palo de Agua ha sido Confirmada!'
                html_message = render_to_string('emails/confirmacion_reserva.html', {'reserva': instance, 'user': user})
                mensaje_notificacion = f"¡Buenas noticias! Tu reserva para el {instance.fecha_reserva.strftime('%d/%m/%Y')} ha sido confirmada."
            
            elif estado_nuevo == 'cancelada':
                subject = 'Actualización sobre tu Reserva en Quinta Palo de Agua'
                html_message = render_to_string('emails/rechazo_reserva.html', {'reserva': instance, 'user': user})
                mensaje_notificacion = f"Tu reserva para el {instance.fecha_reserva.strftime('%d/%m/%Y')} fue rechazada."

            if subject and user.email:
                # 1. Enviar el correo (como ya lo hacíamos)
                send_mail(subject, '', settings.DEFAULT_FROM_EMAIL, [user.email], html_message=html_message)
            
            if mensaje_notificacion:
                # 2. Crear la notificación en el sistema para el cliente
                Notificacion.objects.create(
                    usuario=user, 
                    mensaje=mensaje_notificacion,
                    url=url_notificacion
                )


# --- SEÑAL PARA NOTIFICAR AL ADMIN (CUANDO UN CLIENTE CREA UNA RESERVA) ---
@receiver(post_save, sender=Reserva)
def notificar_admin_nueva_reserva(sender, instance, created, **kwargs):
    if created: # Si la reserva es nueva
        # Buscar a todos los administradores
        admins = User.objects.filter(is_staff=True)
        mensaje = f"Nueva solicitud de reserva de {instance.usuario.username} para el {instance.fecha_reserva.strftime('%d/%m/%Y')}."
        url_notificacion = reverse('lista_reservas_admin') # Enlace a la lista de reservas del panel

        # Crear una notificación para cada administrador
        for admin in admins:
            Notificacion.objects.create(
                usuario=admin,
                mensaje=mensaje,
                url=url_notificacion
            )