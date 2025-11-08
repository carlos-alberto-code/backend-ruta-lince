from fastapi import HTTPException, status
from sqlmodel import Session
from repositories.user import UserRepository
from core.security import hashear_contrasena, verificar_contrasena, crear_access_token
from schemas.login import UserCreate, UserLogin, UserLoginRead, Token


class AuthService:
    """
    Servicio de autenticación.
    Contiene la lógica de negocio para registro, login y gestión de tokens.
    """

    def __init__(self, session: Session):
        self.session = session
        self.user_repo = UserRepository(session)

    def registrar_usuario(self, datos_usuario: UserCreate) -> UserLoginRead:
        """
        Registra un nuevo usuario en el sistema.

        Args:
            datos_usuario: Datos del usuario a crear (email y contraseña)

        Returns:
            UserLoginRead: Los datos del usuario creado

        Raises:
            HTTPException: Si el email ya está registrado
        """
        # Verificar si el email ya existe
        if self.user_repo.existe_email(str(datos_usuario.email)):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El email ya está registrado"
            )
        
        # Hashear la contraseña
        contrasena_hasheada = hashear_contrasena(datos_usuario.contrasena)
        
        # Crear el usuario
        usuario = self.user_repo.crear_usuario(
            email=str(datos_usuario.email),
            contrasena_hasheada=contrasena_hasheada
        )

        # Retornar el usuario sin la contraseña
        return UserLoginRead(
            id=usuario.id,
            email=usuario.email,
            activo=usuario.activo,
            verificado=usuario.verificado
        )

    def autenticar_usuario(self, credenciales: UserLogin):
        """
        Autentica un usuario y genera un token de acceso.

        Args:
            credenciales: Email y contraseña del usuario

        Returns:
            Token: Token de acceso y datos del usuario

        Raises:
            HTTPException: Si las credenciales son incorrectas
        """
        # Buscar el usuario por email
        usuario = self.user_repo.obtener_por_email(str(credenciales.email))

        if not usuario:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Email o contraseña incorrectos",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # Verificar la contraseña
        if not verificar_contrasena(credenciales.password, usuario.contrasena):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Email o contraseña incorrectos",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # Verificar que el usuario esté activo
        if not usuario.activo:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Usuario inactivo"
            )

        # Crear el token de acceso
        access_token = crear_access_token(
            data={"sub": str(usuario.id), "email": usuario.email}
        )

        # Retornar el token y los datos del usuario
        return Token(
            access_token=access_token,
            token_type="bearer",
            user=UserLoginRead(
                id=usuario.id,
                email=usuario.email,
                activo=usuario.activo,
                verificado=usuario.verificado
            )
        )

