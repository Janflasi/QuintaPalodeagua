from django.contrib import admin
from .models import Reserva, Resena # <-- Importamos el nuevo modelo Resena

@admin.register(Reserva)
class ReservaAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'fecha_reserva', 'tipo_evento', 'estado')
    list_filter = ('estado', 'fecha_reserva')
    list_editable = ('estado',)
    search_fields = ('usuario__username', 'tipo_evento')

# --- AÑADE ESTE NUEVO BLOQUE PARA GESTIONAR LAS RESEÑAS ---
@admin.register(Resena)
class ResenaAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'reserva', 'calificacion', 'aprobada', 'fecha_creacion')
    list_filter = ('aprobada', 'calificacion')
    search_fields = ('usuario__username', 'comentario')
    
    # Acción para aprobar reseñas seleccionadas
    actions = ['aprobar_resenas']

    def aprobar_resenas(self, request, queryset):
        queryset.update(aprobada=True)
        self.message_user(request, "Las reseñas seleccionadas han sido aprobadas.")
    aprobar_resenas.short_description = "Aprobar reseñas seleccionadas"