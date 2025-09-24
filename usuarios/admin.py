from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import Perfil

# Define un "inline" para el modelo Perfil.
# Esto permite que se muestre y edite el Perfil en la misma página que el User.
class PerfilInline(admin.StackedInline):
    model = Perfil
    can_delete = False
    verbose_name_plural = 'perfiles'

# Define una nueva clase de admin para el modelo User
class UserAdmin(BaseUserAdmin):
    inlines = (PerfilInline,)

# Vuelve a registrar el modelo User con nuestro UserAdmin personalizado
admin.site.unregister(User)
admin.site.register(User, UserAdmin)