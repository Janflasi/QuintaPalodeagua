# notificaciones/views.py
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Notificacion

@login_required
def ver_notificaciones(request):
    """
    Devuelve las notificaciones no leídas del usuario en formato JSON.
    """
    notificaciones = Notificacion.objects.filter(usuario=request.user, leida=False)
    
    data = {
        'count': notificaciones.count(),
        'notificaciones': [
            {
                'id': n.id,
                'mensaje': n.mensaje,
                'url': n.url,
                'fecha': n.fecha_creacion.strftime('%d %b %Y, %H:%M')
            } for n in notificaciones
        ]
    }
    return JsonResponse(data)


@login_required
def marcar_notificacion_leida(request, notificacion_id):
    """
    Marca una notificación como leída y redirige a su URL.
    """
    try:
        notificacion = Notificacion.objects.get(id=notificacion_id, usuario=request.user)
        notificacion.leida = True
        notificacion.save()

        if notificacion.url:
            return redirect(notificacion.url)
        else:
            # Si no hay URL, redirigir al panel correspondiente
            if request.user.is_staff:
                return redirect('dashboard_admin')
            else:
                return redirect('panel_usuario')

    except Notificacion.DoesNotExist:
        # Manejar el caso en que la notificación no exista o no pertenezca al usuario
        if request.user.is_staff:
            return redirect('dashboard_admin')
        else:
            return redirect('panel_usuario')