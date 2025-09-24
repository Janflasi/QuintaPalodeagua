from django.db import models

class Foto(models.Model):
    titulo = models.CharField(max_length=100, help_text="Título descriptivo de la imagen")
    imagen = models.ImageField(upload_to='galeria/', help_text="Foto para la galería")

    def __str__(self):
        return self.titulo