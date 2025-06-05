from rest_framework import serializers
from .models import Usuario, Vehiculo, Conductor, Ruta, Calificacion, Zona, Tarifa, Rol, Viaje, RutaFavorita, CalificacionConductor, EstadisticaEmpresa, VersionSistema, IntentoLogin, PQRS
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class RolSerializer(serializers.ModelSerializer):
    """
    Serializador para el modelo Rol.
    
    Convierte instancias del modelo Rol a JSON y viceversa.
    Maneja la validación y conversión de datos para operaciones CRUD.
    
    Campos:
        id_rol: Identificador único del rol
        nombre: Nombre del rol
        descripcion: Descripción detallada del rol
    """
    class Meta:
        model = Rol
        fields = ['id_rol', 'nombre', 'descripcion']
        read_only_fields = ['id_rol']

class UsuarioSerializer(serializers.ModelSerializer):
    """
    Serializador para el modelo Usuario.
    
    Convierte instancias del modelo Usuario a JSON y viceversa.
    Maneja la validación y conversión de datos para operaciones CRUD.
    
    Campos:
        id_usuario: Identificador único del usuario
        correo_electronico: Correo electrónico del usuario
        nombre: Nombre completo del usuario
        rol: Rol asignado al usuario
        is_active: Estado de activación del usuario
        is_staff: Indica si el usuario es parte del staff
    """
    rol_nombre = serializers.CharField(source='rol.nombre', read_only=True)
    contrasena = serializers.CharField(write_only=True, required=True)
    
    class Meta:
        model = Usuario
        fields = ['id_usuario', 'correo_electronico', 'nombre', 'rol', 'rol_nombre', 'is_active', 'is_staff', 'contrasena']
        read_only_fields = ['id_usuario']

    def create(self, validated_data):
        contrasena = validated_data.pop('contrasena', None)
        usuario = Usuario(**validated_data)
        if contrasena:
            usuario.set_password(contrasena)
        usuario.save()
        return usuario

    def update(self, instance, validated_data):
        contrasena = validated_data.pop('contrasena', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if contrasena:
            instance.set_password(contrasena)
        instance.save()
        return instance

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
        Valida las credenciales del usuario.
        
        Args:
            attrs (dict): Atributos a validar
            
        Returns:
            dict: Atributos validados
            
        Raises:
            serializers.ValidationError: Si las credenciales son inválidas
        """
        try:
            # Primero verificamos si el usuario existe
            correo_electronico = attrs.get('correo_electronico')
            if not Usuario.objects.filter(correo_electronico=correo_electronico).exists():
                raise serializers.ValidationError({'correo_electronico': 'Usuario no encontrado'})
            
            # Llamamos al método validate del padre para validar la contraseña
            data = super().validate(attrs)
            
            # Verificamos si el usuario está activo
            user = self.user
            if not user.is_active:
                raise serializers.ValidationError({'correo_electronico': 'Usuario inactivo'})
            
            return data
        except serializers.ValidationError as e:
            raise e
        except Exception as e:
            raise serializers.ValidationError({'correo_electronico': 'Credenciales inválidas'})

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

class ZonaSerializer(serializers.ModelSerializer):
    """
    Serializador para el modelo Zona.
    
    Convierte instancias del modelo Zona a JSON y viceversa.
    Maneja la validación y conversión de datos para operaciones CRUD.
    
    Campos:
        id_zona: Identificador único de la zona
        nombre: Nombre de la zona
        descripcion: Descripción detallada de la zona
        activa: Estado de activación de la zona
    """
    class Meta:
        model = Zona
        fields = ['id_zona', 'nombre', 'descripcion', 'activa']
        read_only_fields = ['id_zona']

class TarifaSerializer(serializers.ModelSerializer):
    """
    Serializador para el modelo Tarifa.
    
    Convierte instancias del modelo Tarifa a JSON y viceversa.
    Incluye validación de datos y manejo de relaciones.
    
    Campos:
        id_tarifa: Identificador único de la tarifa
        zona_origen: Zona de origen del viaje
        zona_destino: Zona de destino del viaje
        precio_base: Precio base del viaje
        precio_km: Precio por kilómetro adicional
        activa: Estado de activación de la tarifa
        fecha_actualizacion: Fecha de última actualización
        actualizado_por: Usuario que realizó la última actualización
    """
    zona_origen_nombre = serializers.CharField(source='zona_origen.nombre', read_only=True)
    zona_destino_nombre = serializers.CharField(source='zona_destino.nombre', read_only=True)
    actualizado_por_nombre = serializers.CharField(source='actualizado_por.nombre', read_only=True)

    class Meta:
        model = Tarifa
        fields = ['id_tarifa', 'zona_origen', 'zona_origen_nombre', 'zona_destino', 'zona_destino_nombre',
                 'precio_base', 'precio_km', 'activa', 'fecha_actualizacion', 'actualizado_por', 'actualizado_por_nombre']
        read_only_fields = ['id_tarifa', 'fecha_actualizacion', 'actualizado_por']

    def validate(self, data):
        """
        Valida que la zona de origen y destino sean diferentes.
        
        Args:
            data (dict): Datos a validar
            
        Returns:
            dict: Datos validados
            
        Raises:
            serializers.ValidationError: Si las zonas son iguales
        """
        if data.get('zona_origen') == data.get('zona_destino'):
            raise serializers.ValidationError("La zona de origen y destino no pueden ser la misma")
        return data

class ViajeSerializer(serializers.ModelSerializer):
    """
    Serializador para el modelo Viaje.
    
    Convierte instancias del modelo Viaje a JSON y viceversa.
    Incluye información detallada de la ruta y el usuario.
    
    Campos:
        id_viaje: Identificador único del viaje
        id_ruta: Referencia a la ruta del viaje
        id_usuario: Referencia al pasajero
        fecha_viaje: Fecha en que se realizó el viaje
        estado: Estado del viaje
        precio_final: Precio final del viaje
        calificacion: Referencia a la calificación del viaje
        ruta_detalle: Detalles de la ruta (nombre, origen, destino, horario)
        usuario_nombre: Nombre del pasajero
    """
    ruta_detalle = RutaSerializer(source='id_ruta', read_only=True)
    usuario_nombre = serializers.CharField(source='id_usuario.nombre', read_only=True)
    calificacion_detalle = CalificacionSerializer(source='calificacion', read_only=True)

    class Meta:
        model = Viaje
        fields = ['id_viaje', 'id_ruta', 'id_usuario', 'fecha_viaje', 'estado', 
                 'precio_final', 'calificacion', 'ruta_detalle', 'usuario_nombre',
                 'calificacion_detalle']
        read_only_fields = ['id_viaje', 'fecha_viaje', 'calificacion']

class RutaFavoritaSerializer(serializers.ModelSerializer):
    """
    Serializador para el modelo RutaFavorita.
    
    Convierte instancias del modelo RutaFavorita a JSON y viceversa.
    Incluye información detallada de la ruta y el usuario.
    
    Campos:
        id_ruta_favorita: Identificador único de la ruta favorita
        id_usuario: Referencia al usuario que marcó la ruta como favorita
        id_ruta: Referencia a la ruta marcada como favorita
        fecha_agregada: Fecha en que se marcó la ruta como favorita
        ruta_detalle: Detalles de la ruta (nombre, origen, destino, horario)
        usuario_nombre: Nombre del usuario
    """
    ruta_detalle = RutaSerializer(source='id_ruta', read_only=True)
    usuario_nombre = serializers.CharField(source='id_usuario.nombre', read_only=True)

    class Meta:
        model = RutaFavorita
        fields = ['id_ruta_favorita', 'id_usuario', 'id_ruta', 'fecha_agregada', 
                 'ruta_detalle', 'usuario_nombre']
        read_only_fields = ['id_ruta_favorita', 'fecha_agregada', 'id_usuario']

class CalificacionConductorSerializer(serializers.ModelSerializer):
    """
    Serializador para el modelo CalificacionConductor.
    
    Convierte instancias del modelo CalificacionConductor a JSON y viceversa.
    Incluye información detallada del viaje, usuario y conductor.
    
    Campos:
        id_calificacion_conductor: Identificador único de la calificación
        id_viaje: Referencia al viaje realizado
        id_usuario: Referencia al pasajero que califica
        id_conductor: Referencia al conductor calificado
        calificacion: Puntuación numérica (1-5)
        comentario: Comentario o retroalimentación
        fecha: Fecha de la calificación
        viaje_detalle: Detalles del viaje
        usuario_nombre: Nombre del pasajero
        conductor_nombre: Nombre del conductor
    """
    viaje_detalle = ViajeSerializer(source='id_viaje', read_only=True)
    usuario_nombre = serializers.CharField(source='id_usuario.nombre', read_only=True)
    conductor_nombre = serializers.CharField(source='id_conductor.nombre', read_only=True)

    class Meta:
        model = CalificacionConductor
        fields = ['id_calificacion_conductor', 'id_viaje', 'id_usuario', 'id_conductor',
                 'calificacion', 'comentario', 'fecha', 'viaje_detalle', 'usuario_nombre',
                 'conductor_nombre']
        read_only_fields = ['id_calificacion_conductor', 'fecha', 'id_usuario']

    def validate_calificacion(self, value):
        """
        Valida que la calificación esté dentro del rango permitido (1-5).
        
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

class EstadisticaEmpresaSerializer(serializers.ModelSerializer):
    """
    Serializador para el modelo EstadisticaEmpresa.
    
    Convierte instancias del modelo EstadisticaEmpresa a JSON y viceversa.
    Incluye validación de datos y formateo de campos numéricos.
    
    Campos:
        id_estadistica: Identificador único de la estadística
        id_empresa: ID de la empresa
        fecha: Fecha de la estadística
        total_viajes: Número total de viajes
        viajes_completados: Número de viajes completados
        viajes_cancelados: Número de viajes cancelados
        ingresos_totales: Ingresos totales generados
        calificacion_promedio: Calificación promedio de conductores
        pasajeros_transportados: Número total de pasajeros
        kilometros_recorridos: Kilómetros totales recorridos
    """
    class Meta:
        model = EstadisticaEmpresa
        fields = ['id_estadistica', 'id_empresa', 'fecha', 'total_viajes',
                 'viajes_completados', 'viajes_cancelados', 'ingresos_totales',
                 'calificacion_promedio', 'pasajeros_transportados', 'kilometros_recorridos']
        read_only_fields = ['id_estadistica', 'fecha']

    def validate(self, data):
        """
        Valida que los datos de la estadística sean coherentes.
        
        Args:
            data (dict): Datos a validar
            
        Returns:
            dict: Datos validados
            
        Raises:
            serializers.ValidationError: Si los datos no son coherentes
        """
        if data.get('viajes_completados', 0) + data.get('viajes_cancelados', 0) > data.get('total_viajes', 0):
            raise serializers.ValidationError("La suma de viajes completados y cancelados no puede ser mayor al total de viajes")
        return data

class VersionSistemaSerializer(serializers.ModelSerializer):
    """
    Serializador para el modelo VersionSistema.
    
    Convierte instancias del modelo VersionSistema a JSON y viceversa.
    Incluye validación de datos y formateo de campos.
    
    Campos:
        id_version: Identificador único de la versión
        numero_version: Número de versión (formato: X.Y.Z)
        fecha_lanzamiento: Fecha de lanzamiento
        tipo_cambio: Tipo de cambio (mayor, menor, parche)
        descripcion: Descripción general
        cambios: Lista detallada de cambios
        desarrollador: Usuario que implementó los cambios
        estado: Estado de la versión
        desarrollador_nombre: Nombre del desarrollador
    """
    desarrollador_nombre = serializers.CharField(source='desarrollador.nombre', read_only=True)

    class Meta:
        model = VersionSistema
        fields = ['id_version', 'numero_version', 'fecha_lanzamiento', 'tipo_cambio',
                 'descripcion', 'cambios', 'desarrollador', 'desarrollador_nombre', 'estado']
        read_only_fields = ['id_version', 'fecha_lanzamiento', 'desarrollador']

    def validate_numero_version(self, value):
        """
        Valida el formato del número de versión (X.Y.Z).
        
        Args:
            value (str): Número de versión a validar
            
        Returns:
            str: Número de versión si es válido
            
        Raises:
            serializers.ValidationError: Si el formato no es válido
        """
        import re
        if not re.match(r'^\d+\.\d+\.\d+$', value):
            raise serializers.ValidationError(
                "El número de versión debe seguir el formato X.Y.Z (por ejemplo: 1.0.0)"
            )
        return value

    def validate_cambios(self, value):
        """
        Valida que los cambios sean una lista de diccionarios con la estructura correcta.
        
        Args:
            value (list): Lista de cambios a validar
            
        Returns:
            list: Lista de cambios si es válida
            
        Raises:
            serializers.ValidationError: Si la estructura no es válida
        """
        if not isinstance(value, list):
            raise serializers.ValidationError("Los cambios deben ser una lista")
        
        for cambio in value:
            if not isinstance(cambio, dict):
                raise serializers.ValidationError("Cada cambio debe ser un diccionario")
            if 'tipo' not in cambio or 'descripcion' not in cambio:
                raise serializers.ValidationError(
                    "Cada cambio debe tener 'tipo' y 'descripcion'"
                )
        return value

class IntentoLoginSerializer(serializers.ModelSerializer):
    """
    Serializador para el modelo IntentoLogin.
    
    Convierte instancias del modelo IntentoLogin a JSON y viceversa.
    Incluye validación de datos y formateo de campos.
    
    Campos:
        id_intento: Identificador único del intento
        correo_electronico: Correo electrónico utilizado
        fecha_intento: Fecha y hora del intento
        ip_address: Dirección IP del intento
        exito: Estado del intento
        bloqueado: Estado de bloqueo
        fecha_desbloqueo: Fecha de desbloqueo
    """
    class Meta:
        model = IntentoLogin
        fields = ['id_intento', 'correo_electronico', 'fecha_intento', 'ip_address',
                 'exito', 'bloqueado', 'fecha_desbloqueo']
        read_only_fields = ['id_intento', 'fecha_intento', 'bloqueado', 'fecha_desbloqueo']

class PQRSSerializer(serializers.ModelSerializer):
    """
    Serializador para el modelo PQRS.
    
    Este serializador maneja la conversión de instancias PQRS a JSON y viceversa.
    Incluye validación de datos y campos de solo lectura.
    
    Campos:
    - id_pqrs: Identificador único de la PQRS
    - id_usuario: Usuario que creó la PQRS
    - tipo: Tipo de PQRS (petición, queja, reclamo, sugerencia)
    - asunto: Título de la PQRS
    - descripcion: Detalle de la PQRS
    - fecha_creacion: Fecha y hora de creación
    - estado: Estado actual de la PQRS
    - respuesta: Respuesta del administrador
    - fecha_respuesta: Fecha y hora de la respuesta
    - respondido_por: Administrador que respondió
    """
    usuario_nombre = serializers.CharField(source='id_usuario.nombre', read_only=True)
    respondido_por_nombre = serializers.CharField(source='respondido_por.nombre', read_only=True)
    
    class Meta:
        model = PQRS
        fields = [
            'id_pqrs', 'id_usuario', 'usuario_nombre', 'tipo', 'asunto',
            'descripcion', 'fecha_creacion', 'estado', 'respuesta',
            'fecha_respuesta', 'respondido_por', 'respondido_por_nombre'
        ]
        read_only_fields = ['id_pqrs', 'fecha_creacion', 'estado', 'fecha_respuesta']
        
    def validate_tipo(self, value):
        """
        Valida que el tipo de PQRS sea válido.
        
        Args:
            value: Tipo de PQRS a validar
            
        Returns:
            str: Tipo de PQRS validado
            
        Raises:
            serializers.ValidationError: Si el tipo no es válido
        """
        tipos_validos = ['peticion', 'queja', 'reclamo', 'sugerencia']
        if value not in tipos_validos:
            raise serializers.ValidationError(
                f"El tipo debe ser uno de: {', '.join(tipos_validos)}"
            )
        return value
        
    def validate_estado(self, value):
        """
        Valida que el estado de la PQRS sea válido.
        
        Args:
            value: Estado de la PQRS a validar
            
        Returns:
            str: Estado validado
            
        Raises:
            serializers.ValidationError: Si el estado no es válido
        """
        estados_validos = ['pendiente', 'en_proceso', 'resuelto']
        if value not in estados_validos:
            raise serializers.ValidationError(
                f"El estado debe ser uno de: {', '.join(estados_validos)}"
            )
        return value
