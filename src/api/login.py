from fastapi import APIRouter

from schemas.login_schemas import LoginRespuesta
from src.schemas.login_schemas import LoginUsuario, UsuarioLeido
from src.services.login_service import ServicioAutenticacion

router = APIRouter(prefix="/auth", tags=["autenticación"])


@router.post(
    "/login",
    response_model=UsuarioLeido,
    summary="Iniciar sesión",
    description="Autenticar usuario con email y contraseña y devuelve el usuario autenticado con algunos datos necesarios."
)
async def login(credenciales: LoginUsuario) -> LoginRespuesta:
    return ServicioAutenticacion().autenticar_usuario(credenciales)
