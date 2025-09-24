# usuarios/views.py
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm, UserUpdateForm

def registro(request):
    """
    Gestiona el registro de nuevos usuarios.
    Si el registro es exitoso, redirige a la página de login.
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

def login_inteligente(request):
    """
    Gestiona el inicio de sesión y redirige al usuario
    al panel correcto según su rol (admin o normal).
    """
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                # Lógica de redirección basada en el rol
                if user.is_staff or user.is_superuser:
                    return redirect('admin_dashboard') # Redirige al panel de admin
                else:
                    return redirect('panel_usuario') # Redirige al panel de usuario
            else:
                messages.error(request, "Usuario o contraseña incorrectos.")
        else:
            messages.error(request, "Usuario o contraseña incorrectos.")
    
    form = AuthenticationForm()
    return render(request, 'usuarios/login.html', {'form': form})

@login_required
def perfil(request):
    """
    Muestra la página de perfil del usuario que ha iniciado sesión.
    """
    return render(request, 'usuarios/perfil.html')

@login_required
def editar_perfil(request):
    """
    Permite al usuario editar su propia información de perfil.
    """
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, '¡Tu perfil ha sido actualizado!')
            return redirect('perfil')
    else:
        form = UserUpdateForm(instance=request.user)

    return render(request, 'usuarios/editar_perfil.html', {'form': form})