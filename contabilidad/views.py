# contabilidad/views.py

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum
from .models import Movimiento, Producto, Venta
from .forms import MovimientoForm, ProductoForm, VentaForm

# La vista dashboard_contabilidad se queda igual que antes...
@login_required
def dashboard_contabilidad(request):
    """
    Vista principal de contabilidad. Muestra un resumen financiero
    y una lista de los últimos movimientos.
    """
    if not request.user.is_staff:
        return redirect('index')
    
    ingresos = Movimiento.objects.filter(tipo='ingreso').aggregate(total=Sum('monto'))['total'] or 0
    egresos = Movimiento.objects.filter(tipo='egreso').aggregate(total=Sum('monto'))['total'] or 0
    balance = ingresos - egresos
    ultimos_movimientos = Movimiento.objects.all()[:10]

    context = {
        'ingresos': ingresos, 'egresos': egresos, 'balance': balance, 'ultimos_movimientos': ultimos_movimientos,
    }
    return render(request, 'panel_admin/contabilidad/dashboard.html', context)


# --- REEMPLAZA ESTA VISTA COMPLETA ---
@login_required
def gestionar_inventario(request):
    """
    Vista para ver el inventario y procesar los formularios de
    nuevos productos y registro de ventas.
    """
    if not request.user.is_staff:
        return redirect('index')

    if request.method == 'POST':
        # Identificamos qué formulario se envió usando el nombre del botón de submit
        if 'submit_venta' in request.POST:
            venta_form = VentaForm(request.POST)
            if venta_form.is_valid():
                venta = venta_form.save(commit=False)
                # Verificamos si hay stock suficiente
                if venta.producto.stock_actual >= venta.cantidad:
                    # Actualizamos el stock del producto
                    venta.producto.stock_actual -= venta.cantidad
                    venta.producto.save()
                    venta.save()
                    messages.success(request, f'Venta de {venta.cantidad} x {venta.producto.nombre} registrada correctamente.')
                else:
                    messages.error(request, f'No hay stock suficiente para vender {venta.cantidad} de {venta.producto.nombre}. Stock actual: {venta.producto.stock_actual}.')
            return redirect('gestionar_inventario')

        elif 'submit_producto' in request.POST:
            producto_form = ProductoForm(request.POST)
            if producto_form.is_valid():
                producto_form.save()
                messages.success(request, 'Producto añadido al inventario correctamente.')
            return redirect('gestionar_inventario')

    # Si el método es GET, simplemente mostramos la página con los formularios vacíos
    productos = Producto.objects.all()
    ultimas_ventas = Venta.objects.all()[:10]
    venta_form = VentaForm()
    producto_form = ProductoForm()

    context = {
        'productos': productos,
        'ultimas_ventas': ultimas_ventas,
        'venta_form': venta_form,
        'producto_form': producto_form,
    }
    return render(request, 'panel_admin/contabilidad/inventario.html', context)
@login_required
def crear_movimiento(request, tipo_movimiento):
    """
    Vista para crear un nuevo Movimiento (Ingreso o Egreso).
    """
    if not request.user.is_staff:
        return redirect('index')

    if tipo_movimiento not in ['ingreso', 'egreso']:
        messages.error(request, 'Tipo de movimiento no válido.')
        return redirect('contabilidad:dashboard_contabilidad')

    if request.method == 'POST':
        form = MovimientoForm(request.POST)
        if form.is_valid():
            movimiento = form.save(commit=False)
            movimiento.usuario = request.user
            movimiento.save()
            messages.success(request, f'{movimiento.get_tipo_display()} registrado correctamente.')
            return redirect('contabilidad:dashboard_contabilidad')
    else:
        # Pre-llenamos el campo 'tipo' según la URL
        form = MovimientoForm(initial={'tipo': tipo_movimiento})

    context = {
        'form': form,
        'tipo_movimiento': tipo_movimiento.capitalize(),
    }
    return render(request, 'panel_admin/contabilidad/crear_movimiento.html', context)