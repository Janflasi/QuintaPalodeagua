from django.shortcuts import render, redirect
from reservas.models import Resena # Para mostrar reseñas en la página de inicio

def index(request):
    # Si un usuario ya logueado intenta ir a la página de inicio,
    # lo redirigimos a su panel correspondiente.
    if request.user.is_authenticated:
        return redirect('login_redirect')
    
    # Obtenemos las 3 mejores reseñas para mostrarlas en la página principal.
    mejores_resenas = Resena.objects.filter(aprobada=True, calificacion__gte=4).order_by('-fecha_creacion')[:3]

    context = {
        'resenas': mejores_resenas
    }
    return render(request, 'core/index.html', context)

def sobre_nosotros(request):
    return render(request, 'core/sobre_nosotros.html')

def contacto(request):
    """
    Muestra la página estática con la información de contacto.
    """
    return render(request, 'core/contacto.html')