# core/forms.py
from django import forms

class ContactoForm(forms.Form):
    nombre = forms.CharField(max_length=100, required=True, label="Tu Nombre", 
                             widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(required=True, label="Tu Correo Electrónico",
                             widget=forms.EmailInput(attrs={'class': 'form-control'}))
    asunto = forms.CharField(max_length=100, required=True, label="Asunto",
                              widget=forms.TextInput(attrs={'class': 'form-control'}))
    mensaje = forms.CharField(required=True, label="Mensaje",
                              widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5}))