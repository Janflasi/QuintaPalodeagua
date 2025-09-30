from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import CustomUserCreationForm, UserUpdateForm, PerfilUpdateForm

# ---------------- VISTAS PARA USUARIOS FINALES ----------------

def registro(request):
    """
    Maneja el registro de nuevos usuarios.
    """
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'¡Cuenta creada para {username}! Ahora, por favor, inicia sesión.')
            return redirect('login')
    else:
        form = CustomUserCreationForm()

    return render(request, 'usuarios/registro.html', {'form': form})


@login_required
def perfil(request):
    """
    Muestra la página de perfil del usuario que ha iniciado sesión.
    """
    return render(request, 'usuarios/perfil.html')


@login_required
def editar_perfil(request):
    """
    Maneja la edición de los datos de la cuenta (User) y del perfil (Perfil).
    """
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = PerfilUpdateForm(request.POST, instance=request.user.perfil)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, '¡Tu perfil ha sido actualizado correctamente!')
            return redirect('perfil')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = PerfilUpdateForm(instance=request.user.perfil)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'usuarios/editar_perfil.html', context)


# ---------------- VISTAS DE LÓGICA Y REDIRECCIÓN ----------------

@login_required
def login_redirect_view(request):
    """
    Redirige a los usuarios a su panel correspondiente después de iniciar sesión.
    """
    if request.user.is_staff:
        # Si es admin o staff, va al NUEVO dashboard personalizado
        return redirect('dashboard_admin')
    else:
        # Si es un usuario normal, va a su panel de reservas
        return redirect('panel_usuario')


# ---------------- VISTAS PARA EL PANEL DEL ADMINISTRADOR ----------------

@login_required
def lista_usuarios_admin(request):
    """
    Muestra al administrador una lista de todos los usuarios registrados.
    """
    if not request.user.is_staff:
        return redirect('index')

    usuarios = User.objects.all().order_by('username')
    # Apunta a la nueva ubicación de la plantilla en la carpeta 'panel_admin'
    return render(request, 'panel_admin/admin_lista_usuarios.html', {'usuarios': usuarios})


@login_required
def activar_desactivar_usuario(request, user_id):
    """
    Cambia el estado (activo/inactivo) de un usuario específico.
    """
    if not request.user.is_staff or request.method != 'POST':
        return redirect('index')

    try:
        usuario_a_modificar = User.objects.get(id=user_id)
        usuario_a_modificar.is_active = not usuario_a_modificar.is_active
        usuario_a_modificar.save()
        messages.success(request, f"El estado del usuario {usuario_a_modificar.username} ha sido actualizado.")
    except User.DoesNotExist:
        messages.error(request, "El usuario no existe.")

    return redirect('lista_usuarios_admin')