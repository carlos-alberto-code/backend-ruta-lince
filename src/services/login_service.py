from jose import jwt
from sqlalchemy import ColumnElement
from passlib.context import CryptContext
from fastapi import HTTPException, status
from datetime import UTC, datetime, timedelta

from config import settings
from src.models import Usuario
from src.schemas import UsuarioLeido, LoginUsuario
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
        self._repository: Repository[Usuario] = Repository(Usuario)

    def autenticar_usuario(self, credenciales: LoginUsuario) -> UsuarioLeido:
        condition: ColumnElement[bool] = Usuario.email == credenciales.email
        usuarios: list[Usuario] = self._repository.get_by(condition)
        usuario: Usuario | None = usuarios[0] if usuarios else None

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

        return UsuarioLeido(
            id=usuario.id,
            nombre_completo=f"{usuario.nombre} {usuario.apellidos}",
            access_token=token,
            token_type="bearer"
        )


def hashear_contrasena(contrasena: str) -> str:
    """Convierte contraseña en hash para guardar en DB"""
    return pwd_context.hash(contrasena)

# usuario_nuevo = Usuario( -- Al crear un nuevo usuario, hay que hashear la contraseña
#     email="usuario@ejemplo.com",
#     nombre="Juan",
#     apellidos="Pérez",
#     contrasena_hash=hashear_contrasena("micontraseña123")
# )
