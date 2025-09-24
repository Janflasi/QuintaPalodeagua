# reservas/admin.py
from django.contrib import admin, messages
from .models import Reserva
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

@admin.register(Reserva)
class ReservaAdmin(admin.ModelAdmin):
    # Campos a mostrar en la lista
    list_display = ('usuario', 'fecha_reserva', 'estado', 'tipo_evento', 'numero_personas', 'precio_cotizado')
    # Filtros laterales
    list_filter = ('estado', 'fecha_reserva')
    # Barra de búsqueda
    search_fields = ('usuario__username', 'tipo_evento')
    # Orden por defecto
    ordering = ('fecha_reserva',)

    # --- ACCIONES PERSONALIZADAS ---
    actions = ['confirmar_reservas', 'cancelar_reservas']

    def enviar_correo_estado(self, reserva):
        """Función para enviar correos de notificación."""
        asunto = f'Actualización de tu reserva para el {reserva.fecha_reserva}'
        contexto = {'reserva': reserva}
        html_mensaje = render_to_string('emails/notificacion_reserva.html', contexto)
        mensaje_plano = strip_tags(html_mensaje)
        email_desde = 'tu-email@gmail.com' # <-- CAMBIA ESTO
        email_para = [reserva.usuario.email]

        try:
            send_mail(asunto, mensaje_plano, email_desde, email_para, html_message=html_mensaje)
        except Exception as e:
            # En caso de error, no detener la acción en el admin
            self.message_user(
                self.request,
                f"Error al enviar correo para la reserva de {reserva.usuario.username}: {e}",
                messages.ERROR
            )

    def confirmar_reservas(self, request, queryset):
        for reserva in queryset:
            reserva.estado = 'confirmada'
            reserva.save()
            self.enviar_correo_estado(reserva)
        self.message_user(request, f"{queryset.count()} reservas han sido confirmadas y notificadas.")
    confirmar_reservas.short_description = "Confirmar reservas seleccionadas"

    def cancelar_reservas(self, request, queryset):
        for reserva in queryset:
            reserva.estado = 'cancelada'
            reserva.save()
            self.enviar_correo_estado(reserva)
        self.message_user(request, f"{queryset.count()} reservas han sido canceladas y notificadas.")
    cancelar_reservas.short_description = "Cancelar reservas seleccionadas"