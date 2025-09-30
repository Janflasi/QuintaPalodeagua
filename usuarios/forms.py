from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from .models import Perfil

class CustomUserCreationForm(UserCreationForm):
    """
    Un formulario para crear nuevos usuarios. Extiende el formulario base de Django.
    Actualmente no tiene personalizaciones, pero está aquí por si se necesitan en el futuro.
    """
    pass


class UserUpdateForm(UserChangeForm):
    """
    Formulario para actualizar los datos básicos del usuario (los que vienen con Django).
    La contraseña se elimina de este formulario para que no se muestre en la página de edición.
    """
    password = None # Excluimos el campo de la contraseña

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
        }


class PerfilUpdateForm(forms.ModelForm):
    """
    Formulario para actualizar los datos adicionales del perfil del usuario
    (teléfono y dirección).
    """
    class Meta:
        model = Perfil
        fields = ('telefono', 'direccion')
        widgets = {
            'telefono': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: 3001234567'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Calle 5 # 10-20'}),
        }