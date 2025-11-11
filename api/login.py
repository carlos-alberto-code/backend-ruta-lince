from fastapi import APIRouter

from schemas.login import LoginUsuario, UsuarioLeido
from services.login_service import ServicioAutenticacion

enrutador = APIRouter(prefix="/auth", tags=["autenticación"])


@enrutador.post(
    "/login",
    response_model=UsuarioLeido,
    summary="Iniciar sesión",
    description="Autenticar usuario con email y contraseña y devuelve el usuario autenticado con algunos datos necesarios."
)
async def login(credenciales: LoginUsuario):
    """
    Endpoint para autenticar un usuario.
    - **email**: Email del usuario registrado
    - **contraseña**: Contraseña del usuario
    Retorna los datos del usuario autenticado.
    """
    return ServicioAutenticacion().autenticar_usuario(credenciales)
