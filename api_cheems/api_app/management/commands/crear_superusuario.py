from django.core.management.base import BaseCommand
from api_app.models import Usuario

class Command(BaseCommand):
    help = 'Crea un superusuario con las credenciales especificadas o repara uno existente.'

    def handle(self, *args, **options):
        try:
            # Buscar superusuario existente
            superusers = Usuario.objects.filter(is_superuser=True)
            if superusers.exists():
                for su in superusers:
                    su.is_staff = True
                    su.is_active = True
                    su.set_password('admin123')
                    su.save()
                self.stdout.write(self.style.SUCCESS('Superusuario(s) reparado(s) correctamente. Contraseña: admin123'))
                return

            # Crear el superusuario si no existe
            superuser = Usuario.objects.create_superuser(
                correo_electronico='admin@cheems.com',
                contrasena='admin123',
                nombre='Administrador'
            )
            self.stdout.write(self.style.SUCCESS('Superusuario creado exitosamente'))
            self.stdout.write(f'Email: {superuser.correo_electronico}')
            self.stdout.write(f'Contraseña: admin123')
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error al crear o reparar el superusuario: {str(e)}')) 