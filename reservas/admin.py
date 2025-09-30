# reservas/admin.py

from django.contrib import admin
from .models import Reserva

@admin.register(Reserva)
class ReservaAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'fecha_reserva', 'tipo_evento', 'estado', 'fecha_creacion')
    list_editable = ('estado',)
    list_filter = ('estado', 'fecha_reserva', 'fecha_creacion')
    search_fields = ('usuario__username', 'tipo_evento')
    ordering = ('-fecha_creacion',)
    actions = ['marcar_como_confirmada', 'marcar_como_cancelada']

    def marcar_como_confirmada(self, request, queryset):
        queryset.update(estado='confirmada')
        self.message_user(request, "Las reservas seleccionadas han sido confirmadas.")
    marcar_como_confirmada.short_description = "Confirmar reservas seleccionadas"

    def marcar_como_cancelada(self, request, queryset):
        queryset.update(estado='cancelada')
        self.message_user(request, "Las reservas seleccionadas han sido canceladas.")
    marcar_como_cancelada.short_description = "Cancelar reservas seleccionadas"