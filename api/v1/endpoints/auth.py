from fastapi import APIRouter, status
from schemas.user import UserCreate, UserLogin, UserRead, Token

router = APIRouter(prefix="/auth", tags=["autenticación"])


@router.post(
    "/registrar",
    response_model=UserRead,
    status_code=status.HTTP_201_CREATED,
    summary="Registrar nuevo usuario",
    description="Crear nuevo usuario en el sistema con email y contraseña"
)
async def registrar(datos_de_usuario: UserCreate):
    return UserRead(
        id=1,
        email=datos_de_usuario.email,
        activo=True,
        verificado=False,
    )


@router.post(
    "/login",
    response_model=Token,
    summary="Iniciar sesión",
    description="Autenticar usuario con email y contraseña"
)
async def login(credenciales: UserLogin):
    usuario_mock = UserRead(
        id=1,
        email=credenciales.email,
        activo=True,
        verificado=True,
    )

    return Token(
        access_token="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.mock_token_example",
        token_type="bearer",
        user=usuario_mock
    )
