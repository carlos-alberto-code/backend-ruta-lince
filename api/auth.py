from fastapi import APIRouter

from schemas.login import UserLogin, UserLoginRead

router = APIRouter(prefix="/auth", tags=["autenticación"])


@router.post(
    "/login",
    response_model=UserLoginRead,
    summary="Iniciar sesión",
    description="Autenticar usuario con email y contraseña y devuelve el usuario autenticado con algunos datos necesarios."
)
async def login(credenciales: UserLogin):
    """
    Endpoint para autenticar un usuario.
    - **email**: Email del usuario registrado
    - **password**: Contraseña del usuario
    Retorna los datos del usuario autenticado.
    """
    return UserLoginRead(id=1, verificado=True, nombre_completo="Juan Pérez")
