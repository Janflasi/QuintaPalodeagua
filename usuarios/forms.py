# usuarios/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class CustomUserCreationForm(UserCreationForm):
    """
    Formulario para la creación de nuevos usuarios con campos adicionales
    y placeholders para un diseño moderno.
    """
    class Meta(UserCreationForm.Meta):
        model = User
        # Se añaden los campos de nombre, apellido y correo al formulario base de registro
        fields = ('username', 'first_name', 'last_name', 'email')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Diccionario con los textos de ejemplo para cada campo
        placeholders = {
            'username': 'Nombre de usuario',
            'first_name': 'Tu nombre',
            'last_name': 'Tu apellido',
            'email': 'Correo electrónico',
            'password1': 'Crea una contraseña',
            'password2': 'Confirma tu contraseña',
        }
        # Bucle para aplicar la clase 'form-control' y el placeholder a cada campo
        for field_name, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'form-control', 
                'placeholder': placeholders.get(field_name, '')
            })

class UserUpdateForm(forms.ModelForm):
    """
    Formulario para que los usuarios editen su propia información de perfil.
    """
    # Se asegura de que el campo de correo electrónico sea obligatorio al editar
    email = forms.EmailField(required=True)
    
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Diccionario con los textos de ejemplo para cada campo
        placeholders = {
            'username': 'Nombre de usuario',
            'first_name': 'Tu nombre',
            'last_name': 'Tu apellido',
            'email': 'Correo electrónico',
        }
        # Bucle para aplicar la clase 'form-control' y el placeholder a cada campo
        for field_name, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'form-control',
                'placeholder': placeholders.get(field_name, '')
            })