# usuarios/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import Perfil

class PerfilInline(admin.StackedInline):
    model = Perfil
    can_delete = False
    verbose_name_plural = 'perfiles'

class UserAdmin(BaseUserAdmin):
    inlines = (PerfilInline,)

# Re-registrar User con la configuración simple
admin.site.unregister(User)
admin.site.register(User, UserAdmin)