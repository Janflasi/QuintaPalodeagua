from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Foto
from .forms import FotoForm

# --- VISTA PÚBLICA ---
def galeria(request):
    """
    Muestra la galería pública a todos los visitantes.
    """
    fotos = Foto.objects.all().order_by('-id')
    return render(request, 'galeria/galeria.html', {'fotos': fotos})


# --- VISTAS PARA EL PANEL DE ADMINISTRADOR ---

@login_required
def gestionar_galeria_admin(request):
    """
    Muestra todas las fotos al admin para que pueda subirlas y eliminarlas.
    """
    if not request.user.is_staff:
        return redirect('index')

    if request.method == 'POST':
        form = FotoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'La foto ha sido subida correctamente.')
            return redirect('gestionar_galeria_admin')
    else:
        form = FotoForm()

    fotos = Foto.objects.all().order_by('-id')
    return render(request, 'panel_admin/admin_gestionar_galeria.html', {'fotos': fotos, 'form': form})


@login_required
def eliminar_foto_admin(request, foto_id):
    """
    Elimina una foto específica.
    """
    if not request.user.is_staff or request.method != 'POST':
        return redirect('index')

    try:
        foto = Foto.objects.get(id=foto_id)
        foto.delete()
        messages.success(request, 'La foto ha sido eliminada.')
    except Foto.DoesNotExist:
        messages.error(request, 'La foto que intentas eliminar no existe.')
    
    return redirect('gestionar_galeria_admin')


@login_required
def galeria_panel_usuario(request):
    """
    Muestra la galería DENTRO del panel de usuario, con el menú lateral.
    """
    fotos = Foto.objects.all().order_by('-id')
    # Esta vista siempre usa la plantilla que tiene el sidebar.
    return render(request, 'galeria/panel_galeria.html', {'fotos': fotos})