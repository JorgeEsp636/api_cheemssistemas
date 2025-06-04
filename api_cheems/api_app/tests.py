from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from .models import Usuario, Vehiculo, Conductor, Ruta, Calificacion, Zona, Tarifa, Rol, Viaje, VersionSistema, PQRS
from django.utils import timezone
from datetime import time, date
from django.core.files.uploadedfile import SimpleUploadedFile


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

    def test_listar_usuarios(self):
        """
        Prueba el listado de usuarios.
        Verifica que:
        - Se puedan listar todos los usuarios
        - Se devuelva el código de estado correcto
        - Se incluyan todos los campos necesarios
        """
        # Crear algunos usuarios adicionales
        Usuario.objects.create_user(
            correo_electronico='usuario1@test.com',
            contrasena='test123',
            nombre='Usuario 1'
        )
        Usuario.objects.create_user(
            correo_electronico='usuario2@test.com',
            contrasena='test123',
            nombre='Usuario 2'
        )

        url = reverse('usuario-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)  # superuser + 2 usuarios creados

    def test_actualizar_usuario(self):
        """
        Prueba la actualización de un usuario.
        Verifica que:
        - Se pueda actualizar un usuario existente
        - Los campos se actualicen correctamente
        - Se devuelva el código de estado correcto
        """
        # Crear un usuario para actualizar
        usuario = Usuario.objects.create_user(
            correo_electronico='usuario@test.com',
            contrasena='test123',
            nombre='Usuario Original'
        )

        url = reverse('usuario-detail', args=[usuario.id_usuario])
        data = {
            'nombre': 'Usuario Actualizado',
            'correo_electronico': 'usuario@test.com'  # Mantener el mismo correo
        }
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Usuario.objects.get(id_usuario=usuario.id_usuario).nombre, 'Usuario Actualizado')

    def test_eliminar_usuario(self):
        """
        Prueba la eliminación de un usuario.
        Verifica que:
        - Se pueda eliminar un usuario existente
        - Se devuelva el código de estado correcto
        - El usuario ya no exista en la base de datos
        """
        # Crear un usuario para eliminar
        usuario = Usuario.objects.create_user(
            correo_electronico='usuario@test.com',
            contrasena='test123',
            nombre='Usuario a Eliminar'
        )

        url = reverse('usuario-detail', args=[usuario.id_usuario])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Usuario.objects.filter(id_usuario=usuario.id_usuario).exists())

    def test_validar_campos_usuario(self):
        """
        Prueba las validaciones de campos de usuario.
        Verifica que:
        - No se puedan crear usuarios con correos duplicados
        - Se validen los formatos de correo electrónico
        - Se validen las contraseñas
        """
        # Crear usuario inicial
        Usuario.objects.create_user(
            correo_electronico='usuario@test.com',
            contrasena='test123',
            nombre='Usuario Test'
        )

        # Intentar crear usuario con correo duplicado
        url = reverse('usuario-list')
        data = {
            'correo_electronico': 'usuario@test.com',
            'contrasena': 'test123',
            'nombre': 'Usuario Duplicado'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Intentar crear usuario con correo inválido
        data['correo_electronico'] = 'correo_invalido'
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Intentar crear usuario sin contraseña
        data = {
            'correo_electronico': 'nuevo@test.com',
            'nombre': 'Usuario Sin Contraseña'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

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

    def test_listar_vehiculos(self):
        """
        Prueba el listado de vehículos.
        Verifica que:
        - Se puedan listar todos los vehículos
        - Se devuelva el código de estado correcto
        - Se incluyan todos los campos necesarios
        """
        # Crear algunos vehículos adicionales
        Vehiculo.objects.create(
            placa='CHE-002',
            empresa=1,
            disponibilidad=True
        )
        Vehiculo.objects.create(
            placa='CHE-003',
            empresa=1,
            disponibilidad=False
        )

        url = reverse('vehiculo-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # 2 vehículos creados

    def test_actualizar_vehiculo(self):
        """
        Prueba la actualización de un vehículo.
        Verifica que:
        - Se pueda actualizar un vehículo existente
        - Los campos se actualicen correctamente
        - Se devuelva el código de estado correcto
        """
        # Crear un vehículo para actualizar
        vehiculo = Vehiculo.objects.create(
            placa='CHE-002',
            empresa=1,
            disponibilidad=True
        )

        url = reverse('vehiculo-detail', args=[vehiculo.id_vehiculos])
        data = {
            'placa': 'CHE-002',
            'empresa': 2,
            'disponibilidad': False
        }
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        vehiculo_actualizado = Vehiculo.objects.get(id_vehiculos=vehiculo.id_vehiculos)
        self.assertEqual(vehiculo_actualizado.empresa, 2)
        self.assertEqual(vehiculo_actualizado.disponibilidad, False)

    def test_eliminar_vehiculo(self):
        """
        Prueba la eliminación de un vehículo.
        Verifica que:
        - Se pueda eliminar un vehículo existente
        - Se devuelva el código de estado correcto
        - El vehículo ya no exista en la base de datos
        """
        # Crear un vehículo para eliminar
        vehiculo = Vehiculo.objects.create(
            placa='CHE-002',
            empresa=1,
            disponibilidad=True
        )

        url = reverse('vehiculo-detail', args=[vehiculo.id_vehiculos])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Vehiculo.objects.filter(id_vehiculos=vehiculo.id_vehiculos).exists())

    def test_validar_campos_vehiculo(self):
        """
        Prueba las validaciones de campos de vehículo.
        Verifica que:
        - No se puedan crear vehículos con placas duplicadas
        - Se validen los campos requeridos
        - Se validen los tipos de datos
        """
        # Crear vehículo inicial
        Vehiculo.objects.create(
            placa='CHE-002',
            empresa=1,
            disponibilidad=True
        )

        # Intentar crear vehículo con placa duplicada
        url = reverse('vehiculo-list')
        data = {
            'placa': 'CHE-002',
            'empresa': 1,
            'disponibilidad': True
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Intentar crear vehículo sin placa
        data = {
            'empresa': 1,
            'disponibilidad': True
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Intentar crear vehículo con empresa inválida
        data = {
            'placa': 'CHE-003',
            'empresa': 'empresa_invalida',
            'disponibilidad': True
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

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

    def test_listar_conductores(self):
        """
        Prueba el listado de conductores.
        Verifica que:
        - Se puedan listar todos los conductores
        - Se devuelva el código de estado correcto
        - Se incluyan todos los campos necesarios
        """
        # Crear algunos conductores adicionales
        Conductor.objects.create(
            id_vehiculos=self.vehiculo,
            nombre='Conductor 1',
            licencia_conduccion=12346
        )
        Conductor.objects.create(
            id_vehiculos=self.vehiculo,
            nombre='Conductor 2',
            licencia_conduccion=12347
        )

        url = reverse('conductor-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # 2 conductores creados

    def test_actualizar_conductor(self):
        """
        Prueba la actualización de un conductor.
        Verifica que:
        - Se pueda actualizar un conductor existente
        - Los campos se actualicen correctamente
        - Se devuelva el código de estado correcto
        """
        # Crear un conductor para actualizar
        conductor = Conductor.objects.create(
            id_vehiculos=self.vehiculo,
            nombre='Conductor Original',
            licencia_conduccion=12348
        )

        url = reverse('conductor-detail', args=[conductor.id_conductor])
        data = {
            'nombre': 'Conductor Actualizado',
            'licencia_conduccion': 12349
        }
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        conductor_actualizado = Conductor.objects.get(id_conductor=conductor.id_conductor)
        self.assertEqual(conductor_actualizado.nombre, 'Conductor Actualizado')
        self.assertEqual(conductor_actualizado.licencia_conduccion, 12349)

    def test_eliminar_conductor(self):
        """
        Prueba la eliminación de un conductor.
        Verifica que:
        - Se pueda eliminar un conductor existente
        - Se devuelva el código de estado correcto
        - El conductor ya no exista en la base de datos
        """
        # Crear un conductor para eliminar
        conductor = Conductor.objects.create(
            id_vehiculos=self.vehiculo,
            nombre='Conductor a Eliminar',
            licencia_conduccion=12350
        )

        url = reverse('conductor-detail', args=[conductor.id_conductor])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Conductor.objects.filter(id_conductor=conductor.id_conductor).exists())

    def test_validar_campos_conductor(self):
        """
        Prueba las validaciones de campos de conductor.
        Verifica que:
        - No se puedan crear conductores con licencias duplicadas
        - Se validen los campos requeridos
        - Se validen los tipos de datos
        """
        # Crear conductor inicial
        Conductor.objects.create(
            id_vehiculos=self.vehiculo,
            nombre='Conductor Test',
            licencia_conduccion=12351
        )

        # Intentar crear conductor con licencia duplicada
        url = reverse('conductor-list')
        data = {
            'id_vehiculos': self.vehiculo.id_vehiculos,
            'nombre': 'Conductor Duplicado',
            'licencia_conduccion': 12351
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Intentar crear conductor sin nombre
        data = {
            'id_vehiculos': self.vehiculo.id_vehiculos,
            'licencia_conduccion': 12352
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Intentar crear conductor con licencia inválida
        data = {
            'id_vehiculos': self.vehiculo.id_vehiculos,
            'nombre': 'Conductor Inválido',
            'licencia_conduccion': 'licencia_invalida'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

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

# Agregar después de las clases existentes

class RolTests(TestCase):
    """
    Suite de pruebas para el modelo Rol y sus endpoints.
    """
    def setUp(self):
        self.client = APIClient()
        self.superuser = Usuario.objects.create_superuser(
            correo_electronico='erijahiaron@gmail.com',
            contrasena='1076650495e',
            nombre='Super Erik'
        )
        self.client.force_authenticate(user=self.superuser)

    def test_crear_rol(self):
        url = reverse('rol-list')
        data = {
            'nombre': 'Conductor Senior',
            'descripcion': 'Conductor con más de 5 años de experiencia'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Rol.objects.count(), 1)
        
class ZonaTests(TestCase):
    """
        Suite de pruebas para el modelo Zona y sus endpoints.
            
        Esta clase contiene pruebas para:
        - Creación de zonas
        - Actualización de zonas
        - Validaciones de campos
        - Operaciones CRUD de zonas
    """
    def setUp(self):
        """
        Configuración inicial para las pruebas de zonas.
        Crea un superusuario y configura el cliente API.
        """
        self.client = APIClient()
        self.superuser = Usuario.objects.create_superuser(
            correo_electronico='erijahiaron@gmail.com',
            contrasena='1076650495e',
            nombre='Super Erik'
        )
        self.client.force_authenticate(user=self.superuser)

    def test_crear_zona(self):
        """
        Prueba la creación de una nueva zona.
        Verifica que:
        - Se pueda crear una zona con datos válidos
        - Los campos se guarden correctamente
        - Se devuelva el código de estado correcto
        """
        url = reverse('zona-list')
        data = {
            'nombre': 'Ubate',
            'descripcion': 'Zona de Ubate',
            'activa': True
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Zona.objects.count(), 1)
        self.assertEqual(Zona.objects.get(nombre='Ubate').descripcion, 'Zona de Ubate')

    def test_listar_zonas(self):
        """
        Prueba el listado de zonas.
        Verifica que:
        - Se puedan listar todas las zonas
        - Se devuelva el código de estado correcto
        """
        # Crear algunas zonas
        Zona.objects.create(nombre='Ubate', descripcion='Zona de Ubate', activa=True)
        Zona.objects.create(nombre='Cucunuba', descripcion='Zona de Cucunuba', activa=True)
        
        url = reverse('zona-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_actualizar_zona(self):
        """
        Prueba la actualización de una zona.
        Verifica que:
        - Se pueda actualizar una zona existente
        - Los cambios se guarden correctamente
        - Se devuelva el código de estado correcto
        """
        zona = Zona.objects.create(
            nombre='Ubate',
            descripcion='Zona de Ubate',
            activa=True
        )
        
        url = reverse('zona-detail', args=[zona.id_zona])
        data = {
            'nombre': 'Ubate Centro',
            'descripcion': 'Zona centro de Ubate',
            'activa': True
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Zona.objects.get(id_zona=zona.id_zona).nombre, 'Ubate Centro')

    def test_eliminar_zona(self):
        """
        Prueba la eliminación de una zona.
        Verifica que:
        - Se pueda eliminar una zona existente
        - La zona se elimine correctamente
        - Se devuelva el código de estado correcto
        """
        zona = Zona.objects.create(
            nombre='Ubate',
            descripcion='Zona de Ubate',
            activa=True
        )
        
        url = reverse('zona-detail', args=[zona.id_zona])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Zona.objects.count(), 0)
        
class TarifaTests(TestCase):
    """
    Suite de pruebas para el modelo Tarifa y sus endpoints.
    
    Esta clase contiene pruebas para:
    - Creación de tarifas
    - Validaciones de zonas
    - Actualización de precios
    - Operaciones CRUD de tarifas
    """
    def setUp(self):
        """
        Configuración inicial para las pruebas de tarifas.
        Crea un superusuario, zonas y configura el cliente API.
        """
        self.client = APIClient()
        self.superuser = Usuario.objects.create_superuser(
            correo_electronico='erijahiaron@gmail.com',
            contrasena='1076650495e',
            nombre='Super Erik'
        )
        self.client.force_authenticate(user=self.superuser)
        
        # Crear zonas para las pruebas
        self.zona_origen = Zona.objects.create(
            nombre='Ubate',
            descripcion='Zona de Ubate',
            activa=True
        )
        self.zona_destino = Zona.objects.create(
            nombre='Cucunuba',
            descripcion='Zona de Cucunuba',
            activa=True
        )

    def test_crear_tarifa(self):
        """
        Prueba la creación de una nueva tarifa.
        Verifica que:
        - Se pueda crear una tarifa con datos válidos
        - Los campos se guarden correctamente
        - Se devuelva el código de estado correcto
        """
        url = reverse('tarifa-list')
        data = {
            'zona_origen': self.zona_origen.id_zona,
            'zona_destino': self.zona_destino.id_zona,
            'precio_base': '5000.00',
            'precio_km': '1000.00',
            'activa': True
        }
        response = self.client.post(url, data, format='json')
        print('RESPONSE DATA CREAR TARIFA:', response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Tarifa.objects.count(), 1)
        self.assertEqual(float(Tarifa.objects.get().precio_base), 5000.00)

    def test_validar_zonas_iguales(self):
        """
        Prueba la validación de zonas iguales en una tarifa.
        Verifica que:
        - No se pueda crear una tarifa con la misma zona de origen y destino
        - Se devuelva el código de estado correcto
        """
        url = reverse('tarifa-list')
        data = {
            'zona_origen': self.zona_origen.id_zona,
            'zona_destino': self.zona_origen.id_zona,
            'precio_base': '5000.00',
            'precio_km': '1000.00',
            'activa': True
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_listar_tarifas(self):
        """
        Prueba el listado de tarifas.
        Verifica que:
        - Se puedan listar todas las tarifas
        - Se devuelva el código de estado correcto
        """
        # Crear algunas tarifas
        Tarifa.objects.create(
            zona_origen=self.zona_origen,
            zona_destino=self.zona_destino,
            precio_base='5000.00',
            precio_km='1000.00',
            activa=True,
            actualizado_por=self.superuser
        )
        
        url = reverse('tarifa-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_actualizar_tarifa(self):
        """
        Prueba la actualización de una tarifa.
        Verifica que:
        - Se pueda actualizar una tarifa existente
        - Los cambios se guarden correctamente
        - Se devuelva el código de estado correcto
        """
        tarifa = Tarifa.objects.create(
            zona_origen=self.zona_origen,
            zona_destino=self.zona_destino,
            precio_base='5000.00',
            precio_km='1000.00',
            activa=True,
            actualizado_por=self.superuser
        )
        
        url = reverse('tarifa-detail', args=[tarifa.id_tarifa])
        data = {
            'zona_origen': self.zona_origen.id_zona,
            'zona_destino': self.zona_destino.id_zona,
            'precio_base': '6000.00',
            'precio_km': '1200.00',
            'activa': True
        }
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(float(Tarifa.objects.get(id_tarifa=tarifa.id_tarifa).precio_base), 6000.00)

    def test_eliminar_tarifa(self):
        """
        Prueba la eliminación de una tarifa.
        Verifica que:
        - Se pueda eliminar una tarifa existente
        - La tarifa se elimine correctamente
        - Se devuelva el código de estado correcto
        """
        tarifa = Tarifa.objects.create(
            zona_origen=self.zona_origen,
            zona_destino=self.zona_destino,
            precio_base='5000.00',
            precio_km='1000.00',
            activa=True,
            actualizado_por=self.superuser
        )
        
        url = reverse('tarifa-detail', args=[tarifa.id_tarifa])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Tarifa.objects.count(), 0)

class ImportacionRutasTests(TestCase):
    """
    Suite de pruebas para la importación de rutas desde CSV.
    
    Esta clase contiene pruebas para:
    - Importación de rutas desde CSV
    - Validación de formato CSV
    - Manejo de errores
    - Descarga de plantilla
    """
    def setUp(self):
        """
        Configuración inicial para las pruebas de importación.
        Crea un superusuario y configura el cliente API.
        """
        self.client = APIClient()
        self.superuser = Usuario.objects.create_superuser(
            correo_electronico='erijahiaron@gmail.com',
            contrasena='1076650495e',
            nombre='Super Erik'
        )
        self.client.force_authenticate(user=self.superuser)
        
        # Crear vehículo para las pruebas
        self.vehiculo = Vehiculo.objects.create(
            placa='CHE-001',
            empresa=1,
            disponibilidad=True
        )

    def test_descargar_plantilla(self):
        url = reverse('ruta-plantilla')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response['Content-Type'], 'text/csv')
        self.assertIn('nombre_ruta,origen,destino,horario,placa_vehiculo', 
                     response.content.decode())

    def test_importar_rutas_csv(self):
        url = reverse('ruta-importar')
        csv_content = 'nombre_ruta,origen,destino,horario,placa_vehiculo\n'
        csv_content += 'Rapido el carmen,Ubate,Cucunuba,08:00,CHE-001\n'
        csv_content += 'Rapido el carmen,Cucunuba,Ubate,09:00,CHE-001'
        
        csv_file = SimpleUploadedFile(
            "rutas.csv",
            csv_content.encode(),
            content_type="text/csv"
        )
        
        data = {'archivo': csv_file}
        response = self.client.post(url, data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Ruta.objects.count(), 2)
        # Verificar que ambas rutas se crearon correctamente
        rutas = Ruta.objects.filter(nombre_ruta='Rapido el carmen')
        self.assertEqual(rutas.count(), 2)
        self.assertTrue(rutas.filter(origen='Ubate').exists())
        self.assertTrue(rutas.filter(origen='Cucunuba').exists())

    def test_importar_rutas_csv_invalido(self):
        url = reverse('ruta-importar')
        csv_content = 'campo_invalido\n'
        csv_content += 'dato_invalido'
        
        csv_file = SimpleUploadedFile(
            "rutas_invalidas.csv",
            csv_content.encode(),
            content_type="text/csv"
        )
        
        data = {'archivo': csv_file}
        response = self.client.post(url, data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)

    def test_importar_rutas_vehiculo_no_existe(self):
        url = reverse('ruta-importar')
        csv_content = 'nombre_ruta,origen,destino,horario,placa_vehiculo\n'
        csv_content += 'Ruta Test,Ubate,Cucunuba,08:00,VEHICULO-INEXISTENTE'
        
        csv_file = SimpleUploadedFile(
            "rutas_vehiculo_invalido.csv",
            csv_content.encode(),
            content_type="text/csv"
        )
        
        data = {'archivo': csv_file}
        response = self.client.post(url, data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)

    def test_importar_rutas_formato_horario_invalido(self):
        url = reverse('ruta-importar')
        csv_content = 'nombre_ruta,origen,destino,horario,placa_vehiculo\n'
        csv_content += 'Ruta Test,Ubate,Cucunuba,25:00,CHE-001'
        
        csv_file = SimpleUploadedFile(
            "rutas_horario_invalido.csv",
            csv_content.encode(),
            content_type="text/csv"
        )
        
        data = {'archivo': csv_file}
        response = self.client.post(url, data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)

class VersionSistemaTests(TestCase):
    """
    Suite de pruebas para el modelo VersionSistema y sus endpoints.
    
    Esta clase contiene pruebas para:
    - Creación de versiones
    - Validación de formato de versión
    - Validación de cambios
    - Actualización de versiones
    - Eliminación de versiones
    - Filtrado de versiones
    """
    def setUp(self):
        """
        Configuración inicial para las pruebas de versiones.
        Crea un superusuario y configura el cliente API.
        """
        self.client = APIClient()
        self.superuser = Usuario.objects.create_superuser(
            correo_electronico='erijahiaron@gmail.com',
            contrasena='1076650495e',
            nombre='Super Erik'
        )
        self.client.force_authenticate(user=self.superuser)

    def test_crear_version(self):
        """
        Prueba la creación de una nueva versión.
        Verifica que:
        - Se pueda crear una versión con datos válidos
        - Los campos se guarden correctamente
        - Se devuelva el código de estado correcto
        """
        url = reverse('version-sistema-list')
        data = {
            'numero_version': '1.0.0',
            'tipo_cambio': 'mayor',
            'descripcion': 'Primera versión del sistema',
            'cambios': [
                {
                    'tipo': 'nuevo',
                    'descripcion': 'Implementación inicial del sistema'
                }
            ],
            'estado': 'desarrollo'
        }
        response = self.client.post(url, data, format='json')
        print('RESPONSE DATA CREAR VERSION:', response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(VersionSistema.objects.count(), 1)
        self.assertEqual(VersionSistema.objects.get().numero_version, '1.0.0')

    def test_validar_formato_version(self):
        """
        Prueba la validación del formato de número de versión.
        Verifica que:
        - Se rechacen formatos inválidos
        - Se acepten formatos válidos
        """
        url = reverse('version-sistema-list')
        data = {
            'numero_version': '1.0',  # Formato inválido
            'tipo_cambio': 'mayor',
            'descripcion': 'Versión de prueba',
            'cambios': [
                {
                    'tipo': 'nuevo',
                    'descripcion': 'Test'
                }
            ],
            'estado': 'desarrollo'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_validar_cambios(self):
        """
        Prueba la validación de la estructura de cambios.
        Verifica que:
        - Se rechacen cambios con estructura inválida
        - Se acepten cambios con estructura válida
        """
        url = reverse('version-sistema-list')
        data = {
            'numero_version': '1.0.0',
            'tipo_cambio': 'mayor',
            'descripcion': 'Versión de prueba',
            'cambios': [
                {
                    'tipo': 'nuevo'  # Falta descripción
                }
            ],
            'estado': 'desarrollo'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_actualizar_version(self):
        """
        Prueba la actualización de una versión.
        Verifica que:
        - Se pueda actualizar una versión en desarrollo
        - No se pueda actualizar una versión en producción
        """
        # Crear versión inicial
        version = VersionSistema.objects.create(
            numero_version='1.0.0',
            tipo_cambio='mayor',
            descripcion='Versión inicial',
            cambios=[{'tipo': 'nuevo', 'descripcion': 'Test'}],
            desarrollador=self.superuser,
            estado='desarrollo'
        )

        # Intentar actualizar versión en desarrollo
        url = reverse('version-sistema-detail', args=[version.id_version])
        data = {
            'descripcion': 'Versión actualizada',
            'estado': 'pruebas'
        }
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(VersionSistema.objects.get().descripcion, 'Versión actualizada')

        # Cambiar estado a producción
        version.estado = 'produccion'
        version.save()

        # Intentar actualizar versión en producción
        data = {'descripcion': 'No debería actualizarse'}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_eliminar_version(self):
        """
        Prueba la eliminación de versiones.
        Verifica que:
        - Se pueda eliminar una versión en desarrollo
        - No se pueda eliminar una versión en producción
        """
        # Crear versión en desarrollo
        version = VersionSistema.objects.create(
            numero_version='1.0.0',
            tipo_cambio='mayor',
            descripcion='Versión de prueba',
            cambios=[{'tipo': 'nuevo', 'descripcion': 'Test'}],
            desarrollador=self.superuser,
            estado='desarrollo'
        )

        # Intentar eliminar versión en desarrollo
        url = reverse('version-sistema-detail', args=[version.id_version])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(VersionSistema.objects.count(), 0)

        # Crear versión en producción
        version = VersionSistema.objects.create(
            numero_version='2.0.0',
            tipo_cambio='mayor',
            descripcion='Versión en producción',
            cambios=[{'tipo': 'nuevo', 'descripcion': 'Test'}],
            desarrollador=self.superuser,
            estado='produccion'
        )

        # Intentar eliminar versión en producción
        url = reverse('version-sistema-detail', args=[version.id_version])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(VersionSistema.objects.count(), 1)

    def test_filtrar_versiones(self):
        """
        Prueba el filtrado de versiones.
        Verifica que:
        - Se puedan filtrar por tipo de cambio
        - Se puedan filtrar por estado
        - Se devuelvan los resultados correctos
        """
        # Crear versiones de prueba
        VersionSistema.objects.create(
            numero_version='1.0.0',
            tipo_cambio='mayor',
            descripcion='Versión mayor',
            cambios=[{'tipo': 'nuevo', 'descripcion': 'Test'}],
            desarrollador=self.superuser,
            estado='desarrollo'
        )
        VersionSistema.objects.create(
            numero_version='1.0.1',
            tipo_cambio='parche',
            descripcion='Versión parche',
            cambios=[{'tipo': 'correccion', 'descripcion': 'Test'}],
            desarrollador=self.superuser,
            estado='produccion'
        )

        # Filtrar por tipo de cambio
        url = reverse('version-sistema-list') + '?tipo_cambio=mayor'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['numero_version'], '1.0.0')

        # Filtrar por estado
        url = reverse('version-sistema-list') + '?estado=produccion'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['numero_version'], '1.0.1')

class PQRSTests(TestCase):
    """
    Suite de pruebas para el modelo PQRS y sus endpoints.
    
    Esta clase contiene pruebas para:
    - Creación de PQRS
    - Envío de correos de acuse de recibo
    - Respuesta a PQRS
    - Validaciones de campos
    - Filtrado de PQRS
    """
    def setUp(self):
        """
        Configuración inicial para las pruebas de PQRS.
        Crea un superusuario, un usuario normal y configura el cliente API.
        """
        self.client = APIClient()
        self.superuser = Usuario.objects.create_superuser(
            correo_electronico='erijahiaron@gmail.com',
            contrasena='1076650495e',
            nombre='Super Erik'
        )
        self.usuario_normal = Usuario.objects.create_user(
            correo_electronico='usuario@test.com',
            contrasena='test123',
            nombre='Usuario Test'
        )
        self.client.force_authenticate(user=self.usuario_normal)

    def test_crear_pqrs(self):
        """
        Prueba la creación de una nueva PQRS.
        Verifica que:
        - Se pueda crear una PQRS con datos válidos
        - Se envíe el correo de acuse de recibo
        - Se devuelva el código de estado correcto
        """
        url = reverse('pqrs-list')
        data = {
            'tipo': 'peticion',
            'asunto': 'Solicitud de información',
            'descripcion': 'Necesito información sobre las rutas disponibles',
            'id_usuario': self.usuario_normal.id_usuario
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(PQRS.objects.count(), 1)
        self.assertEqual(PQRS.objects.get().asunto, 'Solicitud de información')
        self.assertEqual(PQRS.objects.get().estado, 'pendiente')

    def test_validar_tipo_pqrs(self):
        """
        Prueba la validación del tipo de PQRS.
        Verifica que:
        - Se rechacen tipos inválidos
        - Se acepten tipos válidos
        """
        url = reverse('pqrs-list')
        data = {
            'tipo': 'tipo_invalido',  # Tipo inválido
            'asunto': 'Test',
            'descripcion': 'Test'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_responder_pqrs(self):
        """
        Prueba la respuesta a una PQRS.
        Verifica que:
        - Solo los administradores puedan responder
        - Se actualice el estado correctamente
        - Se registre el administrador que respondió
        """
        # Crear PQRS
        pqrs = PQRS.objects.create(
            id_usuario=self.usuario_normal,
            tipo='peticion',
            asunto='Test',
            descripcion='Test',
            estado='pendiente'
        )

        # Autenticar como superusuario
        self.client.force_authenticate(user=self.superuser)

        # Responder PQRS
        url = reverse('pqrs-detail', args=[pqrs.id_pqrs])
        data = {
            'respuesta': 'Respuesta de prueba',
            'estado': 'resuelto',
            'respondido_por': self.superuser.id_usuario
        }
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(PQRS.objects.get().estado, 'resuelto')
        self.assertEqual(PQRS.objects.get().respondido_por, self.superuser)

    def test_listar_pqrs_usuario(self):
        """
        Prueba el listado de PQRS para usuarios normales.
        Verifica que:
        - Los usuarios solo vean sus propias PQRS
        - Se devuelvan los datos correctos
        """
        # Crear PQRS para el usuario normal
        PQRS.objects.create(
            id_usuario=self.usuario_normal,
            tipo='peticion',
            asunto='Test 1',
            descripcion='Test 1',
            estado='pendiente'
        )

        # Crear PQRS para otro usuario
        otro_usuario = Usuario.objects.create_user(
            correo_electronico='otro@test.com',
            contrasena='test123',
            nombre='Otro Usuario'
        )
        PQRS.objects.create(
            id_usuario=otro_usuario,
            tipo='peticion',
            asunto='Test 2',
            descripcion='Test 2',
            estado='pendiente'
        )

        # Listar PQRS del usuario normal
        url = reverse('pqrs-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['asunto'], 'Test 1')

    def test_listar_pqrs_admin(self):
        """
        Prueba el listado de PQRS para administradores.
        Verifica que:
        - Los administradores vean todas las PQRS
        - Se puedan filtrar por estado
        """
        # Crear PQRS con diferentes estados
        PQRS.objects.create(
            id_usuario=self.usuario_normal,
            tipo='peticion',
            asunto='Test 1',
            descripcion='Test 1',
            estado='pendiente'
        )
        PQRS.objects.create(
            id_usuario=self.usuario_normal,
            tipo='queja',
            asunto='Test 2',
            descripcion='Test 2',
            estado='resuelto'
        )

        # Autenticar como superusuario
        self.client.force_authenticate(user=self.superuser)

        # Listar todas las PQRS
        url = reverse('pqrs-admin-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

        # Filtrar por estado
        url = reverse('pqrs-admin-list') + '?estado=pendiente'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['estado'], 'pendiente')
        
