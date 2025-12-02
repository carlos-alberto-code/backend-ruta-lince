from fastapi import APIRouter

from src.servicios.login_service import ServicioAutenticacion
from schemas.login_schemas import LoginRespuesta, LoginUsuario

router = APIRouter(prefix="/auth", tags=["autenticación"])


@router.post(
    "/login",
    response_model=LoginRespuesta,
    summary="Iniciar sesión",
    description="Autenticar usuario con email y contraseña y devuelve el usuario autenticado con algunos datos necesarios."
)
async def login(credenciales: LoginUsuario) -> LoginRespuesta:
    return ServicioAutenticacion().autenticar_usuario(credenciales)
