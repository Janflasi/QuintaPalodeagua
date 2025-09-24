# galeria/views.py
from django.shortcuts import render
from .models import Foto

def galeria(request):
    # La consulta a la base de datos es la misma
    fotos = Foto.objects.all()

    # Lógica para elegir la plantilla
    if request.user.is_authenticated:
        # Si el usuario ha iniciado sesión, usa la plantilla del panel
        template_name = 'galeria/panel_galeria.html'
    else:
        # Si es un visitante, usa la plantilla pública
        template_name = 'galeria/galeria.html'

    contexto = {'fotos': fotos}
    return render(request, template_name, contexto)