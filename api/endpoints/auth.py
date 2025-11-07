from fastapi import APIRouter, status, Depends
from sqlmodel import Session
from schemas.user import UserCreate, UserLogin, UserRead, Token
from services.auth import AuthService
from database.database import get_session

router = APIRouter(prefix="/auth", tags=["autenticación"])


def get_auth_service(session: Session = Depends(get_session)) -> AuthService:
    """
    Dependencia que proporciona una instancia del servicio de autenticación.
    """
    return AuthService(session)


@router.post(
    "/registrar",
    response_model=UserRead,
    status_code=status.HTTP_201_CREATED,
    summary="Registrar nuevo usuario",
    description="Crear nuevo usuario en el sistema con email y contraseña"
)
async def registrar(
    datos_de_usuario: UserCreate,
    auth_service: AuthService = Depends(get_auth_service)
):
    """
    Endpoint para registrar un nuevo usuario.

    - **email**: Email válido del usuario
    - **contrasena**: Contraseña de al menos 8 caracteres con letras y números
    """
    return auth_service.registrar_usuario(datos_de_usuario)


@router.post(
    "/login",
    response_model=Token,
    summary="Iniciar sesión",
    description="Autenticar usuario con email y contraseña"
)
async def login(
    credenciales: UserLogin,
    auth_service: AuthService = Depends(get_auth_service)
):
    """
    Endpoint para autenticar un usuario.

    - **email**: Email del usuario registrado
    - **contrasena**: Contraseña del usuario

    Retorna un token JWT que debe ser usado en peticiones autenticadas.
    """
    return auth_service.autenticar_usuario(credenciales)
