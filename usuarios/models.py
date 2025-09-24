# usuarios/models.py

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Perfil(models.Model):
    # Relación uno a uno con el modelo User de Django
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    
    # Campos adicionales que queramos guardar
    telefono = models.CharField(max_length=20, null=True, blank=True)
    direccion = models.CharField(max_length=255, null=True, blank=True)
    
    def __str__(self):
        return f'Perfil de {self.usuario.username}'

# Esta es la "magia" para que el perfil se cree automáticamente
# cuando un nuevo usuario se registra.

@receiver(post_save, sender=User)
def crear_perfil_usuario(sender, instance, created, **kwargs):
    if created:
        Perfil.objects.create(usuario=instance)

@receiver(post_save, sender=User)
def guardar_perfil_usuario(sender, instance, **kwargs):
    instance.perfil.save()