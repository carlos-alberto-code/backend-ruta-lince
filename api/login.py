from fastapi import APIRouter

from schemas.login import LoginUsuario, UsuarioLeido
from services.login_service import ServicioAutenticacion

router = APIRouter(prefix="/auth", tags=["autenticación"])


@router.post(
    "/login",
    response_model=UsuarioLeido,
    summary="Iniciar sesión",
    description="Autenticar usuario con email y contraseña y devuelve el usuario autenticado con algunos datos necesarios."
)
async def login(credenciales: LoginUsuario):
    return ServicioAutenticacion().autenticar_usuario(credenciales)
