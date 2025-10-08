from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import CustomUserCreationForm, UserUpdateForm, PerfilUpdateForm, AdminUserCreationForm

# --- Importaciones necesarias para el envío de correos de invitación ---
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes

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
        # Si es admin o staff, va al dashboard personalizado
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


@login_required
def crear_usuario_admin(request):
    """
    Permite al admin crear un nuevo usuario desde el panel de control.
    Al crearlo, se le envía un correo para que establezca su contraseña.
    """
    if not request.user.is_staff:
        return redirect('index')

    if request.method == 'POST':
        form = AdminUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_staff = form.cleaned_data.get('is_staff', False)
            user.set_unusable_password()  # Se crea sin contraseña válida
            user.save()

            # --- Lógica para enviar el correo de invitación ---
            current_site = get_current_site(request)
            mail_subject = '¡Bienvenido a Quinta Palo de Agua! Por favor, activa tu cuenta.'
            message = render_to_string('emails/password_reset_invitation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
                'protocol': 'https' if request.is_secure() else 'http',
            })
            
            send_mail(mail_subject, message, None, [user.email])
            # --- Fin de la lógica de correo ---

            messages.success(request, f'El usuario "{user.username}" ha sido creado. Se ha enviado un correo de invitación para que establezca su contraseña.')
            return redirect('lista_usuarios_admin')
    else:
        form = AdminUserCreationForm()

    return render(request, 'panel_admin/admin_crear_usuario.html', {'form': form})