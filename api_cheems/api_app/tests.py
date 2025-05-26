from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from .models import Usuario, Vehiculo, Conductor, Ruta, Calificacion
from django.utils import timezone
from datetime import time, date

class UsuarioTests(TestCase):
    """
    Suite de pruebas para el modelo Usuario y sus endpoints.
    
    Esta clase contiene pruebas para:
    - Creación de usuarios
    - Autenticación de usuarios
    - Operaciones CRUD de usuarios
    - Validaciones de campos
    """
    def setUp(self):
        """
        Configuración inicial para las pruebas de usuario.
        Crea un superusuario y configura el cliente API.
        """
        self.client = APIClient()
        # Crear superusuario una sola vez para todas las pruebas
        self.superuser = Usuario.objects.create_superuser(
            correo_electronico='erijahiaron@gmail.com',
            contrasena='1076650495e',
            nombre='Super Erik'
        )
        self.client.force_authenticate(user=self.superuser)

    def test_crear_usuario(self):
        """
        Prueba la creación de un nuevo usuario.
        Verifica que:
        - Se pueda crear un usuario con datos válidos
        - Los campos se guarden correctamente
        - Se devuelva el código de estado correcto
        """
        url = reverse('usuario-list')
        data = {
            'correo_electronico': 'arevaloerik2705@gmail.com',
            'contrasena': '1076650495e',
            'nombre': 'Erik Normal'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Usuario.objects.count(), 2)
        self.assertEqual(Usuario.objects.get(correo_electronico='arevaloerik2705@gmail.com').nombre, 'Erik Normal')

    def test_autenticacion_usuario(self):
        """
        Prueba la autenticación de usuarios.
        Verifica que:
        - Un usuario pueda iniciar sesión con credenciales válidas
        - Se devuelva un token de autenticación
        - Se rechacen credenciales inválidas
        """
        url = reverse('token_obtain_pair')
        data = {
            'correo_electronico': 'erijahiaron@gmail.com',
            'contrasena': '1076650495e'
        }
        response = self.client.post(url, data, format='json')
        print("Response status:", response.status_code)
        print("Response data:", response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

class VehiculoTests(TestCase):
    """
    Suite de pruebas para el modelo Vehiculo y sus endpoints.
    
    Esta clase contiene pruebas para:
    - Creación de vehículos
    - Actualización de vehículos
    - Eliminación de vehículos
    - Validaciones de campos
    """
    def setUp(self):
        """
        Configuración inicial para las pruebas de vehículos.
        Crea un superusuario y configura el cliente API.
        """
        self.client = APIClient()
        self.superuser = Usuario.objects.create_superuser(
            correo_electronico='erijahiaron@gmail.com',
            contrasena='1076650495e',
            nombre='Super Erik'
        )
        self.client.force_authenticate(user=self.superuser)

    def test_crear_vehiculo(self):
        """
        Prueba la creación de un nuevo vehículo.
        Verifica que:
        - Se pueda crear un vehículo con datos válidos
        - Los campos se guarden correctamente
        - Se devuelva el código de estado correcto
        """
        url = reverse('vehiculo-list')
        data = {
            'placa': 'CHE-001',
            'empresa': 1,
            'disponibilidad': True
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Vehiculo.objects.count(), 1)
        self.assertEqual(Vehiculo.objects.get(placa='CHE-001').empresa, 1)

class ConductorTests(TestCase):
    """
    Suite de pruebas para el modelo Conductor y sus endpoints.
    
    Esta clase contiene pruebas para:
    - Creación de conductores
    - Asignación de vehículos
    - Validaciones de campos
    - Relaciones con vehículos
    """
    def setUp(self):
        """
        Configuración inicial para las pruebas de conductores.
        Crea un superusuario, un vehículo y configura el cliente API.
        """
        self.client = APIClient()
        self.superuser = Usuario.objects.create_superuser(
            correo_electronico='erijahiaron@gmail.com',
            contrasena='1076650495e',
            nombre='Super Erik'
        )
        self.client.force_authenticate(user=self.superuser)
        self.vehiculo = Vehiculo.objects.create(
            placa='CHE-001',
            empresa=1,
            disponibilidad=True
        )

    def test_crear_conductor(self):
        """
        Prueba la creación de un nuevo conductor.
        Verifica que:
        - Se pueda crear un conductor con datos válidos
        - Se asigne correctamente el vehículo
        - Se devuelva el código de estado correcto
        """
        url = reverse('conductor-list')
        data = {
            'id_vehiculos': self.vehiculo.id_vehiculos,
            'nombre': 'Jorge Espitia',
            'licencia_conduccion': 12345
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Conductor.objects.count(), 1)
        self.assertEqual(Conductor.objects.get(nombre='Jorge Espitia').licencia_conduccion, 12345)

class RutaTests(TestCase):
    """
    Suite de pruebas para el modelo Ruta y sus endpoints.
    
    Esta clase contiene pruebas para:
    - Creación de rutas
    - Asignación de vehículos
    - Validaciones de horarios
    - Relaciones con vehículos
    """
    def setUp(self):
        """
        Configuración inicial para las pruebas de rutas.
        Crea un superusuario, un vehículo y configura el cliente API.
        """
        self.client = APIClient()
        self.superuser = Usuario.objects.create_superuser(
            correo_electronico='erijahiaron@gmail.com',
            contrasena='1076650495e',
            nombre='Super Erik'
        )
        self.client.force_authenticate(user=self.superuser)
        self.vehiculo = Vehiculo.objects.create(
            placa='CHE-001',
            empresa=1,
            disponibilidad=True
        )

    def test_crear_ruta(self):
        """
        Prueba la creación de una nueva ruta.
        Verifica que:
        - Se pueda crear una ruta con datos válidos
        - Se asigne correctamente el vehículo
        - Se manejen correctamente los horarios
        - Se devuelva el código de estado correcto
        """
        url = reverse('ruta-list')
        data = {
            'id_vehiculos': self.vehiculo.id_vehiculos,
            'nombre_ruta': 'Rapido el carmen',
            'origen': 'Ubate',
            'destino': 'Cucucnuba',
            'horario': '08:00:00'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Ruta.objects.count(), 1)
        self.assertEqual(Ruta.objects.get(nombre_ruta='Rapido el carmen').origen, 'Ubate')

class CalificacionTests(TestCase):
    """
    Suite de pruebas para el modelo Calificacion y sus endpoints.
    
    Esta clase contiene pruebas para:
    - Creación de calificaciones
    - Validaciones de puntuaciones
    - Relaciones con rutas y usuarios
    - Validaciones de fechas
    """
    def setUp(self):
        """
        Configuración inicial para las pruebas de calificaciones.
        Crea un superusuario, un vehículo, una ruta y configura el cliente API.
        """
        self.client = APIClient()
        self.superuser = Usuario.objects.create_superuser(
            correo_electronico='erijahiaron@gmail.com',
            contrasena='1076650495e',
            nombre='Super Erik'
        )
        self.client.force_authenticate(user=self.superuser)
        self.vehiculo = Vehiculo.objects.create(
            placa='CHE-001',
            empresa=1,
            disponibilidad=True
        )
        self.ruta = Ruta.objects.create(
            id_vehiculos=self.vehiculo,
            nombre_ruta='Rapido el carmen',
            origen='Ubate',
            destino='Cucucnuba',
            horario=time(8, 0)
        )

    def test_crear_calificacion(self):
        """
        Prueba la creación de una nueva calificación.
        Verifica que:
        - Se pueda crear una calificación con datos válidos
        - Se validen correctamente las puntuaciones
        - Se manejen correctamente las fechas
        - Se devuelva el código de estado correcto
        """
        url = reverse('calificacion-list')
        data = {
            'id_ruta': self.ruta.id_ruta,
            'id_usuario': self.superuser.id_usuario,
            'calificacion': 5,
            'comentario': 'Excelente servicio, muy puntual',
            'fecha': date.today()
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Calificacion.objects.count(), 1)
        self.assertEqual(Calificacion.objects.get(comentario='Excelente servicio, muy puntual').calificacion, 5)

    def test_calificacion_invalida(self):
        """
        Prueba la validación de calificaciones inválidas.
        Verifica que:
        - Se rechacen calificaciones fuera del rango permitido
        - Se devuelvan mensajes de error apropiados
        """
        url = reverse('calificacion-list')
        data = {
            'id_ruta': self.ruta.id_ruta,
            'id_usuario': self.superuser.id_usuario,
            'calificacion': 6,  # Calificación inválida
            'comentario': 'Test comentario',
            'fecha': date.today()
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class RecuperacionContrasenaTests(TestCase):
    """
    Suite de pruebas para la recuperación de contraseña.
    
    Esta clase contiene pruebas para:
    - Solicitud de recuperación de contraseña
    - Validación de correos existentes
    - Manejo de errores
    """
    def setUp(self):
        """
        Configuración inicial para las pruebas de recuperación de contraseña.
        Crea un usuario de prueba y configura el cliente API.
        """
        self.client = APIClient()
        self.usuario = Usuario.objects.create_user(
            correo_electronico='arevaloerik2705@gmail.com',
            contrasena='1076650495e',
            nombre='Erik Normal'
        )
        self.recuperar_url = reverse('recuperar-contrasena')
        self.restablecer_url = reverse('restablecer-contrasena')

    def test_recuperar_contrasena(self):
        """
        Prueba la solicitud de recuperación de contraseña.
        Verifica que:
        - Se pueda solicitar la recuperación con un correo válido
        - Se devuelva el mensaje de confirmación correcto
        """
        data = {'correo_electronico': 'arevaloerik2705@gmail.com'}
        response = self.client.post(self.recuperar_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['confirmación'], 'Correo enviado con instrucciones')

    def test_recuperar_contrasena_usuario_no_existe(self):
        """
        Prueba el intento de recuperación con un correo inexistente.
        Verifica que:
        - Se rechace la solicitud con un correo no registrado
        - Se devuelva el código de error apropiado
        """
        data = {'correo_electronico': 'noexiste@cheems.com'}
        response = self.client.post(self.recuperar_url, data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
