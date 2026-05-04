from django.contrib import admin
from .models import Usuario, Rol

@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('correo_electronico', 'nombre', 'is_superuser', 'is_staff', 'is_active', 'rol')
    search_fields = ('correo_electronico', 'nombre')
    list_filter = ('is_superuser', 'is_staff', 'is_active', 'rol')

@admin.register(Rol)
class RolAdmin(admin.ModelAdmin):
    list_display = ('id_rol', 'nombre', 'descripcion')
    search_fields = ('nombre',)
