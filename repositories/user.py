from sqlmodel import Session, select
from models.user import Usuario
from typing import Optional


class RepositorioUsuario:
    """
    Repositorio para operaciones CRUD de usuarios.
    Separa la lógica de acceso a datos del resto de la aplicación.
    """

    def __init__(self, sesion: Session):
        self.sesion = sesion

    def crear_usuario(self, email: str, contrasena_hasheada: str,
                      nombre: str = "", apellidos: str = "") -> Usuario:
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
        usuario = Usuario(
            email=email,
            contrasena=contrasena_hasheada,
            nombre=nombre,
            apellidos=apellidos,
            activo=True,
            verificado=False
        )

        self.sesion.add(usuario)
        self.sesion.commit()
        self.sesion.refresh(usuario)

        return usuario

    def obtener_por_email(self, email: str) -> Optional[Usuario]:
        """
        Busca un usuario por su email.

        Args:
            email: Email del usuario a buscar

        Returns:
            El usuario si existe, None en caso contrario
        """
        declaracion = select(Usuario).where(Usuario.email == email)
        usuario = self.sesion.exec(declaracion).first()
        return usuario

    def obtener_por_id(self, id_usuario: int) -> Optional[Usuario]:
        """
        Busca un usuario por su ID.

        Args:
            id_usuario: ID del usuario

        Returns:
            El usuario si existe, None en caso contrario
        """
        return self.sesion.get(Usuario, id_usuario)

    def existe_email(self, email: str) -> bool:
        """
        Verifica si un email ya está registrado.

        Args:
            email: Email a verificar

        Returns:
            True si el email existe, False en caso contrario
        """
        return self.obtener_por_email(email) is not None

