from sqlmodel import Session, select
from models.user import User
from typing import Optional


class UserRepository:
    """
    Repositorio para operaciones CRUD de usuarios.
    Separa la lógica de acceso a datos del resto de la aplicación.
    """

    def __init__(self, session: Session):
        self.session = session

    def crear_usuario(self, email: str, contrasena_hasheada: str,
                      nombre: str = "", apellidos: str = "") -> User:
        """
        Crea un nuevo usuario en la base de datos.

        Args:
            email: Email del usuario
            contrasena_hasheada: Contraseña ya hasheada
            nombre: Nombre del usuario
            apellidos: Apellidos del usuario

        Returns:
            El usuario creado
        """
        usuario = User(
            email=email,
            contrasena=contrasena_hasheada,
            nombre=nombre,
            apellidos=apellidos,
            activo=True,
            verificado=False
        )

        self.session.add(usuario)
        self.session.commit()
        self.session.refresh(usuario)

        return usuario

    def obtener_por_email(self, email: str) -> Optional[User]:
        """
        Busca un usuario por su email.

        Args:
            email: Email del usuario a buscar

        Returns:
            El usuario si existe, None en caso contrario
        """
        statement = select(User).where(User.email == email)
        usuario = self.session.exec(statement).first()
        return usuario

    def obtener_por_id(self, user_id: int) -> Optional[User]:
        """
        Busca un usuario por su ID.

        Args:
            user_id: ID del usuario

        Returns:
            El usuario si existe, None en caso contrario
        """
        return self.session.get(User, user_id)

    def existe_email(self, email: str) -> bool:
        """
        Verifica si un email ya está registrado.

        Args:
            email: Email a verificar

        Returns:
            True si el email existe, False en caso contrario
        """
        return self.obtener_por_email(email) is not None

