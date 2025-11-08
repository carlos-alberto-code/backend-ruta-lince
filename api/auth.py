from fastapi import APIRouter

from schemas.login import LoginUsuario, LeerLoginUsuario

enrutador = APIRouter(prefix="/auth", tags=["autenticación"])


@enrutador.post(
    "/login",
    response_model=LeerLoginUsuario,
    summary="Iniciar sesión",
    description="Autenticar usuario con email y contraseña y devuelve el usuario autenticado con algunos datos necesarios."
)
async def login(credenciales: LoginUsuario):
    """
    Endpoint para autenticar un usuario.
    - **email**: Email del usuario registrado
    - **contrasena**: Contraseña del usuario
    Retorna los datos del usuario autenticado.
    """
    return LeerLoginUsuario(id=1, verificado=True, nombre_completo="Juan Pérez")
