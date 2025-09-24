# core/views.py
from django.shortcuts import render, redirect

def index(request):
    # Si el usuario ya está autenticado, redirígelo a su panel
    if request.user.is_authenticated:
        return redirect('panel_usuario')
    
    # Si no, muéstrale la página de bienvenida normal
    return render(request, 'core/index.html')

def sobre_nosotros(request):
    return render(request, 'core/sobre_nosotros.html')