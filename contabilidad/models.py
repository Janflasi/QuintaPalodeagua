# contabilidad/models.py

from django.db import models
from django.contrib.auth.models import User
from reservas.models import Reserva # Importamos el modelo de Reserva para poder enlazarlo

# --- Modelo para Contabilidad General ---

class Movimiento(models.Model):
    """ Representa una transacción monetaria, ya sea un ingreso o un egreso. """
    
    TIPO_MOVIMIENTO_CHOICES = [
        ('ingreso', 'Ingreso'),
        ('egreso', 'Egreso'),
    ]

    tipo = models.CharField(max_length=7, choices=TIPO_MOVIMIENTO_CHOICES, verbose_name="Tipo de Movimiento")
    monto = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Monto")
    descripcion = models.TextField(verbose_name="Descripción")
    fecha = models.DateField(auto_now_add=True, verbose_name="Fecha de Registro")
    
    # Quién registró el movimiento (opcional)
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Usuario que registra")
    
    # Si el ingreso está ligado a una reserva específica (opcional)
    reserva_asociada = models.ForeignKey(Reserva, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Reserva Asociada")

    def __str__(self):
        return f"{self.get_tipo_display()} - ${self.monto:,.2f} - {self.descripcion[:40]}"

    class Meta:
        ordering = ['-fecha']


# --- Modelos para Inventario y Ventas ---

class Producto(models.Model):
    """ Representa un producto que se vende en la quinta, como cervezas, snacks, etc. """
    
    nombre = models.CharField(max_length=100, unique=True, verbose_name="Nombre del Producto")
    precio_venta = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Precio de Venta")
    stock_actual = models.PositiveIntegerField(default=0, verbose_name="Cantidad en Stock")

    def __str__(self):
        return self.nombre

    class Meta:
        ordering = ['nombre']


class Venta(models.Model):
    """ Registra una venta de uno o más productos. """
    
    producto = models.ForeignKey(Producto, on_delete=models.PROTECT, verbose_name="Producto Vendido")
    cantidad = models.PositiveIntegerField(verbose_name="Cantidad Vendida")
    precio_total = models.DecimalField(max_digits=10, decimal_places=2, editable=False, verbose_name="Precio Total")
    fecha = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Venta")

    def save(self, *args, **kwargs):
        # Calcula el precio total antes de guardar
        self.precio_total = self.producto.precio_venta * self.cantidad
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Venta de {self.cantidad} x {self.producto.nombre} el {self.fecha.strftime('%d/%m/%Y')}"

    class Meta:
        ordering = ['-fecha']