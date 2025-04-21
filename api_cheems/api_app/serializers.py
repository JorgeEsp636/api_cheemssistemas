from rest_framework import serializers
from .models import Usuario, Vehiculo, Conductor, Ruta, Calificacion

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ['id_usuario', 'correo_electronico', 'nombre', 'contrasena']

class VehiculoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehiculo
        fields = ['placa', 'empresa', 'disponibilidad']

class ConductorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Conductor
        fields = '__all__'

class RutaSerializer(serializers.ModelSerializer):
    vehiculo = VehiculoSerializer(source='id_vehiculos')  # Relación con el vehículo

    class Meta:
        model = Ruta
        fields = ['nombre_ruta', 'origen', 'destino', 'horario', 'vehiculo']

class CalificacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Calificacion
        fields = '__all__'
