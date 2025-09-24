# reservas/forms.py (archivo nuevo)
from django import forms
from .models import Reserva

class ReservaForm(forms.ModelForm):
    class Meta:
        model = Reserva
        # Campos que el usuario llenará
        fields = ['fecha_reserva', 'numero_personas', 'tipo_evento']
        # Widgets para mejorar la apariencia de los campos
        widgets = {
            'fecha_reserva': forms.DateInput(
                attrs={'type': 'date', 'class': 'form-control'}
            ),
            'numero_personas': forms.NumberInput(
                attrs={'class': 'form-control', 'placeholder': 'Ej: 50'}
            ),
            'tipo_evento': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Ej: Boda, Cumpleaños, Evento Corporativo'}
            ),
        }
        # Etiquetas personalizadas en español
        labels = {
            'fecha_reserva': 'Fecha deseada para el evento',
            'numero_personas': 'Número estimado de personas',
            'tipo_evento': 'Tipo de evento',
        }