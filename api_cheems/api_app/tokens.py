#este archivo se usa principalmente para manejar todo lo relacionado con los tokens que duraran 1 hora
from itsdangerous import URLSafeTimedSerializer
from django.conf import settings

def generar_token_de_recuperacion(email):
    serializer = URLSafeTimedSerializer(settings.SECRET_KEY)
    return serializer.dumps(email, salt="recuperar-contrasena")

def verificar_token_de_recuperacion(token, max_age=3600): 
    serializer = URLSafeTimedSerializer(settings.SECRET_KEY)
    try:
        email = serializer.loads(token, salt="recuperar-contrasena", max_age=max_age)
        return email
    except Exception:
        return None
