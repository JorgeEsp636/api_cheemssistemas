from rest_framework import serializers
from .models import Usuario, Vehiculo, Conductor, Ruta, Calificacion
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class UsuarioSerializer(serializers.ModelSerializer):
    """
    Serializador para el modelo Usuario.
    
    Convierte instancias del modelo Usuario a JSON y viceversa.
    Maneja la validación y conversión de datos para operaciones CRUD.
    
    Campos:
        id_usuario: Identificador único del usuario
        correo_electronico: Correo electrónico del usuario
        nombre: Nombre completo del usuario
        is_active: Estado de activación del usuario
        is_staff: Indica si el usuario es parte del staff
    """
    class Meta:
        model = Usuario
        fields = ['id_usuario', 'correo_electronico', 'nombre', 'is_active', 'is_staff']
        read_only_fields = ['id_usuario']

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Serializador personalizado para la autenticación.
    
    Este serializador extiende TokenObtainPairSerializer para personalizar el proceso de autenticación:
    1. Usa correo_electronico en lugar de username como identificador
    2. Acepta contrasena en lugar de password
    3. Mapea internamente contrasena a password para la autenticación
    
    El mapeo se realiza en el método to_internal_value para asegurar que el campo
    password esté disponible antes de la validación.
    
    Campos esperados:
        correo_electronico: Correo electrónico del usuario
        contrasena: Contraseña del usuario
    """
    username_field = 'correo_electronico'
    password_field = 'contrasena'

    def to_internal_value(self, data):
        """
        Convierte los datos de entrada antes de la validación.
        
        Mapea el campo 'contrasena' a 'password' para que sea compatible
        con el sistema de autenticación de Django.
        
        Args:
            data (dict): Datos de entrada del request
            
        Returns:
            dict: Datos procesados con el campo password
        """
        if 'contrasena' in data:
            data = data.copy()
            data['password'] = data.pop('contrasena')
        return super().to_internal_value(data)

    def validate(self, attrs):
        """
        Valida los datos de autenticación.
        
        Args:
            attrs (dict): Atributos validados
            
        Returns:
            dict: Datos validados con tokens de acceso
        """
        return super().validate(attrs)

class VehiculoSerializer(serializers.ModelSerializer):
    """
    Serializador para el modelo Vehiculo.
    
    Convierte instancias del modelo Vehiculo a JSON y viceversa.
    Incluye validación de datos y manejo de relaciones.
    
    Campos:
        id_vehiculos: Identificador único del vehículo
        placa: Placa del vehículo
        empresa: ID de la empresa propietaria
        disponibilidad: Estado de disponibilidad del vehículo
    """
    class Meta:
        model = Vehiculo
        fields = ['id_vehiculos', 'placa', 'empresa', 'disponibilidad']
        read_only_fields = ['id_vehiculos']

class ConductorSerializer(serializers.ModelSerializer):
    """
    Serializador para el modelo Conductor.
    
    Convierte instancias del modelo Conductor a JSON y viceversa.
    Incluye la relación con el vehículo asignado.
    
    Campos:
        id_conductor: Identificador único del conductor
        id_vehiculos: Referencia al vehículo asignado
        nombre: Nombre completo del conductor
        licencia_conduccion: Número de licencia de conducción
    """
    class Meta:
        model = Conductor
        fields = ['id_conductor', 'id_vehiculos', 'nombre', 'licencia_conduccion']
        read_only_fields = ['id_conductor']

class RutaSerializer(serializers.ModelSerializer):
    """
    Serializador para el modelo Ruta.
    
    Convierte instancias del modelo Ruta a JSON y viceversa.
    Incluye la relación con el vehículo asignado y manejo de horarios.
    
    Campos:
        id_ruta: Identificador único de la ruta
        id_vehiculos: Referencia al vehículo asignado
        nombre_ruta: Nombre descriptivo de la ruta
        origen: Punto de origen
        destino: Punto de destino
        horario: Horario programado
    """
    class Meta:
        model = Ruta
        fields = ['id_ruta', 'id_vehiculos', 'nombre_ruta', 'origen', 'destino', 'horario']
        read_only_fields = ['id_ruta']

class CalificacionSerializer(serializers.ModelSerializer):
    """
    Serializador para el modelo Calificacion.
    
    Convierte instancias del modelo Calificacion a JSON y viceversa.
    Incluye relaciones con ruta y usuario, y validación de calificaciones.
    
    Campos:
        id_calificaciones: Identificador único de la calificación
        id_ruta: Referencia a la ruta calificada
        id_usuario: Referencia al usuario que califica
        calificacion: Puntuación numérica
        comentario: Comentario o retroalimentación
        fecha: Fecha de la calificación
    """
    class Meta:
        model = Calificacion
        fields = ['id_calificaciones', 'id_ruta', 'id_usuario', 'calificacion', 'comentario', 'fecha']
        read_only_fields = ['id_calificaciones', 'fecha']

    def validate_calificacion(self, value):
        """
        Valida que la calificación esté dentro del rango permitido.
        
        Args:
            value (int): Valor de la calificación a validar
            
        Returns:
            int: Valor de la calificación si es válido
            
        Raises:
            serializers.ValidationError: Si la calificación está fuera del rango
        """
        if value < 1 or value > 5:
            raise serializers.ValidationError("La calificación debe estar entre 1 y 5")
        return value
