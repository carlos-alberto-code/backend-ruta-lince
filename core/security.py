from datetime import datetime, timedelta, timezone
from typing import Any
from jose import jwt
from passlib.context import CryptContext
from core.config import settings

# Configuración para el hashing de contraseñas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verificar_contrasena(contrasena_plana: str, contrasena_hasheada: str) -> bool:
    """
    Verifica si una contraseña en texto plano coincide con su versión hasheada.

    Args:
        contrasena_plana: La contraseña en texto plano
        contrasena_hasheada: La contraseña hasheada almacenada en BD

    Returns:
        True si las contraseñas coinciden, False en caso contrario
    """
    return pwd_context.verify(contrasena_plana, contrasena_hasheada)


def hashear_contrasena(contrasena: str) -> str:
    """
    Genera un hash de una contraseña en texto plano.

    Args:
        contrasena: La contraseña en texto plano

    Returns:
        La contraseña hasheada
    """
    return pwd_context.hash(contrasena)


def crear_access_token(data: dict[str, Any], expires_delta: timedelta | None = None) -> str:
    """
    Crea un token JWT de acceso.

    Args:
        data: Los datos a incluir en el token (típicamente el user_id o email)
        expires_delta: Tiempo de expiración del token

    Returns:
        El token JWT como string
    """
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

    return encoded_jwt

