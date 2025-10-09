# contabilidad/forms.py

from django import forms
from .models import Movimiento, Producto, Venta

class MovimientoForm(forms.ModelForm):
    """ Formulario para crear o editar un Movimiento (ingreso/egreso). """
    class Meta:
        model = Movimiento
        fields = ['tipo', 'monto', 'descripcion', 'reserva_asociada']
        widgets = {
            'tipo': forms.Select(attrs={'class': 'form-control'}),
            'monto': forms.NumberInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'reserva_asociada': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Hacemos que la reserva asociada sea opcional
        self.fields['reserva_asociada'].required = False


class ProductoForm(forms.ModelForm):
    """ Formulario para crear o editar un Producto. """
    class Meta:
        model = Producto
        fields = ['nombre', 'precio_venta', 'stock_actual']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'precio_venta': forms.NumberInput(attrs={'class': 'form-control'}),
            'stock_actual': forms.NumberInput(attrs={'class': 'form-control'}),
        }


class VentaForm(forms.ModelForm):
    """ Formulario para registrar una Venta. """
    class Meta:
        model = Venta
        fields = ['producto', 'cantidad']
        widgets = {
            'producto': forms.Select(attrs={'class': 'form-control'}),
            'cantidad': forms.NumberInput(attrs={'class': 'form-control'}),
        }