from django.shortcuts import render
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import generics, status
from .models import Usuario, Vehiculo, Conductor, Ruta, Calificacion, Zona, Tarifa, Rol
from .serializers import (UsuarioSerializer,VehiculoSerializer, ConductorSerializer, RutaSerializer,CalificacionSerializer, CustomTokenObtainPairSerializer, RolSerializer, ZonaSerializer, TarifaSerializer)
from django.core.mail import send_mail
from django.conf import settings
from .models import Usuario
from .utils.token import generar_token, verificar_token 
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.hashers import make_password
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework_simplejwt.views import TokenObtainPairView
import csv
import io
from datetime import datetime
from django.db import transaction
from django.http import HttpResponse

class UsuarioList(generics.ListCreateAPIView):
    """
    Vista para manejar la lista de usuarios y su creación.
    
    Esta vista permite:
    - GET: Obtener la lista de todos los usuarios registrados
    - POST: Crear un nuevo usuario
    
    Requiere autenticación para acceder a cualquiera de los métodos.
    """
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
    permission_classes = [IsAuthenticated]

class UsuarioDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Vista para manejar operaciones CRUD sobre un usuario específico.
    
    Esta vista permite:
    - GET: Obtener los detalles de un usuario específico
    - PUT/PATCH: Actualizar los datos de un usuario
    - DELETE: Eliminar un usuario
    
    Requiere autenticación para acceder a cualquiera de los métodos.
    """
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
    permission_classes = [IsAuthenticated]

class VehiculoList(generics.ListCreateAPIView):
    """
    Vista para manejar la lista de vehículos y su creación.
    
    Esta vista permite:
    - GET: Obtener la lista de todos los vehículos registrados
    - POST: Crear un nuevo vehículo
    
    Requiere autenticación para acceder a cualquiera de los métodos.
    """
    queryset = Vehiculo.objects.all()
    serializer_class = VehiculoSerializer
    permission_classes = [IsAuthenticated]

class VehiculoDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Vista para manejar operaciones CRUD sobre un vehículo específico.
    
    Esta vista permite:
    - GET: Obtener los detalles de un vehículo específico
    - PUT/PATCH: Actualizar los datos de un vehículo
    - DELETE: Eliminar un vehículo
    
    Requiere autenticación para acceder a cualquiera de los métodos.
    """
    queryset = Vehiculo.objects.all()
    serializer_class = VehiculoSerializer
    permission_classes = [IsAuthenticated]

class ConductorList(generics.ListCreateAPIView):
    """
    Vista para manejar la lista de conductores y su creación.
    
    Esta vista permite:
    - GET: Obtener la lista de todos los conductores registrados
    - POST: Crear un nuevo conductor
    
    Requiere autenticación para acceder a cualquiera de los métodos.
    """
    queryset = Conductor.objects.all()
    serializer_class = ConductorSerializer
    permission_classes = [IsAuthenticated]

class ConductorDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Vista para manejar operaciones CRUD sobre un conductor específico.
    
    Esta vista permite:
    - GET: Obtener los detalles de un conductor específico
    - PUT/PATCH: Actualizar los datos de un conductor
    - DELETE: Eliminar un conductor
    
    Requiere autenticación para acceder a cualquiera de los métodos.
    """
    queryset = Conductor.objects.all()
    serializer_class = ConductorSerializer
    permission_classes = [IsAuthenticated]

class RutaList(generics.ListCreateAPIView):
    """
    Vista para manejar la lista de rutas y su creación.
    
    Esta vista permite:
    - GET: Obtener la lista de todas las rutas registradas
    - POST: Crear una nueva ruta
    
    Características especiales:
    - Permite filtrar rutas por origen y destino
    - Utiliza select_related para optimizar las consultas a la base de datos
    """
    serializer_class = RutaSerializer

    def get_queryset(self):
        """
        Método para obtener y filtrar las rutas.
        
        Filtros disponibles:
        - origen: Filtra rutas que contengan el texto especificado en el origen
        - destino: Filtra rutas que contengan el texto especificado en el destino
        
        Returns:
            QuerySet: Conjunto de rutas filtradas según los parámetros
        """
        queryset = Ruta.objects.all().select_related('id_vehiculos') 
        origen = self.request.query_params.get('origen')
        destino = self.request.query_params.get('destino')

        if origen:
            queryset = queryset.filter(origen__icontains=origen)
        if destino:
            queryset = queryset.filter(destino__icontains=destino)

        return queryset

class RutaDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Vista para manejar operaciones CRUD sobre una ruta específica.
    
    Esta vista permite:
    - GET: Obtener los detalles de una ruta específica
    - PUT/PATCH: Actualizar los datos de una ruta
    - DELETE: Eliminar una ruta
    
    Requiere autenticación para acceder a cualquiera de los métodos.
    """
    queryset = Ruta.objects.all()
    serializer_class = RutaSerializer
    permission_classes = [IsAuthenticated]

class CalificacionList(generics.ListCreateAPIView):
    """
    Vista para manejar la lista de calificaciones y su creación.
    
    Esta vista permite:
    - GET: Obtener la lista de todas las calificaciones registradas
    - POST: Crear una nueva calificación
    
    Características especiales:
    - Permite filtrar calificaciones por usuario y ruta
    - Requiere autenticación para acceder
    """
    queryset = Calificacion.objects.all()
    serializer_class = CalificacionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Método para obtener y filtrar las calificaciones.
        
        Filtros disponibles:
        - usuario: Filtra calificaciones por ID de usuario
        - ruta: Filtra calificaciones por ID de ruta
        
        Returns:
            QuerySet: Conjunto de calificaciones filtradas según los parámetros
        """
        queryset = super().get_queryset()
        usuario_id = self.request.query_params.get('usuario')
        ruta_id = self.request.query_params.get('ruta')
        if usuario_id:
            queryset = queryset.filter(id_usuario_id=usuario_id)
        if ruta_id:
            queryset = queryset.filter(id_ruta_id=ruta_id)
        return queryset

class CalificacionDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Vista para manejar operaciones CRUD sobre una calificación específica.
    
    Esta vista permite:
    - GET: Obtener los detalles de una calificación específica
    - PUT/PATCH: Actualizar los datos de una calificación
    - DELETE: Eliminar una calificación
    
    Requiere autenticación para acceder a cualquiera de los métodos.
    """
    queryset = Calificacion.objects.all()
    serializer_class = CalificacionSerializer
    permission_classes = [IsAuthenticated]

# Esta es la vista para que el usuario pueda recuperar contraseña
class RecuperarContrasenaView(APIView):
    """
    Vista para manejar la recuperación de contraseña de usuarios.
    
    Esta vista permite:
    - POST: Solicitar la recuperación de contraseña
    
    Proceso:
    1. Recibe el correo electrónico del usuario
    2. Genera un token único
    3. Envía un correo con el enlace para restablecer la contraseña
    
    Respuestas:
    - 200: Correo enviado exitosamente
    - 404: Usuario no encontrado
    """
    def post(self, request):
        """
        Método para procesar la solicitud de recuperación de contraseña.
        
        Args:
            request: Objeto Request con el correo electrónico del usuario
            
        Returns:
            Response: Respuesta con el estado de la operación
        """
        email = request.data.get('correo_electronico')
        try:
            usuario = Usuario.objects.get(correo_electronico=email)
            token = generar_token(email)
            link = f"http://localhost:8000/api/auth/restablecer-contrasena/?token={token}"
            send_mail(
                subject="Recupera tu contraseña",
                message=f"Haz clic en el siguiente enlace para restablecer tu contraseña: {link}",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[email],
                fail_silently=False
            )
            return Response({'confirmación': 'Correo enviado con instrucciones'}, status=status.HTTP_200_OK)
        except Usuario.DoesNotExist:
            return Response({'error': 'Usuario no encontrado'}, status=status.HTTP_404_NOT_FOUND)

# Esta es la vista para que el usuario pueda restablecer la contraseña
class RestablecerContrasenaView(APIView):
    """
    Vista para manejar el restablecimiento de contraseña.
    
    Esta vista permite:
    - POST: Restablecer la contraseña usando el token recibido
    
    Proceso:
    1. Verifica el token recibido
    2. Actualiza la contraseña del usuario
    3. Confirma la actualización
    
    Respuestas:
    - 200: Contraseña actualizada exitosamente
    - 400: Token inválido o expirado
    - 404: Usuario no encontrado
    """
    def post(self, request):
        """
        Método para procesar el restablecimiento de contraseña.
        
        Args:
            request: Objeto Request con la nueva contraseña y el token
            
        Returns:
            Response: Respuesta con el estado de la operación
        """
        token = request.query_params.get('token')
        nueva_contrasena = request.data.get('nueva_contrasena')

        email = verificar_token(token)
        if email:
            try:
                usuario = Usuario.objects.get(correo_electronico=email)
                usuario.contrasena = make_password(nueva_contrasena)
                usuario.save()
                return Response({'confirmación': 'Su contraseña actualizada correctamente'}, status=status.HTTP_200_OK)
            except Usuario.DoesNotExist:
                return Response({'error': 'Usuario no encontrado'}, status=status.HTTP_404_NOT_FOUND)
        return Response({'error': 'Token inválido o expirado'}, status=status.HTTP_400_BAD_REQUEST)

class CustomTokenObtainPairView(TokenObtainPairView):
    """
    Vista personalizada para la autenticación.
    
    Usa el serializer CustomTokenObtainPairSerializer para autenticar con correo_electronico y contrasena.
    """
    serializer_class = CustomTokenObtainPairSerializer

class RolList(generics.ListCreateAPIView):
    """
    Vista para manejar la lista de roles y su creación.
    
    Esta vista permite:
    - GET: Obtener la lista de todos los roles registrados
    - POST: Crear un nuevo rol
    
    Requiere autenticación y permisos de administrador para acceder.
    """
    queryset = Rol.objects.all()
    serializer_class = RolSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

class RolDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Vista para manejar operaciones CRUD sobre un rol específico.
    
    Esta vista permite:
    - GET: Obtener los detalles de un rol específico
    - PUT/PATCH: Actualizar los datos de un rol
    - DELETE: Eliminar un rol
    
    Requiere autenticación y permisos de administrador para acceder.
    """
    queryset = Rol.objects.all()
    serializer_class = RolSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

class ZonaList(generics.ListCreateAPIView):
    """
    Vista para manejar la lista de zonas y su creación.
    
    Esta vista permite:
    - GET: Obtener la lista de todas las zonas registradas
    - POST: Crear una nueva zona
    
    Requiere autenticación y permisos de administrador para acceder.
    """
    queryset = Zona.objects.all()
    serializer_class = ZonaSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

class ZonaDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Vista para manejar operaciones CRUD sobre una zona específica.
    
    Esta vista permite:
    - GET: Obtener los detalles de una zona específica
    - PUT/PATCH: Actualizar los datos de una zona
    - DELETE: Eliminar una zona
    
    Requiere autenticación y permisos de administrador para acceder.
    """
    queryset = Zona.objects.all()
    serializer_class = ZonaSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

class TarifaList(generics.ListCreateAPIView):
    """
    Vista para manejar la lista de tarifas y su creación.
    
    Esta vista permite:
    - GET: Obtener la lista de todas las tarifas registradas
    - POST: Crear una nueva tarifa
    
    Características especiales:
    - Permite filtrar tarifas por zona de origen y destino
    - Requiere autenticación y permisos de administrador
    """
    serializer_class = TarifaSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get_queryset(self):
        """
        Método para obtener y filtrar las tarifas.
        
        Filtros disponibles:
        - zona_origen: Filtra tarifas por ID de zona de origen
        - zona_destino: Filtra tarifas por ID de zona de destino
        - activa: Filtra tarifas por estado de activación
        
        Returns:
            QuerySet: Conjunto de tarifas filtradas según los parámetros
        """
        queryset = Tarifa.objects.all().select_related('zona_origen', 'zona_destino', 'actualizado_por')
        zona_origen = self.request.query_params.get('zona_origen')
        zona_destino = self.request.query_params.get('zona_destino')
        activa = self.request.query_params.get('activa')

        if zona_origen:
            queryset = queryset.filter(zona_origen_id=zona_origen)
        if zona_destino:
            queryset = queryset.filter(zona_destino_id=zona_destino)
        if activa is not None:
            queryset = queryset.filter(activa=activa.lower() == 'true')

        return queryset

    def perform_create(self, serializer):
        """
        Método para crear una nueva tarifa.
        
        Args:
            serializer: Serializador con los datos de la tarifa
        """
        serializer.save(actualizado_por=self.request.user)

class TarifaDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Vista para manejar operaciones CRUD sobre una tarifa específica.
    
    Esta vista permite:
    - GET: Obtener los detalles de una tarifa específica
    - PUT/PATCH: Actualizar los datos de una tarifa
    - DELETE: Eliminar una tarifa
    
    Requiere autenticación y permisos de administrador para acceder.
    """
    queryset = Tarifa.objects.all()
    serializer_class = TarifaSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

    def perform_update(self, serializer):
        """
        Método para actualizar una tarifa existente.
        
        Args:
            serializer: Serializador con los datos actualizados de la tarifa
        """
        serializer.save(actualizado_por=self.request.user)

class ImportarRutasView(APIView):
    """
    Vista para importar rutas y horarios desde archivos CSV.
    
    Esta vista permite:
    - POST: Importar rutas y horarios desde un archivo CSV
    
    El archivo CSV debe tener el siguiente formato:
    - nombre_ruta: Nombre de la ruta
    - origen: Punto de origen
    - destino: Punto de destino
    - horario: Horario en formato HH:MM
    - placa_vehiculo: Placa del vehículo asignado
    
    Requiere autenticación y permisos de administrador para acceder.
    """
    permission_classes = [IsAuthenticated, IsAdminUser]

    def post(self, request):
        """
        Método para procesar la importación de rutas desde CSV.
        
        Args:
            request: Objeto Request con el archivo CSV
            
        Returns:
            Response: Respuesta con el resultado de la importación
        """
        if 'archivo' not in request.FILES:
            return Response(
                {'error': 'No se proporcionó ningún archivo'},
                status=status.HTTP_400_BAD_REQUEST
            )

        archivo = request.FILES['archivo']
        if not archivo.name.endswith('.csv'):
            return Response(
                {'error': 'El archivo debe ser de tipo CSV'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            contenido = archivo.read().decode('utf-8')
            csv_file = io.StringIO(contenido)
            reader = csv.DictReader(csv_file)

            rutas_creadas = []
            errores = []

            with transaction.atomic():
                for fila in reader:
                    try:
                        campos_requeridos = ['nombre_ruta', 'origen', 'destino', 'horario', 'placa_vehiculo']
                        for campo in campos_requeridos:
                            if campo not in fila or not fila[campo]:
                                raise ValueError(f'El campo {campo} es requerido')

                        # Buscar el vehículo, no crearlo automáticamente
                        try:
                            vehiculo = Vehiculo.objects.get(placa=fila['placa_vehiculo'])
                        except Vehiculo.DoesNotExist:
                            raise ValueError(f'El vehículo con placa {fila["placa_vehiculo"]} no existe')

                        # Convertir horario a objeto time
                        try:
                            horario = datetime.strptime(fila['horario'], '%H:%M').time()
                        except ValueError:
                            raise ValueError(f'Formato de horario inválido: {fila["horario"]}')

                        ruta = Ruta.objects.create(
                            nombre_ruta=fila['nombre_ruta'],
                            origen=fila['origen'],
                            destino=fila['destino'],
                            horario=horario,
                            id_vehiculos=vehiculo
                        )
                        rutas_creadas.append({
                            'id': ruta.id_ruta,
                            'nombre': ruta.nombre_ruta,
                            'origen': ruta.origen,
                            'destino': ruta.destino,
                            'horario': ruta.horario.strftime('%H:%M')
                        })
                    except Exception as e:
                        errores.append({
                            'fila': reader.line_num,
                            'error': str(e)
                        })

            if rutas_creadas and errores:
                return Response({
                    'mensaje': f'Se importaron {len(rutas_creadas)} rutas, pero hubo errores en algunas filas.',
                    'rutas_creadas': rutas_creadas,
                    'errores': errores
                }, status=207)  # 207 Multi-Status
            elif rutas_creadas:
                return Response({
                    'mensaje': f'Se importaron {len(rutas_creadas)} rutas exitosamente',
                    'rutas_creadas': rutas_creadas
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    'error': 'No se pudo importar ninguna ruta',
                    'errores': errores
                }, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response(
                {'error': f'Error al procesar el archivo: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class DescargarPlantillaRutasView(APIView):
    """
    Vista para descargar una plantilla CSV para importar rutas.
    
    Esta vista permite:
    - GET: Descargar una plantilla CSV con los campos necesarios
    
    Requiere autenticación y permisos de administrador para acceder.
    """
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request):
        """
        Método para generar y descargar la plantilla CSV.
        
        Returns:
            HttpResponse: Archivo CSV con la plantilla
        """
        # Crear un buffer en memoria para el archivo CSV
        output = io.StringIO()
        writer = csv.writer(output)
        
        # Escribir encabezados
        writer.writerow(['nombre_ruta', 'origen', 'destino', 'horario', 'placa_vehiculo'])
        
        # Escribir una fila de ejemplo
        writer.writerow(['Ruta 1', 'Zona Norte', 'Zona Sur', '08:00', 'ABC123'])
        
        # Preparar la respuesta
        response = HttpResponse(
            output.getvalue(),
            content_type='text/csv'
        )
        response['Content-Disposition'] = 'attachment; filename="plantilla_rutas.csv"'
        
        return response