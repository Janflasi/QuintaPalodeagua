# reservas/views.py
from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from datetime import date
from calendar import HTMLCalendar
from .models import Reserva # Importamos el modelo Reserva
from .forms import ReservaForm # Importar el nuevo formulario

@login_required
def panel_usuario(request):
    # Buscamos todas las reservas que pertenecen al usuario actual
    # y las ordenamos por fecha de reserva de forma descendente.
    reservas = Reserva.objects.filter(usuario=request.user).order_by('-fecha_reserva')

    # Pasamos las reservas a la plantilla en el contexto
    contexto = {'reservas': reservas}
    return render(request, 'reservas/panel.html', contexto)

@login_required
def crear_reserva(request):
    if request.method == 'POST':
        form = ReservaForm(request.POST)
        if form.is_valid():
            reserva = form.save(commit=False)
            reserva.usuario = request.user
            reserva.save()
            messages.success(request, '¡Tu solicitud de reserva ha sido enviada! Recibirás una notificación cuando sea confirmada.')
            return redirect('panel_usuario')
    else:
        form = ReservaForm()

    return render(request, 'reservas/crear_reserva.html', {'form': form})

@login_required
def ver_disponibilidad(request):
    # Obtener todas las fechas con reservas confirmadas
    fechas_ocupadas = Reserva.objects.filter(estado='confirmada').values_list('fecha_reserva', flat=True)

    # Crear un calendario HTML para el mes actual
    cal = HTMLCalendar().formatmonth(date.today().year, date.today().month)

    # Resaltar los días ocupados en el HTML del calendario
    for fecha in fechas_ocupadas:
        # Formateamos el día como ' 1 ', ' 2 ', ... ' 31 ' para buscarlo en el string
        dia_a_buscar = f'>{fecha.day}<'
        clase_a_reemplazar = f' class="ocupado">{fecha.day}<'
        cal = cal.replace(dia_a_buscar, clase_a_reemplazar)

    contexto = {'calendario': cal}
    return render(request, 'reservas/disponibilidad.html', contexto)