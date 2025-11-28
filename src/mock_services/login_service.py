from jose import jwt
from sqlalchemy import ColumnElement
from passlib.context import CryptContext
from fastapi import HTTPException, status
from datetime import UTC, datetime, timedelta

from config import settings
from src.models import Estudiantes
from src.schemas import UsuarioLeido, LoginUsuario, LoginRespuesta
from src.database.repository import Repository

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def _verificar_contrasena(contrasena_plana: str, contrasena_hash: str) -> bool:
    return pwd_context.verify(contrasena_plana, contrasena_hash)


def _crear_token_acceso(usuario_id: int, email: str) -> str:
    expiracion = datetime.now(UTC) + timedelta(days=settings.ACCESS_TOKEN_EXPIRE_DAYS)
    datos_token = {
        "sub": str(usuario_id),
        "email": email,
        "exp": expiracion
    }
    token = jwt.encode(datos_token, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return token


class ServicioAutenticacion:

    def __init__(self):
        self._repository: Repository[Estudiantes] = Repository(Estudiantes)

    def autenticar_usuario(self, credenciales: LoginUsuario) -> LoginRespuesta:
        condition: ColumnElement[bool] = Estudiantes.email == credenciales.email
        usuarios: list[Estudiantes] = self._repository.get_by(condition)
        usuario: Estudiantes | None = usuarios[0] if usuarios else None

        if not usuario:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Email o contraseña incorrectos",
                headers={"WWW-Authenticate": "Bearer"},
            )

        if not _verificar_contrasena(credenciales.contrasena, usuario.contrasena_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Email o contraseña incorrectos",
                headers={"WWW-Authenticate": "Bearer"},
            )

        token = _crear_token_acceso(usuario.id, usuario.email)

        # return UsuarioLeido(
        #     id=usuario.id,
        #     nombre_completo=f"{usuario.nombre} {usuario.apellidos}",
        #     access_token=token,
        #     token_type="bearer"
        # )
        return LoginRespuesta(
            access_token=token,
            token_type="bearer",
            usuario=UsuarioLeido(
                id=usuario.id,
                nombre_completo=f"{usuario.nombre} {usuario.apellidos}"
            )
        )


def hashear_contrasena(contrasena: str) -> str:
    """Convierte contraseña en hash para guardar en DB"""
    return pwd_context.hash(contrasena)
