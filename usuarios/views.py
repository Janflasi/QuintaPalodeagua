# usuarios/views.py
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import CustomUserCreationForm
from django.contrib.auth.decorators import login_required # Importar el decorador
from .forms import CustomUserCreationForm, UserUpdateForm # Añadir UserUpdateForm

def registro(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            # Mensaje de éxito mejorado
            messages.success(request, f'¡Cuenta creada para {username}! Ahora, por favor, inicia sesión.')
            # Redirigir a la página de LOGIN
            return redirect('login') 
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'usuarios/registro.html', {'form': form})
@login_required # <-- Este decorador protege la vista
def perfil(request):
    return render(request, 'usuarios/perfil.html')


@login_required
def editar_perfil(request):
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, '¡Tu perfil ha sido actualizado!')
            return redirect('perfil')
    else:
        form = UserUpdateForm(instance=request.user)

    return render(request, 'usuarios/editar_perfil.html', {'form': form})