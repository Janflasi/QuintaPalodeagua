# reservas/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import Reserva
from .forms import ReservaForm

from datetime import date
from calendar import HTMLCalendar
import locale

try:
    locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')
except locale.Error:
    locale.setlocale(locale.LC_TIME, 'Spanish_Spain')

class ReservaCalendar(HTMLCalendar):
    def __init__(self, fechas_ocupadas):
        super().__init__()
        self.fechas_ocupadas = fechas_ocupadas

    def formatday(self, day, weekday):
        if day == 0:
            return '<td class="noday">&nbsp;</td>'

        cssclass = self.cssclasses[weekday]
        current_date = date(self.year, self.month, day)
        
        if current_date in self.fechas_ocupadas:
            cssclass += ' ocupado'
        
        return f'<td class="{cssclass}">{day}</td>'

    def formatmonth(self, theyear, themonth, withyear=True):
        self.year, self.month = theyear, themonth
        return super().formatmonth(theyear, themonth, withyear)

@login_required
def panel_usuario(request):
    reservas = Reserva.objects.filter(usuario=request.user).order_by('-fecha_reserva')
    contexto = {'reservas': reservas}
    return render(request, 'reservas/panel.html', contexto)

@login_required
def crear_reserva(request):
    if request.method == 'POST':
        form = ReservaForm(request.POST)
        if form.is_valid():
            fecha_solicitada = form.cleaned_data['fecha_reserva']
            # --- CORRECCIÓN CLAVE 1 ---
            if Reserva.objects.filter(fecha_reserva=fecha_solicitada, estado__contains='confirmada').exists():
                messages.error(request, 'La fecha seleccionada ya no está disponible. Por favor, elige otra.')
            else:
                reserva = form.save(commit=False)
                reserva.usuario = request.user
                reserva.save()
                messages.success(request, '¡Tu solicitud de reserva ha sido enviada!')
                return redirect('panel_usuario')
    else:
        form = ReservaForm()
    
    return render(request, 'reservas/crear_reserva.html', {'form': form})

@login_required
def ver_disponibilidad(request, year=None, month=None):
    if year is None or month is None:
        today = timezone.now()
        year, month = today.year, today.month
    else:
        year, month = int(year), int(month)

    last_month = date(year, month, 1) - timezone.timedelta(days=1)
    next_month = date(year, month, 28) + timezone.timedelta(days=4)
    
    # --- CORRECCIÓN CLAVE 2 ---
    # Usamos __contains para ignorar espacios y encontrar la palabra 'confirmada'
    fechas_ocupadas = set(Reserva.objects.filter(
        estado__contains='confirmada'
    ).values_list('fecha_reserva', flat=True))
    
    cal = ReservaCalendar(fechas_ocupadas).formatmonth(year, month)
    
    nombre_mes = date(year, month, 1).strftime('%B').capitalize()
    ano_actual = timezone.now().year
    rango_anios = range(ano_actual, ano_actual + 3)

    contexto = {
        'calendario': cal,
        'nombre_mes': nombre_mes,
        'ano_actual': year,
        'mes_actual': month,
        'mes_anterior': last_month,
        'mes_siguiente': next_month,
        'rango_anios': rango_anios,
    }
    return render(request, 'reservas/disponibilidad.html', contexto)