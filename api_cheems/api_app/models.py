from django.db import models

class Usuario(models.Model):
    id_usuario = models.AutoField(primary_key=True, db_column='id_usuario')
    nombre = models.CharField(max_length=100, db_column='nombre')
    correo_electronico = models.EmailField(max_length=100, db_column='correo_electronico')
    contrasena = models.IntegerField(db_column='contrasena')

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
    disponibilidad = models.BooleanField(default=True, db_column='disponibilidad')  # NUEVO CAMPO

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
