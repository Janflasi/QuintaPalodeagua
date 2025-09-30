from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Reserva
from .forms import ReservaForm
from django.contrib.auth.models import User
import calendar
from datetime import date
from django.utils import timezone
from django.http import JsonResponse
from django.urls import reverse

# ---------------- VISTAS PARA USUARIOS REGULARES ----------------

@login_required
def panel_usuario(request):
    """
    Muestra al usuario regular su historial de reservas.
    """
    reservas = Reserva.objects.filter(usuario=request.user).order_by('-fecha_reserva')
    return render(request, 'reservas/panel.html', {'reservas': reservas})


@login_required
def crear_reserva(request):
    """
    Maneja la creación de una nueva solicitud de reserva.
    Ahora responde a peticiones AJAX.
    """
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'

    if request.method == 'POST':
        form = ReservaForm(request.POST)
        if form.is_valid():
            reserva = form.save(commit=False)
            reserva.usuario = request.user
            reserva.save()
            
            if is_ajax:
                return JsonResponse({
                    'success': True,
                    'message': '¡Tu solicitud de reserva ha sido enviada con éxito!',
                    'redirect_url': reverse('panel_usuario')
                })
            
            messages.success(request, '¡Tu solicitud de reserva ha sido enviada con éxito!')
            return redirect('panel_usuario')
        else:
            if is_ajax:
                return JsonResponse({'success': False, 'errors': form.errors})
    else:
        form = ReservaForm()
    
    return render(request, 'reservas/crear_reserva.html', {'form': form})


def ver_disponibilidad(request, year=None, month=None):
    """
    Muestra un calendario de disponibilidad dinámico y navegable.
    """
    if year is None or month is None:
        today = timezone.now()
        year = today.year
        month = today.month
    
    fechas_ocupadas = Reserva.objects.filter(estado='confirmada').values_list('fecha_reserva', flat=True)
    
    cal = calendar.Calendar()
    dias_del_mes = cal.monthdatescalendar(year, month)

    current_date = date(year, month, 1)
    
    prev_month_date = current_date - timezone.timedelta(days=1)
    prev_month_year = prev_month_date.year
    prev_month = prev_month_date.month

    next_month_date = current_date.replace(day=28) + timezone.timedelta(days=4)
    next_month_year = next_month_date.year
    next_month = next_month_date.month

    nombre_mes = calendar.month_name[month].capitalize()

    context = {
        'year': year,
        'month': month,
        'nombre_mes': nombre_mes,
        'semanas': dias_del_mes,
        'fechas_ocupadas': fechas_ocupadas,
        'hoy': timezone.now().date(),
        'prev_month': prev_month,
        'prev_month_year': prev_month_year,
        'next_month': next_month,
        'next_month_year': next_month_year,
    }
    
    return render(request, 'reservas/disponibilidad.html', context)


@login_required
def cancelar_reserva_usuario(request, reserva_id):
    """
    Permite a un usuario cancelar su propia solicitud de reserva si está pendiente.
    """
    if request.method != 'POST':
        return redirect('panel_usuario')

    try:
        reserva = Reserva.objects.get(id=reserva_id, usuario=request.user)
        if reserva.estado == 'pendiente':
            reserva.estado = 'cancelada'
            reserva.save()
            messages.success(request, "Tu solicitud de reserva ha sido cancelada.")
        else:
            messages.error(request, "No puedes cancelar esta reserva porque ya ha sido procesada.")
    except Reserva.DoesNotExist:
        messages.error(request, "La reserva que intentas cancelar no existe.")

    return redirect('panel_usuario')


# ---------------- VISTAS PARA EL PANEL DEL ADMINISTRADOR ----------------

@login_required
def dashboard_admin(request):
    """
    Muestra la página principal del panel de control personalizado del administrador.
    """
    if not request.user.is_staff:
        return redirect('index')

    total_usuarios = User.objects.count()
    reservas_pendientes = Reserva.objects.filter(estado='pendiente').count()
    reservas_confirmadas = Reserva.objects.filter(estado='confirmada').count()

    context = {
        'total_usuarios': total_usuarios,
        'reservas_pendientes': reservas_pendientes,
        'reservas_confirmadas': reservas_confirmadas,
    }
    return render(request, 'panel_admin/admin_dashboard.html', context)


@login_required
def lista_reservas_admin(request):
    """
    Muestra al admin una lista de TODAS las reservas para gestionarlas.
    """
    if not request.user.is_staff:
        return redirect('index')

    filtro_estado = request.GET.get('estado', '')
    if filtro_estado in ['pendiente', 'confirmada', 'cancelada']:
        lista_reservas = Reserva.objects.filter(estado=filtro_estado).order_by('-fecha_creacion')
    else:
        lista_reservas = Reserva.objects.all().order_by('-fecha_creacion')

    return render(request, 'panel_admin/admin_lista_reservas.html', {
        'reservas': lista_reservas,
        'filtro_actual': filtro_estado
    })


@login_required
def actualizar_estado_reserva(request, reserva_id):
    """
    Actualiza el estado de una reserva específica (Confirmada o Cancelada).
    """
    if not request.user.is_staff or request.method != 'POST':
        return redirect('index')

    nuevo_estado = request.POST.get('estado')
    if nuevo_estado not in ['confirmada', 'cancelada']:
        messages.error(request, "Estado no válido.")
        return redirect('lista_reservas_admin')

    try:
        reserva = Reserva.objects.get(id=reserva_id)
        reserva.estado = nuevo_estado
        reserva.save()
        messages.success(request, f"La reserva para {reserva.usuario.username} ha sido actualizada a '{nuevo_estado}'.")
    except Reserva.DoesNotExist:
        messages.error(request, "La reserva no existe.")
    
    return redirect('lista_reservas_admin')


@login_required
def editar_reserva_admin(request, reserva_id):
    """
    Permite al admin editar los detalles completos de una reserva existente.
    """
    if not request.user.is_staff:
        return redirect('index')

    try:
        reserva = Reserva.objects.get(id=reserva_id)
    except Reserva.DoesNotExist:
        messages.error(request, "La reserva que intentas editar no existe.")
        return redirect('lista_reservas_admin')

    if request.method == 'POST':
        form = ReservaForm(request.POST, instance=reserva)
        if form.is_valid():
            form.save()
            messages.success(request, f"La reserva de {reserva.usuario.username} ha sido actualizada.")
            return redirect('lista_reservas_admin')
    else:
        form = ReservaForm(instance=reserva)

    return render(request, 'panel_admin/admin_editar_reserva.html', {
        'form': form,
        'reserva': reserva
    })