# reservas/management/commands/cancelar_reservas_impagas.py

from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from reservas.models import Reserva
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings # Importar settings

class Command(BaseCommand):
    help = 'Busca y cancela las reservas que no han sido pagadas después de 24 horas.'

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE('Iniciando tarea: Cancelar reservas impagas...'))

        # Límite de tiempo. RECUERDA: Cambia a hours=24 para producción
        limite_de_tiempo = timezone.now() - timedelta(seconds=10)

        reservas_a_cancelar = Reserva.objects.filter(
            estado='esperando_pago',
            fecha_esperando_pago__lte=limite_de_tiempo
        )

        if not reservas_a_cancelar.exists():
            self.stdout.write(self.style.SUCCESS('No se encontraron reservas para cancelar.'))
            return

        for reserva in reservas_a_cancelar:
            reserva.estado = 'cancelada'
            reserva.save(update_fields=['estado'])

            # --- Enviar correo de notificación al cliente ---
            mail_subject = 'Tu solicitud de reserva ha sido cancelada'
            
            # --- AJUSTE AQUÍ ---
            # Definimos el dominio. Para desarrollo local es '127.0.0.1:8000'.
            # Para producción, sería 'www.quintapalodeagua.com'
            domain = '127.0.0.1:8000'
            protocol = 'http'

            message = render_to_string('emails/cancelacion_automatica.html', {
                'reserva': reserva,
                'domain': domain,
                'protocol': protocol,
            })
            
            send_mail(mail_subject, '', None, [reserva.usuario.email], html_message=message)
            # --- Fin del ajuste ---

            self.stdout.write(self.style.WARNING(f'Reserva ID {reserva.id} para "{reserva.usuario.username}" ha sido cancelada por falta de pago.'))
        
        self.stdout.write(self.style.SUCCESS(f'Tarea completada. Se cancelaron {reservas_a_cancelar.count()} reservas.'))

