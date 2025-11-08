from datetime import datetime, timedelta, timezone
from typing import Any
from jose import jwt
from passlib.context import CryptContext
from core.config import configuracion

# Configuración para el hashing de contraseñas
contexto_contrasena = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verificar_contrasena(contrasena_plana: str, contrasena_hasheada: str) -> bool:
    """
    Verifica si una contraseña en texto plano coincide con su versión hasheada.

    Args:
        contrasena_plana: La contraseña en texto plano
        contrasena_hasheada: La contraseña hasheada almacenada en BD

    Returns:
        True si las contraseñas coinciden, False en caso contrario
    """
    return contexto_contrasena.verify(contrasena_plana, contrasena_hasheada)


def hashear_contrasena(contrasena: str) -> str:
    """
    Genera un hash de una contraseña en texto plano.

    Args:
        contrasena: La contraseña en texto plano

    Returns:
        La contraseña hasheada
    """
    return contexto_contrasena.hash(contrasena)


def crear_token_acceso(datos: dict[str, Any], delta_expiracion: timedelta | None = None) -> str:
    """
    Crea un token JWT de acceso.

    Args:
        datos: Los datos a incluir en el token (típicamente el id_usuario o email)
        delta_expiracion: Tiempo de expiración del token

    Returns:
        El token JWT como string
    """
    a_codificar = datos.copy()

    if delta_expiracion:
        expiracion = datetime.now(timezone.utc) + delta_expiracion
    else:
        expiracion = datetime.now(timezone.utc) + timedelta(minutes=configuracion.MINUTOS_EXPIRACION_TOKEN_ACCESO)

    a_codificar.update({"exp": expiracion})
    jwt_codificado = jwt.encode(a_codificar, configuracion.CLAVE_SECRETA, algorithm=configuracion.ALGORITMO)

    return jwt_codificado

