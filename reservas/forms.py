# reservas/forms.py

from django import forms
from .models import Reserva, Resena

# --- FORMULARIO PARA CLIENTES (EL QUE FALTABA) ---
class ReservaForm(forms.ModelForm):
    class Meta:
        model = Reserva
        fields = ['fecha_reserva', 'numero_personas', 'tipo_evento']
        widgets = {
            'fecha_reserva': forms.DateInput(
                attrs={
                    'type': 'date',
                    'class': 'form-control',
                }
            ),
            'numero_personas': forms.NumberInput(
                attrs={'class': 'form-control', 'placeholder': 'Ej: 50'}
            ),
            'tipo_evento': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Ej: Boda, Cumpleaños'}
            ),
        }
        labels = {
            'fecha_reserva': 'Fecha deseada para el evento',
            'numero_personas': 'Número aproximado de personas',
            'tipo_evento': 'Tipo de evento',
        }


# --- FORMULARIO PARA EL ADMINISTRADOR (EL QUE ACTUALIZAMOS) ---
class ReservaAdminForm(forms.ModelForm):
    class Meta:
        model = Reserva
        fields = [
            'usuario', 'fecha_reserva', 'numero_personas', 'tipo_evento', 
            'estado', 'precio', 'hora_ingreso', 'hora_salida', 
            'detalles_privilegios', 'penalizacion_tardia'
        ]
        widgets = {
            'usuario': forms.Select(attrs={'class': 'form-control'}),
            'fecha_reserva': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'numero_personas': forms.NumberInput(attrs={'class': 'form-control'}),
            'tipo_evento': forms.TextInput(attrs={'class': 'form-control'}),
            'estado': forms.Select(attrs={'class': 'form-control'}),
            'precio': forms.NumberInput(attrs={'class': 'form-control'}),
            'hora_ingreso': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'hora_salida': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'detalles_privilegios': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
            'penalizacion_tardia': forms.NumberInput(attrs={'class': 'form-control'}),
        }


# --- FORMULARIO PARA RESEÑAS ---
class ResenaForm(forms.ModelForm):
    class Meta:
        model = Resena
        fields = ['calificacion', 'comentario']
        widgets = {
            'calificacion': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 5}),
            'comentario': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }
        labels = {
            'calificacion': 'Calificación (1 a 5 estrellas)',
            'comentario': 'Tu comentario',
        }