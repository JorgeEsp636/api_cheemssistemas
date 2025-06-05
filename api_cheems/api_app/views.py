from django.shortcuts import render
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import generics, status, serializers
from .models import Usuario, Vehiculo, Conductor, Ruta, Calificacion, Zona, Tarifa, Rol, Viaje, RutaFavorita, CalificacionConductor, EstadisticaEmpresa, VersionSistema, IntentoLogin, PQRS
from .serializers import (UsuarioSerializer,VehiculoSerializer, ConductorSerializer, RutaSerializer,CalificacionSerializer, CustomTokenObtainPairSerializer, RolSerializer, ZonaSerializer, TarifaSerializer, ViajeSerializer, RutaFavoritaSerializer, CalificacionConductorSerializer, EstadisticaEmpresaSerializer, VersionSistemaSerializer, PQRSSerializer)
from django.core.mail import send_mail
from django.conf import settings
from .models import Usuario
from .utils.token import generar_token, verificar_token 
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.hashers import make_password
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
import csv
import io
from datetime import datetime
from django.db import transaction
from django.http import HttpResponse
from django.utils import timezone
from django.core.exceptions import PermissionDenied

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
    Vista personalizada para la autenticación con control de intentos fallidos.
    
    Características:
    - Bloquea la cuenta después de 5 intentos fallidos
    - Registra cada intento de inicio de sesión
    - Implementa un tiempo de espera de 30 minutos
    - Registra la IP del usuario
    """
    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        """
        Método para procesar el intento de inicio de sesión.
        
        Args:
            request: Objeto Request con las credenciales
            
        Returns:
            Response: Tokens de acceso o mensaje de error
        """
        correo_electronico = request.data.get('correo_electronico')
        ip_address = self.get_client_ip(request)

        # Verificar si la cuenta está bloqueada
        intentos_recientes = IntentoLogin.objects.filter(
            correo_electronico=correo_electronico,
            fecha_intento__gte=timezone.now() - timezone.timedelta(minutes=30)
        ).order_by('-fecha_intento')

        if intentos_recientes.exists():
            ultimo_intento = intentos_recientes.first()
            if ultimo_intento.bloqueado:
                if ultimo_intento.fecha_desbloqueo and ultimo_intento.fecha_desbloqueo > timezone.now():
                    tiempo_restante = ultimo_intento.fecha_desbloqueo - timezone.now()
                    minutos = int(tiempo_restante.total_seconds() / 60)
                    return Response({
                        'error': f'Cuenta bloqueada. Intente nuevamente en {minutos} minutos.'
                    }, status=status.HTTP_403_FORBIDDEN)

        # Registrar el intento actual
        intento = IntentoLogin.objects.create(
            correo_electronico=correo_electronico,
            ip_address=ip_address
        )

        try:
            response = super().post(request, *args, **kwargs)
            intento.exito = True
            intento.save()
            return response
        except Exception as e:
            # Contar intentos fallidos en los últimos 30 minutos
            intentos_fallidos = intentos_recientes.filter(exito=False).count()
            
            if intentos_fallidos >= 4:  # 4 intentos anteriores + el actual = 5
                # Bloquear la cuenta por 30 minutos
                intento.bloqueado = True
                intento.fecha_desbloqueo = timezone.now() + timezone.timedelta(minutes=30)
                intento.save()
                return Response({
                    'error': 'Cuenta bloqueada por 30 minutos debido a múltiples intentos fallidos.'
                }, status=status.HTTP_403_FORBIDDEN)
            
            intento.save()
            return Response({
                'error': 'Credenciales inválidas',
                'intentos_restantes': 5 - (intentos_fallidos + 1)
            }, status=status.HTTP_401_UNAUTHORIZED)

    def get_client_ip(self, request):
        """
        Obtiene la dirección IP del cliente.
        
        Args:
            request: Objeto Request
            
        Returns:
            str: Dirección IP del cliente
        """
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

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

class ViajeList(generics.ListCreateAPIView):
    """
    Vista para manejar la lista de viajes y su creación.
    
    Esta vista permite:
    - GET: Obtener la lista de viajes del usuario autenticado
    - POST: Crear un nuevo viaje
    
    Características especiales:
    - Filtra automáticamente los viajes por el usuario autenticado
    - Permite filtrar por estado del viaje
    - Incluye detalles completos de la ruta y calificaciones
    """
    serializer_class = ViajeSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Método para obtener y filtrar los viajes.
        
        Filtros disponibles:
        - estado: Filtra viajes por estado (completado, cancelado, en_curso)
        
        Returns:
            QuerySet: Conjunto de viajes filtrados según los parámetros
        """
        queryset = Viaje.objects.filter(id_usuario=self.request.user).select_related(
            'id_ruta', 'id_usuario', 'calificacion'
        )
        estado = self.request.query_params.get('estado')
        if estado:
            queryset = queryset.filter(estado=estado)
        return queryset

    def perform_create(self, serializer):
        """
        Método para crear un nuevo viaje.
        
        Args:
            serializer: Serializador con los datos del viaje
        """
        serializer.save(id_usuario=self.request.user)

class ViajeDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Vista para manejar operaciones CRUD sobre un viaje específico.
    
    Esta vista permite:
    - GET: Obtener los detalles de un viaje específico
    - PUT/PATCH: Actualizar el estado de un viaje
    - DELETE: Cancelar un viaje
    
    Características especiales:
    - Solo permite acceder a los viajes del usuario autenticado
    - Permite actualizar el estado del viaje
    - Permite cancelar viajes en curso
    """
    serializer_class = ViajeSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Método para obtener los viajes del usuario autenticado.
        
        Returns:
            QuerySet: Conjunto de viajes del usuario
        """
        return Viaje.objects.filter(id_usuario=self.request.user)

    def perform_update(self, serializer):
        """
        Método para actualizar un viaje.
        
        Args:
            serializer: Serializador con los datos actualizados
        """
        instance = self.get_object()
        if instance.estado == 'completado':
            raise serializers.ValidationError("No se puede modificar un viaje completado")
        serializer.save()

    def perform_destroy(self, instance):
        """
        Método para cancelar un viaje.
        
        Args:
            instance: Instancia del viaje a cancelar
        """
        if instance.estado == 'completado':
            raise serializers.ValidationError("No se puede cancelar un viaje completado")
        instance.estado = 'cancelado'
        instance.save()

class RutaFavoritaList(generics.ListCreateAPIView):
    """
    Vista para manejar la lista de rutas favoritas y su creación.
    
    Esta vista permite:
    - GET: Obtener la lista de rutas favoritas del usuario autenticado
    - POST: Marcar una ruta como favorita
    
    Características especiales:
    - Filtra automáticamente las rutas favoritas por el usuario autenticado
    - Incluye detalles completos de la ruta
    """
    serializer_class = RutaFavoritaSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Método para obtener las rutas favoritas del usuario autenticado.
        
        Returns:
            QuerySet: Conjunto de rutas favoritas del usuario
        """
        return RutaFavorita.objects.filter(id_usuario=self.request.user).select_related(
            'id_ruta', 'id_usuario'
        )

    def perform_create(self, serializer):
        """
        Método para crear una nueva ruta favorita.
        
        Args:
            serializer: Serializador con los datos de la ruta favorita
        """
        serializer.save(id_usuario=self.request.user)

class RutaFavoritaDetail(generics.RetrieveDestroyAPIView):
    """
    Vista para manejar operaciones sobre una ruta favorita específica.
    
    Esta vista permite:
    - GET: Obtener los detalles de una ruta favorita específica
    - DELETE: Eliminar una ruta de favoritos
    
    Características especiales:
    - Solo permite acceder a las rutas favoritas del usuario autenticado
    """
    serializer_class = RutaFavoritaSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Método para obtener las rutas favoritas del usuario autenticado.
        
        Returns:
            QuerySet: Conjunto de rutas favoritas del usuario
        """
        return RutaFavorita.objects.filter(id_usuario=self.request.user)

class CalificacionConductorList(generics.ListCreateAPIView):
    """
    Vista para manejar la lista de calificaciones de conductores y su creación.
    
    Esta vista permite:
    - GET: Obtener la lista de calificaciones de conductores
    - POST: Crear una nueva calificación de conductor
    
    Características especiales:
    - Permite filtrar calificaciones por usuario, conductor y viaje
    - Solo permite calificar conductores de viajes realizados
    - Incluye detalles completos del viaje, usuario y conductor
    """
    serializer_class = CalificacionConductorSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Método para obtener y filtrar las calificaciones de conductores.
        
        Filtros disponibles:
        - usuario: Filtra calificaciones por ID de usuario
        - conductor: Filtra calificaciones por ID de conductor
        - viaje: Filtra calificaciones por ID de viaje
        
        Returns:
            QuerySet: Conjunto de calificaciones filtradas según los parámetros
        """
        queryset = CalificacionConductor.objects.all().select_related(
            'id_viaje', 'id_usuario', 'id_conductor'
        )
        usuario_id = self.request.query_params.get('usuario')
        conductor_id = self.request.query_params.get('conductor')
        viaje_id = self.request.query_params.get('viaje')

        if usuario_id:
            queryset = queryset.filter(id_usuario_id=usuario_id)
        if conductor_id:
            queryset = queryset.filter(id_conductor_id=conductor_id)
        if viaje_id:
            queryset = queryset.filter(id_viaje_id=viaje_id)

        return queryset

    def perform_create(self, serializer):
        """
        Método para crear una nueva calificación de conductor.
        
        Args:
            serializer: Serializador con los datos de la calificación
            
        Raises:
            serializers.ValidationError: Si el usuario no ha realizado el viaje
        """
        viaje = serializer.validated_data['id_viaje']
        if viaje.id_usuario != self.request.user:
            raise serializers.ValidationError("Solo puedes calificar conductores de tus propios viajes")
        serializer.save(id_usuario=self.request.user)

class CalificacionConductorDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Vista para manejar operaciones CRUD sobre una calificación de conductor específica.
    
    Esta vista permite:
    - GET: Obtener los detalles de una calificación específica
    - PUT/PATCH: Actualizar los datos de una calificación
    - DELETE: Eliminar una calificación
    
    Características especiales:
    - Solo permite acceder a las calificaciones propias
    """
    serializer_class = CalificacionConductorSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Método para obtener las calificaciones del usuario autenticado.
        
        Returns:
            QuerySet: Conjunto de calificaciones del usuario
        """
        return CalificacionConductor.objects.filter(id_usuario=self.request.user)

class DashboardEmpresaView(APIView):
    """
    Vista para el dashboard de empresas de transporte.
    
    Esta vista proporciona:
    - Estadísticas generales de la empresa
    - Resumen de viajes y conductores
    - Métricas de rendimiento
    - Gráficos y tendencias
    
    Requiere autenticación y permisos de administrador.
    """
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request):
        """
        Método para obtener las estadísticas del dashboard.
        
        Returns:
            Response: Datos estadísticos de la empresa
        """
        empresa_id = request.query_params.get('empresa_id')
        if not empresa_id:
            return Response(
                {'error': 'Se requiere el ID de la empresa'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            # Obtener estadísticas generales
            estadisticas = EstadisticaEmpresa.objects.filter(
                id_empresa=empresa_id
            ).order_by('-fecha')[:30]  # Últimos 30 días

            # Obtener datos de vehículos y conductores
            vehiculos = Vehiculo.objects.filter(empresa=empresa_id)
            conductores = Conductor.objects.filter(id_vehiculos__in=vehiculos)

            # Obtener datos de viajes
            viajes = Viaje.objects.filter(
                id_ruta__id_vehiculos__in=vehiculos
            ).order_by('-fecha_viaje')[:10]  # Últimos 10 viajes

            # Calcular métricas
            total_vehiculos = vehiculos.count()
            total_conductores = conductores.count()
            vehiculos_disponibles = vehiculos.filter(disponibilidad=True).count()
            
            # Calcular ingresos y calificaciones
            ingresos_mes = sum(est.ingresos_totales for est in estadisticas)
            calificacion_promedio = sum(est.calificacion_promedio for est in estadisticas) / len(estadisticas) if estadisticas else 0

            # Preparar respuesta
            response_data = {
                'estadisticas_generales': {
                    'total_vehiculos': total_vehiculos,
                    'vehiculos_disponibles': vehiculos_disponibles,
                    'total_conductores': total_conductores,
                    'ingresos_mes': ingresos_mes,
                    'calificacion_promedio': calificacion_promedio
                },
                'estadisticas_diarias': EstadisticaEmpresaSerializer(estadisticas, many=True).data,
                'ultimos_viajes': ViajeSerializer(viajes, many=True).data,
                'conductores_activos': ConductorSerializer(conductores, many=True).data
            }

            return Response(response_data)

        except Exception as e:
            return Response(
                {'error': f'Error al obtener estadísticas: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class EstadisticaEmpresaView(generics.ListCreateAPIView):
    """
    Vista para manejar las estadísticas de empresas.
    
    Esta vista permite:
    - GET: Obtener estadísticas de una empresa
    - POST: Crear nuevas estadísticas
    
    Características especiales:
    - Filtrado por empresa y rango de fechas
    - Cálculo automático de métricas
    - Validación de datos
    """
    serializer_class = EstadisticaEmpresaSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get_queryset(self):
        """
        Método para obtener y filtrar las estadísticas.
        
        Filtros disponibles:
        - empresa_id: ID de la empresa
        - fecha_inicio: Fecha inicial del rango
        - fecha_fin: Fecha final del rango
        
        Returns:
            QuerySet: Conjunto de estadísticas filtradas
        """
        queryset = EstadisticaEmpresa.objects.all()
        empresa_id = self.request.query_params.get('empresa_id')
        fecha_inicio = self.request.query_params.get('fecha_inicio')
        fecha_fin = self.request.query_params.get('fecha_fin')

        if empresa_id:
            queryset = queryset.filter(id_empresa=empresa_id)
        if fecha_inicio:
            queryset = queryset.filter(fecha__gte=fecha_inicio)
        if fecha_fin:
            queryset = queryset.filter(fecha__lte=fecha_fin)

        return queryset.order_by('-fecha')

    def perform_create(self, serializer):
        """
        Método para crear nuevas estadísticas.
        
        Args:
            serializer: Serializador con los datos de la estadística
        """
        # Calcular métricas automáticamente
        empresa_id = serializer.validated_data['id_empresa']
        fecha = serializer.validated_data['fecha']

        # Obtener vehículos de la empresa
        vehiculos = Vehiculo.objects.filter(empresa=empresa_id)
        
        # Obtener viajes del día
        viajes = Viaje.objects.filter(
            id_ruta__id_vehiculos__in=vehiculos,
            fecha_viaje__date=fecha
        )

        # Calcular métricas
        total_viajes = viajes.count()
        viajes_completados = viajes.filter(estado='completado').count()
        viajes_cancelados = viajes.filter(estado='cancelado').count()
        ingresos_totales = sum(viaje.precio_final for viaje in viajes if viaje.estado == 'completado')
        
        # Calcular calificación promedio
        calificaciones = CalificacionConductor.objects.filter(
            id_viaje__in=viajes
        )
        calificacion_promedio = sum(cal.calificacion for cal in calificaciones) / len(calificaciones) if calificaciones else 0

        # Guardar estadísticas
        serializer.save(
            total_viajes=total_viajes,
            viajes_completados=viajes_completados,
            viajes_cancelados=viajes_cancelados,
            ingresos_totales=ingresos_totales,
            calificacion_promedio=calificacion_promedio,
            pasajeros_transportados=viajes_completados,  # Un pasajero por viaje completado
            kilometros_recorridos=0  # Este valor debería calcularse basado en las rutas
        )

class VersionSistemaList(generics.ListCreateAPIView):
    """
    Vista para manejar la lista de versiones del sistema y su creación.
    
    Esta vista permite:
    - GET: Obtener la lista de todas las versiones del sistema
    - POST: Crear una nueva versión
    
    Características especiales:
    - Filtrado por tipo de cambio y estado
    - Ordenamiento por fecha de lanzamiento
    - Validación de formato de versión
    """
    serializer_class = VersionSistemaSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get_queryset(self):
        """
        Método para obtener y filtrar las versiones.
        
        Filtros disponibles:
        - tipo_cambio: Filtra por tipo de cambio (mayor, menor, parche)
        - estado: Filtra por estado (desarrollo, pruebas, producción)
        
        Returns:
            QuerySet: Conjunto de versiones filtradas
        """
        queryset = VersionSistema.objects.all().select_related('desarrollador')
        tipo_cambio = self.request.query_params.get('tipo_cambio')
        estado = self.request.query_params.get('estado')

        if tipo_cambio:
            queryset = queryset.filter(tipo_cambio=tipo_cambio)
        if estado:
            queryset = queryset.filter(estado=estado)

        return queryset.order_by('-fecha_lanzamiento')

    def perform_create(self, serializer):
        """
        Método para crear una nueva versión.
        
        Args:
            serializer: Serializador con los datos de la versión
        """
        serializer.save(desarrollador=self.request.user)

class VersionSistemaDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Vista para manejar operaciones CRUD sobre una versión específica.
    
    Esta vista permite:
    - GET: Obtener los detalles de una versión específica
    - PUT/PATCH: Actualizar los datos de una versión
    - DELETE: Eliminar una versión
    
    Características especiales:
    - Solo permite actualizar versiones en desarrollo
    - Mantiene un registro de cambios
    """
    serializer_class = VersionSistemaSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]
    queryset = VersionSistema.objects.all()

    def perform_update(self, serializer):
        """
        Método para actualizar una versión.
        
        Args:
            serializer: Serializador con los datos actualizados
            
        Raises:
            serializers.ValidationError: Si se intenta actualizar una versión en producción
        """
        instance = self.get_object()
        if instance.estado == 'produccion':
            raise serializers.ValidationError(
                "No se puede modificar una versión en producción"
            )
        serializer.save()

    def perform_destroy(self, instance):
        """
        Método para eliminar una versión.
        
        Args:
            instance: Instancia de la versión a eliminar
            
        Raises:
            serializers.ValidationError: Si se intenta eliminar una versión en producción
        """
        if instance.estado == 'produccion':
            raise serializers.ValidationError(
                "No se puede eliminar una versión en producción"
            )
        instance.delete()

class PQRSList(generics.ListCreateAPIView):
    """
    Vista para manejar la lista de PQRS y su creación.
    
    Esta vista permite:
    - GET: Obtener la lista de PQRS del usuario autenticado
    - POST: Crear una nueva PQRS
    
    Características especiales:
    - Filtra automáticamente las PQRS por el usuario autenticado
    - Envía correo de acuse de recibo al crear una PQRS
    - Permite filtrar por tipo y estado
    """
    serializer_class = PQRSSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Método para obtener y filtrar las PQRS.
        
        Filtros disponibles:
        - tipo: Filtra por tipo de PQRS
        - estado: Filtra por estado de la PQRS
        
        Returns:
            QuerySet: Conjunto de PQRS filtradas según los parámetros
        """
        queryset = PQRS.objects.filter(id_usuario=self.request.user).select_related(
            'id_usuario', 'respondido_por'
        )
        tipo = self.request.query_params.get('tipo')
        estado = self.request.query_params.get('estado')

        if tipo:
            queryset = queryset.filter(tipo=tipo)
        if estado:
            queryset = queryset.filter(estado=estado)

        return queryset

    def perform_create(self, serializer):
        """
        Método para crear una nueva PQRS y enviar correo de acuse.
        
        Args:
            serializer: Serializador con los datos de la PQRS
        """
        pqrs = serializer.save(id_usuario=self.request.user)
        
        # Enviar correo de acuse de recibo
        try:
            send_mail(
                subject=f"Acuse de recibo - {pqrs.get_tipo_display()} #{pqrs.id_pqrs}",
                message=f"""
                Estimado/a {self.request.user.nombre},

                Hemos recibido su {pqrs.get_tipo_display().lower()} con el siguiente detalle:

                Asunto: {pqrs.asunto}
                Descripción: {pqrs.descripcion}
                Fecha de recepción: {pqrs.fecha_creacion.strftime('%d/%m/%Y %H:%M')}
                Número de radicado: {pqrs.id_pqrs}

                Nos pondremos en contacto con usted a la brevedad.

                Atentamente,
                Equipo de Soporte
                """,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[self.request.user.correo_electronico],
                fail_silently=False
            )
        except Exception as e:
            # Registrar el error pero no interrumpir la creación de la PQRS
            print(f"Error al enviar correo de acuse: {str(e)}")

class PQRSDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Vista para manejar operaciones CRUD sobre una PQRS específica.
    
    Esta vista permite:
    - GET: Obtener los detalles de una PQRS específica
    - PUT/PATCH: Actualizar una PQRS (solo administradores)
    - DELETE: Eliminar una PQRS
    
    Características especiales:
    - Solo permite acceder a las PQRS propias
    - Los administradores pueden responder PQRS
    - Envía correo de respuesta al actualizar
    """
    serializer_class = PQRSSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Método para obtener las PQRS del usuario autenticado o todas si es admin.
        Returns:
            QuerySet: Conjunto de PQRS del usuario o todas si es admin
        """
        if self.request.user.is_staff:
            return PQRS.objects.all()
        return PQRS.objects.filter(id_usuario=self.request.user)

    def perform_update(self, serializer):
        """
        Método para actualizar una PQRS y enviar correo de respuesta.
        
        Args:
            serializer: Serializador con los datos actualizados
            
        Raises:
            PermissionDenied: Si el usuario no es administrador
        """
        if not self.request.user.is_staff:
            raise PermissionDenied("Solo los administradores pueden responder PQRS")
        
        instance = self.get_object()
        if instance.estado == 'resuelto':
            raise serializers.ValidationError("No se puede modificar una PQRS resuelta")
        
        # Actualizar la PQRS
        pqrs = serializer.save(
            respondido_por=self.request.user,
            fecha_respuesta=timezone.now(),
            estado='resuelto'
        )
        
        # Enviar correo de respuesta
        try:
            send_mail(
                subject=f"Respuesta a su {pqrs.get_tipo_display()} #{pqrs.id_pqrs}",
                message=f"""
                Estimado/a {pqrs.id_usuario.nombre},

                Hemos respondido a su {pqrs.get_tipo_display().lower()}:

                Asunto: {pqrs.asunto}
                Respuesta: {pqrs.respuesta}
                Fecha de respuesta: {pqrs.fecha_respuesta.strftime('%d/%m/%Y %H:%M')}

                Si tiene alguna otra consulta, no dude en contactarnos.

                Atentamente,
                Equipo de Soporte
                """,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[pqrs.id_usuario.correo_electronico],
                fail_silently=False
            )
        except Exception as e:
            # Registrar el error pero no interrumpir la actualización
            print(f"Error al enviar correo de respuesta: {str(e)}")

    def perform_destroy(self, instance):
        """
        Método para eliminar una PQRS.
        
        Args:
            instance: Instancia de la PQRS a eliminar
            
        Raises:
            serializers.ValidationError: Si la PQRS está resuelta
        """
        if instance.estado == 'resuelto':
            raise serializers.ValidationError("No se puede eliminar una PQRS resuelta")
        instance.delete()

class PQRSAdminList(generics.ListAPIView):
    """
    Vista exclusiva para administradores para listar y filtrar todas las PQRS.
    Permite filtrar por tipo, estado y usuario.
    Solo accesible para administradores.
    """
    serializer_class = PQRSSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get_queryset(self):
        queryset = PQRS.objects.all().select_related('id_usuario', 'respondido_por')
        tipo = self.request.query_params.get('tipo')
        estado = self.request.query_params.get('estado')
        usuario_id = self.request.query_params.get('usuario')
        if tipo:
            queryset = queryset.filter(tipo=tipo)
        if estado:
            queryset = queryset.filter(estado=estado)
        if usuario_id:
            queryset = queryset.filter(id_usuario_id=usuario_id)
        return queryset

class RegistroUsuarioView(APIView):
    """
    Vista para el registro de nuevos usuarios.
    No requiere autenticación.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UsuarioSerializer(data=request.data)
        if serializer.is_valid():
            # Obtener el rol de pasajero por defecto
            try:
                rol_pasajero = Rol.objects.get(nombre='Pasajero')
            except Rol.DoesNotExist:
                return Response(
                    {'error': 'El rol de pasajero no existe en el sistema'},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

            # Crear el usuario con el rol de pasajero
            usuario = serializer.save(rol=rol_pasajero)
            return Response(
                {
                    'message': 'Usuario registrado exitosamente',
                    'usuario': UsuarioSerializer(usuario).data
                },
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UsuarioActualView(APIView):
    """
    Vista para obtener la información del usuario actual.
    Requiere autenticación.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UsuarioSerializer(request.user)
        return Response(serializer.data)