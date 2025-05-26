import jwt
from datetime import datetime, timedelta
from django.conf import settings

def generar_token(user_id, expiracion=24):
    """
    Genera un token JWT para el usuario especificado.
    
    Args:
        user_id: ID del usuario.
        expiracion: Tiempo de expiración en horas (por defecto 24).
    
    Returns:
        str: Token JWT generado.
    """
    payload = {
        'user_id': user_id,
        'exp': datetime.utcnow() + timedelta(hours=expiracion)
    }
    return jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')

def verificar_token(token):
    """
    Verifica un token JWT y devuelve el payload si es válido.
    
    Args:
        token: Token JWT a verificar.
    
    Returns:
        dict: Payload del token si es válido.
    
    Raises:
        jwt.ExpiredSignatureError: Si el token ha expirado.
        jwt.InvalidTokenError: Si el token es inválido.
    """
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        raise Exception('Token expirado')
    except jwt.InvalidTokenError:
        raise Exception('Token inválido') 