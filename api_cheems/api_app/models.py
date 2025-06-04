from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.exceptions import ValidationError

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
    rol = models.ForeignKey(Rol, on_delete=models.PROTECT, db_column='Roles_id_rol', null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    
    objects = UsuarioManager()

    USERNAME_FIELD = 'correo_electronico'
    REQUIRED_FIELDS = ['nombre']

    def clean(self):
        """Valida los campos del modelo antes de guardar."""
        super().clean()
        if not self.correo_electronico:
            raise ValidationError({'correo_electronico': 'El correo electrónico es requerido'})
        if not self.nombre:
            raise ValidationError({'nombre': 'El nombre es requerido'})
        if Usuario.objects.filter(correo_electronico=self.correo_electronico).exclude(pk=self.pk).exists():
            raise ValidationError({'correo_electronico': 'Este correo electrónico ya está registrado'})

    def save(self, *args, **kwargs):
        """Guarda el modelo después de validar los campos."""
        self.full_clean()
        super().save(*args, **kwargs)

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
    placa = models.CharField(max_length=20, db_column='placa', unique=True)
    empresa = models.IntegerField(db_column='empresa')
    disponibilidad = models.BooleanField(default=True, db_column='disponibilidad')

    def clean(self):
        """Valida los campos del modelo antes de guardar."""
        super().clean()
        if not self.placa:
            raise ValidationError({'placa': 'La placa es requerida'})
        if not self.empresa:
            raise ValidationError({'empresa': 'La empresa es requerida'})
        if Vehiculo.objects.filter(placa=self.placa).exclude(pk=self.pk).exists():
            raise ValidationError({'placa': 'Esta placa ya está registrada'})

    def save(self, *args, **kwargs):
        """Guarda el modelo después de validar los campos."""
        self.full_clean()
        super().save(*args, **kwargs)

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
        fecha_vencimiento_licencia: Fecha de vencimiento de la licencia de conducción
        fecha_vencimiento_soat: Fecha de vencimiento del SOAT
        fecha_vencimiento_tecnomecanica: Fecha de vencimiento de la tecnomecánica
    """
    id_conductor = models.AutoField(primary_key=True, db_column='id_conductor')
    id_vehiculos = models.ForeignKey(Vehiculo, on_delete=models.CASCADE, db_column='Vehiculos_id_vehiculos')
    nombre = models.CharField(max_length=100, db_column='nombre')
    licencia_conduccion = models.IntegerField(db_column='licencia_conduccion', unique=True)
    fecha_vencimiento_licencia = models.DateField(db_column='fecha_vencimiento_licencia', null=True, blank=True)
    fecha_vencimiento_soat = models.DateField(db_column='fecha_vencimiento_soat', null=True, blank=True)
    fecha_vencimiento_tecnomecanica = models.DateField(db_column='fecha_vencimiento_tecnomecanica', null=True, blank=True)

    def clean(self):
        """Valida los campos del modelo antes de guardar."""
        super().clean()
        if not self.nombre:
            raise ValidationError({'nombre': 'El nombre es requerido'})
        if not self.licencia_conduccion:
            raise ValidationError({'licencia_conduccion': 'La licencia de conducción es requerida'})
        if not self.id_vehiculos:
            raise ValidationError({'id_vehiculos': 'El vehículo es requerido'})
        if Conductor.objects.filter(licencia_conduccion=self.licencia_conduccion).exclude(pk=self.pk).exists():
            raise ValidationError({'licencia_conduccion': 'Esta licencia ya está registrada'})

    def save(self, *args, **kwargs):
        """Guarda el modelo después de validar los campos."""
        self.full_clean()
        super().save(*args, **kwargs)

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

class Viaje(models.Model):
    """
    Modelo para representar los viajes realizados por los pasajeros.
    
    Campos:
        id_viaje: Identificador único del viaje
        id_ruta: Referencia a la ruta del viaje
        id_usuario: Referencia al pasajero
        fecha_viaje: Fecha en que se realizó el viaje
        estado: Estado del viaje (completado, cancelado, en curso)
        precio_final: Precio final del viaje
        calificacion: Referencia a la calificación del viaje (opcional)
    """
    ESTADOS = [
        ('completado', 'Completado'),
        ('cancelado', 'Cancelado'),
        ('en_curso', 'En Curso')
    ]
    
    id_viaje = models.AutoField(primary_key=True, db_column='id_viaje')
    id_ruta = models.ForeignKey(Ruta, on_delete=models.PROTECT, db_column='Rutas_id_ruta')
    id_usuario = models.ForeignKey(Usuario, on_delete=models.PROTECT, db_column='Usuarios_id_usuario')
    fecha_viaje = models.DateTimeField(db_column='fecha_viaje', auto_now_add=True)
    estado = models.CharField(max_length=20, choices=ESTADOS, default='en_curso', db_column='estado')
    precio_final = models.DecimalField(max_digits=10, decimal_places=2, db_column='precio_final')
    calificacion = models.OneToOneField(Calificacion, on_delete=models.SET_NULL, null=True, blank=True, db_column='Calificaciones_id_calificaciones')

    def __str__(self):
        """Retorna la descripción del viaje como representación en string."""
        return f"Viaje {self.id_viaje} - {self.id_usuario.nombre} - {self.id_ruta.nombre_ruta}"

    class Meta:
        """Metadatos del modelo Viaje."""
        db_table = 'Viajes'
        verbose_name = 'Viaje'
        verbose_name_plural = 'Viajes'
        ordering = ['-fecha_viaje']

class RutaFavorita(models.Model):
    """
    Modelo para representar las rutas favoritas de los usuarios.
    
    Campos:
        id_ruta_favorita: Identificador único de la ruta favorita
        id_usuario: Referencia al usuario que marcó la ruta como favorita
        id_ruta: Referencia a la ruta marcada como favorita
        fecha_agregada: Fecha en que se marcó la ruta como favorita
    """
    id_ruta_favorita = models.AutoField(primary_key=True, db_column='id_ruta_favorita')
    id_usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, db_column='Usuarios_id_usuario')
    id_ruta = models.ForeignKey(Ruta, on_delete=models.CASCADE, db_column='Rutas_id_ruta')
    fecha_agregada = models.DateTimeField(db_column='fecha_agregada', auto_now_add=True)

    def __str__(self):
        """Retorna la descripción de la ruta favorita como representación en string."""
        return f"Ruta favorita de {self.id_usuario.nombre}: {self.id_ruta.nombre_ruta}"

    class Meta:
        """Metadatos del modelo RutaFavorita."""
        db_table = 'RutasFavoritas'
        verbose_name = 'Ruta Favorita'
        verbose_name_plural = 'Rutas Favoritas'
        unique_together = ['id_usuario', 'id_ruta']
        ordering = ['-fecha_agregada']

class CalificacionConductor(models.Model):
    """
    Modelo para representar las calificaciones de conductores.
    
    Campos:
        id_calificacion_conductor: Identificador único de la calificación
        id_viaje: Referencia al viaje realizado
        id_usuario: Referencia al pasajero que califica
        id_conductor: Referencia al conductor calificado
        calificacion: Puntuación numérica (1-5)
        comentario: Comentario o retroalimentación sobre el conductor
        fecha: Fecha en que se realizó la calificación
    """
    id_calificacion_conductor = models.AutoField(primary_key=True, db_column='id_calificacion_conductor')
    id_viaje = models.ForeignKey(Viaje, on_delete=models.CASCADE, db_column='Viajes_id_viaje')
    id_usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, db_column='Usuarios_id_usuario')
    id_conductor = models.ForeignKey(Conductor, on_delete=models.CASCADE, db_column='Conductores_id_conductor')
    calificacion = models.IntegerField(db_column='calificacion')
    comentario = models.TextField(db_column='comentario')
    fecha = models.DateTimeField(db_column='fecha', auto_now_add=True)

    def __str__(self):
        """Retorna la descripción de la calificación como representación en string."""
        return f"Calificación de {self.id_usuario.nombre} a {self.id_conductor.nombre}: {self.calificacion}"

    class Meta:
        """Metadatos del modelo CalificacionConductor."""
        db_table = 'CalificacionesConductores'
        verbose_name = 'Calificación de Conductor'
        verbose_name_plural = 'Calificaciones de Conductores'
        unique_together = ['id_viaje', 'id_usuario', 'id_conductor']
        ordering = ['-fecha']

class EstadisticaEmpresa(models.Model):
    """
    Modelo para almacenar estadísticas de las empresas de transporte.
    
    Campos:
        id_estadistica: Identificador único de la estadística
        id_empresa: ID de la empresa a la que pertenece la estadística
        fecha: Fecha de la estadística
        total_viajes: Número total de viajes realizados
        viajes_completados: Número de viajes completados
        viajes_cancelados: Número de viajes cancelados
        ingresos_totales: Ingresos totales generados
        calificacion_promedio: Calificación promedio de los conductores
        pasajeros_transportados: Número total de pasajeros transportados
        kilometros_recorridos: Kilómetros totales recorridos
    """
    id_estadistica = models.AutoField(primary_key=True, db_column='id_estadistica')
    id_empresa = models.IntegerField(db_column='id_empresa')
    fecha = models.DateField(db_column='fecha', auto_now_add=True)
    total_viajes = models.IntegerField(db_column='total_viajes', default=0)
    viajes_completados = models.IntegerField(db_column='viajes_completados', default=0)
    viajes_cancelados = models.IntegerField(db_column='viajes_cancelados', default=0)
    ingresos_totales = models.DecimalField(max_digits=10, decimal_places=2, db_column='ingresos_totales', default=0)
    calificacion_promedio = models.DecimalField(max_digits=3, decimal_places=2, db_column='calificacion_promedio', default=0)
    pasajeros_transportados = models.IntegerField(db_column='pasajeros_transportados', default=0)
    kilometros_recorridos = models.DecimalField(max_digits=10, decimal_places=2, db_column='kilometros_recorridos', default=0)

    def __str__(self):
        """Retorna la descripción de la estadística como representación en string."""
        return f"Estadísticas de Empresa {self.id_empresa} - {self.fecha}"

    class Meta:
        """Metadatos del modelo EstadisticaEmpresa."""
        db_table = 'EstadisticasEmpresas'
        verbose_name = 'Estadística de Empresa'
        verbose_name_plural = 'Estadísticas de Empresas'
        ordering = ['-fecha']
        unique_together = ['id_empresa', 'fecha']

class VersionSistema(models.Model):
    """
    Modelo para registrar el historial de versiones y cambios del sistema.
    
    Campos:
        id_version: Identificador único de la versión
        numero_version: Número de versión (formato: X.Y.Z)
        fecha_lanzamiento: Fecha de lanzamiento de la versión
        tipo_cambio: Tipo de cambio (mayor, menor, parche)
        descripcion: Descripción general de la versión
        cambios: Lista detallada de cambios implementados
        desarrollador: Usuario que implementó los cambios
        estado: Estado de la versión (desarrollo, pruebas, producción)
    """
    TIPOS_CAMBIO = [
        ('mayor', 'Cambio Mayor'),
        ('menor', 'Cambio Menor'),
        ('parche', 'Parche')
    ]
    
    ESTADOS = [
        ('desarrollo', 'En Desarrollo'),
        ('pruebas', 'En Pruebas'),
        ('produccion', 'En Producción')
    ]
    
    id_version = models.AutoField(primary_key=True, db_column='id_version')
    numero_version = models.CharField(max_length=20, db_column='numero_version', unique=True)
    fecha_lanzamiento = models.DateTimeField(db_column='fecha_lanzamiento', auto_now_add=True)
    tipo_cambio = models.CharField(max_length=10, choices=TIPOS_CAMBIO, db_column='tipo_cambio')
    descripcion = models.TextField(db_column='descripcion')
    cambios = models.JSONField(db_column='cambios')  # Almacena lista de cambios en formato JSON
    desarrollador = models.ForeignKey(Usuario, on_delete=models.PROTECT, db_column='Usuarios_id_desarrollador')
    estado = models.CharField(max_length=20, choices=ESTADOS, default='desarrollo', db_column='estado')

    def __str__(self):
        """Retorna la descripción de la versión como representación en string."""
        return f"Versión {self.numero_version} - {self.get_tipo_cambio_display()}"

    class Meta:
        """Metadatos del modelo VersionSistema."""
        db_table = 'VersionesSistema'
        verbose_name = 'Versión del Sistema'
        verbose_name_plural = 'Versiones del Sistema'
        ordering = ['-fecha_lanzamiento']

class IntentoLogin(models.Model):
    """
    Modelo para registrar los intentos de inicio de sesión.
    
    Campos:
        id_intento: Identificador único del intento
        correo_electronico: Correo electrónico utilizado en el intento
        fecha_intento: Fecha y hora del intento
        ip_address: Dirección IP desde donde se realizó el intento
        exitoso: Indica si el intento fue exitoso
        bloqueado: Indica si la cuenta está bloqueada
        fecha_desbloqueo: Fecha y hora en que se desbloqueará la cuenta
    """
    id_intento = models.AutoField(primary_key=True, db_column='id_intento')
    correo_electronico = models.EmailField(db_column='correo_electronico')
    fecha_intento = models.DateTimeField(db_column='fecha_intento', auto_now_add=True)
    ip_address = models.GenericIPAddressField(db_column='ip_address')
    exito = models.BooleanField(db_column='exito', default=False)
    bloqueado = models.BooleanField(db_column='bloqueado', default=False)
    fecha_desbloqueo = models.DateTimeField(db_column='fecha_desbloqueo', null=True, blank=True)

    def __str__(self):
        """Retorna la descripción del intento como representación en string."""
        return f"Intento de {self.correo_electronico} - {'Exitoso' if self.exito else 'Fallido'}"

    class Meta:
        """Metadatos del modelo IntentoLogin."""
        db_table = 'IntentosLogin'
        verbose_name = 'Intento de Login'
        verbose_name_plural = 'Intentos de Login'
        ordering = ['-fecha_intento']

class PQRS(models.Model):
    """
    Modelo para registrar las Peticiones, Quejas, Reclamos y Sugerencias.
    
    Campos:
        id_pqrs: Identificador único de la PQRS
        id_usuario: Referencia al usuario que realiza la PQRS
        tipo: Tipo de PQRS (peticion, queja, reclamo, sugerencia)
        asunto: Asunto de la PQRS
        descripcion: Descripción detallada
        estado: Estado de la PQRS (pendiente, en_proceso, resuelto)
        fecha_creacion: Fecha de creación
        fecha_respuesta: Fecha de respuesta
        respuesta: Respuesta a la PQRS
        respondido_por: Usuario que respondió
    """
    TIPOS = [
        ('peticion', 'Petición'),
        ('queja', 'Queja'),
        ('reclamo', 'Reclamo'),
        ('sugerencia', 'Sugerencia')
    ]
    
    ESTADOS = [
        ('pendiente', 'Pendiente'),
        ('en_proceso', 'En Proceso'),
        ('resuelto', 'Resuelto')
    ]
    
    id_pqrs = models.AutoField(primary_key=True, db_column='id_pqrs')
    id_usuario = models.ForeignKey(Usuario, on_delete=models.PROTECT, db_column='Usuarios_id_usuario')
    tipo = models.CharField(max_length=20, choices=TIPOS, db_column='tipo')
    asunto = models.CharField(max_length=200, db_column='asunto')
    descripcion = models.TextField(db_column='descripcion')
    estado = models.CharField(max_length=20, choices=ESTADOS, default='pendiente', db_column='estado')
    fecha_creacion = models.DateTimeField(db_column='fecha_creacion', auto_now_add=True)
    fecha_respuesta = models.DateTimeField(db_column='fecha_respuesta', null=True, blank=True)
    respuesta = models.TextField(db_column='respuesta', null=True, blank=True)
    respondido_por = models.ForeignKey(Usuario, on_delete=models.PROTECT, null=True, blank=True, 
                                     related_name='pqrs_respondidas', db_column='Usuarios_id_respondido_por')

    def __str__(self):
        """Retorna la descripción de la PQRS como representación en string."""
        return f"{self.get_tipo_display()} - {self.asunto}"

    class Meta:
        """Metadatos del modelo PQRS."""
        db_table = 'PQRS'
        verbose_name = 'PQRS'
        verbose_name_plural = 'PQRS'
        ordering = ['-fecha_creacion']
