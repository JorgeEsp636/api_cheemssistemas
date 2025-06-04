from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class Rol(models.Model):
    """
    Modelo para representar roles de usuario en el sistema.
    
    Campos:
        id_rol: Identificador único del rol
        nombre: Nombre del rol (pasajero, conductor, administrador)
        descripcion: Descripción detallada del rol
    """
    id_rol = models.AutoField(primary_key=True, db_column='id_rol')
    nombre = models.CharField(max_length=50, db_column='nombre', unique=True)
    descripcion = models.TextField(db_column='descripcion')

    def __str__(self):
        """Retorna el nombre del rol como representación en string."""
        return self.nombre

    class Meta:
        """Metadatos del modelo Rol."""
        db_table = 'Roles'
        verbose_name = 'Rol'
        verbose_name_plural = 'Roles'

#creación de manager para los usuarios
class UsuarioManager(BaseUserManager):
    """
    Manager personalizado para el modelo Usuario.
    
    Este manager extiende BaseUserManager para proporcionar métodos de creación
    de usuarios que utilizan correo electrónico como identificador principal.
    
    Métodos:
        create_user: Crea un usuario normal con correo electrónico y contraseña
        create_superuser: Crea un superusuario con permisos administrativos
    
    Características:
        - Normaliza automáticamente las direcciones de correo electrónico
        - Maneja el hashing de contraseñas de forma segura
        - Establece permisos por defecto según el tipo de usuario
    """
    def create_user(self, correo_electronico, contrasena=None, **extra_fields):
        """
        Crea y guarda un usuario con el correo electrónico y contraseña dados.
        
        Args:
            correo_electronico (str): Correo electrónico del usuario
            contrasena (str): Contraseña del usuario
            **extra_fields: Campos adicionales para el usuario
            
        Returns:
            Usuario: El usuario creado
            
        Raises:
            ValueError: Si el correo electrónico no es proporcionado
        """
        if not correo_electronico:
            raise ValueError('El correo electrónico debe ser proporcionado')
        correo_electronico = self.normalize_email(correo_electronico)
        user = self.model(correo_electronico=correo_electronico, **extra_fields)
        user.set_password(contrasena)
        user.save(using=self._db)
        return user

    def create_superuser(self, correo_electronico, contrasena=None, **extra_fields):
        """
        Crea y guarda un superusuario con el correo electrónico y contraseña dados.
        
        Args:
            correo_electronico (str): Correo electrónico del superusuario
            contrasena (str): Contraseña del superusuario
            **extra_fields: Campos adicionales para el superusuario
            
        Returns:
            Usuario: El superusuario creado
            
        Características del superusuario:
            - is_staff = True
            - is_superuser = True
            - is_active = True
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(correo_electronico, contrasena, **extra_fields)

# modificación del modelo Usuario enlazado a AbstractBaseUser
class Usuario(AbstractBaseUser):
    """
    Modelo personalizado de Usuario.
    
    Extiende AbstractBaseUser para proporcionar un modelo de usuario personalizado
    que usa correo electrónico como identificador único.
    
    Campos:
        id_usuario: Identificador único del usuario
        correo_electronico: Correo electrónico del usuario (identificador único)
        nombre: Nombre completo del usuario
        rol: Rol asignado al usuario (pasajero, conductor, administrador)
        is_active: Indica si el usuario está activo
        is_staff: Indica si el usuario es parte del staff
        is_superuser: Indica si el usuario es superusuario
    """
    id_usuario = models.AutoField(primary_key=True, db_column='id_usuario')
    correo_electronico = models.EmailField(unique=True, db_column='correo_electronico')
    nombre = models.CharField(max_length=100, db_column='nombre')
    rol = models.ForeignKey(Rol, on_delete=models.PROTECT, db_column='Roles_id_rol', null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    
    objects = UsuarioManager()

    USERNAME_FIELD = 'correo_electronico'
    REQUIRED_FIELDS = ['nombre']

    def __str__(self):
        """Retorna el nombre del usuario como representación en string."""
        return self.nombre

    class Meta:
        """Metadatos del modelo Usuario."""
        db_table = 'Usuarios'
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'


class Vehiculo(models.Model):
    """
    Modelo para representar vehículos en el sistema.
    
    Campos:
        id_vehiculos: Identificador único del vehículo
        placa: Placa del vehículo
        empresa: ID de la empresa a la que pertenece el vehículo
        disponibilidad: Indica si el vehículo está disponible
    """
    id_vehiculos = models.AutoField(primary_key=True, db_column='id_vehiculos')
    placa = models.CharField(max_length=20, db_column='placa')
    empresa = models.IntegerField(db_column='empresa')
    disponibilidad = models.BooleanField(default=True, db_column='disponibilidad')

    def __str__(self):
        """Retorna la placa del vehículo como representación en string."""
        return self.placa

    class Meta:
        """Metadatos del modelo Vehiculo."""
        db_table = 'Vehiculos'
        verbose_name = 'Vehículo'
        verbose_name_plural = 'Vehículos'


class Conductor(models.Model):
    """
    Modelo para representar conductores en el sistema.
    
    Campos:
        id_conductor: Identificador único del conductor
        id_vehiculos: Referencia al vehículo asignado
        nombre: Nombre completo del conductor
        licencia_conduccion: Número de licencia de conducción
    """
    id_conductor = models.AutoField(primary_key=True, db_column='id_conductor')
    id_vehiculos = models.ForeignKey(Vehiculo, on_delete=models.CASCADE, db_column='Vehiculos_id_vehiculos')
    nombre = models.CharField(max_length=100, db_column='nombre')
    licencia_conduccion = models.IntegerField(db_column='licencia_conduccion')

    def __str__(self):
        """Retorna el nombre del conductor como representación en string."""
        return self.nombre

    class Meta:
        """Metadatos del modelo Conductor."""
        db_table = 'Conductores'
        verbose_name = 'Conductor'
        verbose_name_plural = 'Conductores'


class Ruta(models.Model):
    """
    Modelo para representar rutas en el sistema.
    
    Campos:
        id_ruta: Identificador único de la ruta
        id_vehiculos: Referencia al vehículo asignado
        nombre_ruta: Nombre descriptivo de la ruta
        origen: Punto de origen de la ruta
        destino: Punto de destino de la ruta
        horario: Horario programado de la ruta
    """
    id_ruta = models.AutoField(primary_key=True, db_column='id_ruta')
    id_vehiculos = models.ForeignKey(Vehiculo, on_delete=models.CASCADE, db_column='Vehiculos_id_vehiculos')
    nombre_ruta = models.CharField(max_length=100, db_column='nombre_ruta')  
    origen = models.CharField(max_length=100, db_column='origen')         
    destino = models.CharField(max_length=100, db_column='destino')         
    horario = models.TimeField(db_column='horario')

    def __str__(self):
        """Retorna el nombre de la ruta como representación en string."""
        return self.nombre_ruta

    class Meta:
        """Metadatos del modelo Ruta."""
        db_table = 'Rutas'
        verbose_name = 'Ruta'
        verbose_name_plural = 'Rutas'


class Calificacion(models.Model):
    """
    Modelo para representar calificaciones de rutas.
    
    Campos:
        id_calificaciones: Identificador único de la calificación
        id_ruta: Referencia a la ruta calificada
        id_usuario: Referencia al usuario que realiza la calificación
        calificacion: Puntuación numérica de la calificación
        comentario: Comentario o retroalimentación sobre la ruta
        fecha: Fecha en que se realizó la calificación (se asigna automáticamente)
    """
    id_calificaciones = models.AutoField(primary_key=True, db_column='id_calificaciones')
    id_ruta = models.ForeignKey(Ruta, on_delete=models.CASCADE, db_column='Rutas_id_ruta')
    id_usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, db_column='Usuarios_id_usuario')
    calificacion = models.IntegerField(db_column='calificacion')
    comentario = models.TextField(db_column='comentario')
    fecha = models.DateField(db_column='fecha', auto_now_add=True)

    def __str__(self):
        """Retorna la calificación y el usuario como representación en string."""
        return f"{self.calificacion} - {self.id_usuario}"

    class Meta:
        """Metadatos del modelo Calificacion."""
        db_table = 'Calificaciones'
        verbose_name = 'Calificación'
        verbose_name_plural = 'Calificaciones'

class Zona(models.Model):
    """
    Modelo para representar zonas geográficas en el sistema.
    
    Campos:
        id_zona: Identificador único de la zona
        nombre: Nombre de la zona
        descripcion: Descripción detallada de la zona
        activa: Indica si la zona está activa para tarifas
    """
    id_zona = models.AutoField(primary_key=True, db_column='id_zona')
    nombre = models.CharField(max_length=100, db_column='nombre')
    descripcion = models.TextField(db_column='descripcion')
    activa = models.BooleanField(default=True, db_column='activa')

    def __str__(self):
        """Retorna el nombre de la zona como representación en string."""
        return self.nombre

    class Meta:
        """Metadatos del modelo Zona."""
        db_table = 'Zonas'
        verbose_name = 'Zona'
        verbose_name_plural = 'Zonas'

class Tarifa(models.Model):
    """
    Modelo para representar tarifas dinámicas por zona.
    
    Campos:
        id_tarifa: Identificador único de la tarifa
        zona_origen: Zona de origen del viaje
        zona_destino: Zona de destino del viaje
        precio_base: Precio base del viaje
        precio_km: Precio por kilómetro adicional
        activa: Indica si la tarifa está activa
        fecha_actualizacion: Fecha de última actualización
        actualizado_por: Usuario que realizó la última actualización
    """
    id_tarifa = models.AutoField(primary_key=True, db_column='id_tarifa')
    zona_origen = models.ForeignKey(Zona, on_delete=models.PROTECT, related_name='tarifas_origen', db_column='Zonas_id_origen')
    zona_destino = models.ForeignKey(Zona, on_delete=models.PROTECT, related_name='tarifas_destino', db_column='Zonas_id_destino')
    precio_base = models.DecimalField(max_digits=10, decimal_places=2, db_column='precio_base')
    precio_km = models.DecimalField(max_digits=10, decimal_places=2, db_column='precio_km')
    activa = models.BooleanField(default=True, db_column='activa')
    fecha_actualizacion = models.DateTimeField(auto_now=True, db_column='fecha_actualizacion')
    actualizado_por = models.ForeignKey(Usuario, on_delete=models.PROTECT, db_column='Usuarios_id_actualizado_por')

    def __str__(self):
        """Retorna la descripción de la tarifa como representación en string."""
        return f"Tarifa {self.zona_origen} - {self.zona_destino}"

    class Meta:
        """Metadatos del modelo Tarifa."""
        db_table = 'Tarifas'
        verbose_name = 'Tarifa'
        verbose_name_plural = 'Tarifas'
        unique_together = ['zona_origen', 'zona_destino']
