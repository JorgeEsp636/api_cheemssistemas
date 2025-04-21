from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

#creación de manager para los usuarios
class UsuarioManager(BaseUserManager):
    def create_user(self, correo_electronico, contrasena=None, **extra_fields):
        if not correo_electronico:
            raise ValueError('El correo electrónico debe ser proporcionado')
        correo_electronico = self.normalize_email(correo_electronico)
        user = self.model(correo_electronico=correo_electronico, **extra_fields)
        user.set_password(contrasena)
        user.save(using=self._db)
        return user

    def create_superuser(self, correo_electronico, contrasena=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(correo_electronico, contrasena, **extra_fields)

# modificación del modelo Usuario enlazado a AbstractBaseUser
class Usuario(AbstractBaseUser):
    id_usuario = models.AutoField(primary_key=True, db_column='id_usuario')
    correo_electronico = models.EmailField(unique=True, db_column='correo_electronico')
    contrasena = models.CharField(max_length=255, db_column='contrasena')
    nombre = models.CharField(max_length=100, db_column='nombre')
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    
    objects = UsuarioManager()

    USERNAME_FIELD = 'correo_electronico'
    REQUIRED_FIELDS = ['nombre']

    def __str__(self):
        return self.nombre

    class Meta:
        db_table = 'Usuarios'
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'


class Vehiculo(models.Model):
    id_vehiculos = models.AutoField(primary_key=True, db_column='id_vehiculos')
    placa = models.CharField(max_length=20, db_column='placa')
    empresa = models.IntegerField(db_column='empresa')
    disponibilidad = models.BooleanField(default=True, db_column='disponibilidad')

    def __str__(self):
        return self.placa

    class Meta:
        db_table = 'Vehiculos'
        verbose_name = 'Vehículo'
        verbose_name_plural = 'Vehículos'


class Conductor(models.Model):
    id_conductor = models.AutoField(primary_key=True, db_column='id_conductor')
    id_vehiculos = models.ForeignKey(Vehiculo, on_delete=models.CASCADE, db_column='Vehiculos_id_vehiculos')
    nombre = models.CharField(max_length=100, db_column='nombre')  # Ca
    licencia_conduccion = models.IntegerField(db_column='licencia_conduccion')

    def __str__(self):
        return self.nombre

    class Meta:
        db_table = 'Conductores'
        verbose_name = 'Conductor'
        verbose_name_plural = 'Conductores'


class Ruta(models.Model):
    id_ruta = models.AutoField(primary_key=True, db_column='id_ruta')
    id_vehiculos = models.ForeignKey(Vehiculo, on_delete=models.CASCADE, db_column='Vehiculos_id_vehiculos')
    nombre_ruta = models.CharField(max_length=100, db_column='nombre_ruta')  
    origen = models.CharField(max_length=100, db_column='origen')         
    destino = models.CharField(max_length=100, db_column='destino')         
    horario = models.TimeField(db_column='horario')

    def __str__(self):
        return self.nombre_ruta

    class Meta:
        db_table = 'Rutas'
        verbose_name = 'Ruta'
        verbose_name_plural = 'Rutas'


class Calificacion(models.Model):
    id_calificaciones = models.AutoField(primary_key=True, db_column='id_calificaciones')
    id_ruta = models.ForeignKey(Ruta, on_delete=models.CASCADE, db_column='Rutas_id_ruta')
    id_usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, db_column='Usuarios_id_usuario')
    calificacion = models.IntegerField(db_column='calificacion')
    comentario = models.TextField(db_column='comentario')
    fecha = models.DateField(db_column='fecha')

    def __str__(self):
        return f"{self.calificacion} - {self.id_usuario}"

    class Meta:
        db_table = 'Calificaciones'
        verbose_name = 'Calificación'
        verbose_name_plural = 'Calificaciones'
