from django.db import migrations

def crear_roles_iniciales(apps, schema_editor):
    Rol = apps.get_model('api_app', 'Rol')
    roles = [
        {'nombre': 'Administrador', 'descripcion': 'Rol con acceso total al sistema'},
        {'nombre': 'Conductor', 'descripcion': 'Rol para conductores de vehículos'},
        {'nombre': 'Pasajero', 'descripcion': 'Rol para usuarios pasajeros'}
    ]
    for rol in roles:
        Rol.objects.get_or_create(nombre=rol['nombre'], defaults=rol)

def eliminar_roles_iniciales(apps, schema_editor):
    Rol = apps.get_model('api_app', 'Rol')
    Rol.objects.filter(nombre__in=['Administrador', 'Conductor', 'Pasajero']).delete()

class Migration(migrations.Migration):
    dependencies = [
        ('api_app', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(crear_roles_iniciales, eliminar_roles_iniciales),
    ] 