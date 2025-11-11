from fastapi import HTTPException, status
from sqlalchemy import ColumnElement

from models import Usuario
from database.repository import Repository
from schemas.login import UsuarioLeido, LoginUsuario


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
        return UsuarioLeido(id=usuario.id, nombre_completo=usuario.nombre + " " + usuario.apellidos)
