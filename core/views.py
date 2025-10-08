from django.shortcuts import render, redirect
from reservas.models import Resena # Para mostrar reseñas en la página de inicio

def index(request):
    # Si un usuario ya logueado intenta ir a la página de inicio,
    # lo redirigimos a su panel correspondiente.
    if request.user.is_authenticated:
        return redirect('login_redirect')
    
    # Obtenemos TODAS las reseñas aprobadas para mostrarlas en la página principal.
    todas_las_resenas = Resena.objects.filter(aprobada=True).order_by('-fecha_creacion')

    context = {
        'resenas': todas_las_resenas
    }
    return render(request, 'core/index.html', context)

def sobre_nosotros(request):
    """
    Muestra la página de "Sobre Nosotros". Si el usuario está autenticado,
    usa la plantilla del panel; de lo contrario, usa la pública.
    """
    if request.user.is_authenticated and not request.user.is_staff:
        template_name = 'core/panel_sobre_nosotros.html'
    else:
        template_name = 'core/sobre_nosotros.html'
        
    return render(request, template_name)

def contacto(request):
    """
    Muestra la página de contacto. Si el usuario está autenticado,
    usa la plantilla del panel de usuario.
    """
    if request.user.is_authenticated and not request.user.is_staff:
        template_name = 'core/panel_contacto.html'
    else:
        template_name = 'core/contacto.html'
        
    return render(request, template_name)