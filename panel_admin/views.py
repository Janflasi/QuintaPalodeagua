# panel_admin/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages
from reservas.models import Reserva
from django.contrib.auth.models import User

# Importaciones clave para enviar correos
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings

# -------------------
# FUNCIÓN DE AYUDA
# -------------------

def es_admin(user):
    """
    Verifica si un usuario tiene permisos de administrador (staff o superuser).
    Se usa para proteger las vistas de este panel.
    """
    return user.is_staff or user.is_superuser

def enviar_correo_notificacion(reserva):
    """
    Prepara y envía un correo electrónico al usuario sobre el estado de su reserva.
    """
    if not reserva.usuario.email:
        # Si el usuario no tiene correo, no se puede enviar nada.
        return

    asunto = f'Actualización de tu reserva en Quinta Palo de Agua para el {reserva.fecha_reserva.strftime("%d/%m/%Y")}'
    
    contexto = {'reserva': reserva}
    html_mensaje = render_to_string('emails/notificacion_reserva.html', contexto)
    mensaje_plano = strip_tags(html_mensaje)
    
    send_mail(
        asunto,
        mensaje_plano,
        settings.EMAIL_HOST_USER, # Correo configurado en settings.py
        [reserva.usuario.email],  # Lista de destinatarios
        html_message=html_mensaje
    )

# -------------------
# VISTAS DEL PANEL
# -------------------

@user_passes_test(es_admin)
def dashboard(request):
    """
    Muestra la página principal del panel de admin con estadísticas clave.
    """
    reservas_pendientes = Reserva.objects.filter(estado='pendiente').count()
    reservas_confirmadas = Reserva.objects.filter(estado='confirmada').count()
    total_usuarios = User.objects.filter(is_staff=False).count()

    contexto = {
        'reservas_pendientes': reservas_pendientes,
        'reservas_confirmadas': reservas_confirmadas,
        'total_usuarios': total_usuarios,
    }
    return render(request, 'panel_admin/dashboard.html', contexto)

@user_passes_test(es_admin)
def gestionar_reservas(request):
    """
    Muestra una tabla con todas las reservas para que el admin las gestione.
    """
    lista_reservas = Reserva.objects.all().order_by('-fecha_creacion')
    contexto = {'reservas': lista_reservas}
    return render(request, 'panel_admin/gestionar_reservas.html', contexto)

@user_passes_test(es_admin)
def ver_usuarios(request):
    """
    Muestra una lista de todos los clientes registrados (no administradores).
    """
    clientes = User.objects.filter(is_staff=False).order_by('-date_joined')
    contexto = {'clientes': clientes}
    return render(request, 'panel_admin/ver_usuarios.html', contexto)

# -------------------
# VISTAS DE ACCIONES
# -------------------

@user_passes_test(es_admin)
def confirmar_reserva(request, reserva_id):
    """
    Cambia el estado de una reserva a 'confirmada' y notifica al cliente.
    """
    reserva = get_object_or_404(Reserva, id=reserva_id)
    reserva.estado = 'confirmada'
    reserva.save()
    
    try:
        enviar_correo_notificacion(reserva)
        messages.success(request, f"La reserva de {reserva.usuario.username} ha sido CONFIRMADA y el cliente ha sido notificado.")
    except Exception as e:
        messages.error(request, f"La reserva fue confirmada, pero hubo un error al enviar el correo: {e}")

    return redirect('admin_gestionar_reservas')

@user_passes_test(es_admin)
def cancelar_reserva(request, reserva_id):
    """
    Cambia el estado de una reserva a 'cancelada' y notifica al cliente.
    """
    reserva = get_object_or_404(Reserva, id=reserva_id)
    reserva.estado = 'cancelada'
    reserva.save()

    try:
        enviar_correo_notificacion(reserva)
        messages.success(request, f"La reserva de {reserva.usuario.username} ha sido CANCELADA y el cliente ha sido notificado.")
    except Exception as e:
        messages.error(request, f"La reserva fue cancelada, pero hubo un error al enviar el correo: {e}")

    return redirect('admin_gestionar_reservas')