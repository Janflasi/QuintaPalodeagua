# galeria/forms.py

from django import forms
from .models import Foto

class FotoForm(forms.ModelForm):
    class Meta:
        model = Foto
        fields = ['titulo', 'imagen']
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control'}),
            'imagen': forms.FileInput(attrs={'class': 'form-control'}),
        }