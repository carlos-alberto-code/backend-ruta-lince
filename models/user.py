"""
Modelos y esquemas relacionados con usuarios.

Este módulo contiene:
- User: Modelo de tabla (SQLModel con table=True)
- UserCreate: Schema para creación (input)
- UserUpdate: Schema para actualización (input)
- UserPublic: Schema para respuesta (output)
"""

from datetime import datetime
from typing import TYPE_CHECKING

from sqlmodel import Field, SQLModel

if TYPE_CHECKING:
    # Para evitar imports circulares si necesitamos relaciones en el futuro
    pass


# ============================================================================
# MODELO DE TABLA (Database Model)
# ============================================================================

class User(SQLModel, table=True):
    """
    Modelo de usuario en la base de datos.

    Representa la tabla 'users' y contiene todos los campos que se
    almacenarán en la base de datos, incluyendo campos sensibles como
    hashed_password.
    """
    __tablename__ = "users"

    # Primary Key
    id: int | None = Field(
        default=None,
        primary_key=True,
        description="ID único del usuario"
    )

    # Campos de autenticación
    email: str = Field(
        unique=True,
        index=True,
        max_length=255,
        description="Email único del usuario (usado para login)"
    )
    hashed_password: str = Field(
        max_length=255,
        description="Contraseña hasheada con bcrypt"
    )

    # Información personal
    full_name: str | None = Field(
        default=None,
        max_length=255,
        description="Nombre completo del usuario"
    )

    # Estado y permisos
    is_active: bool = Field(
        default=True,
        description="Si el usuario está activo (puede iniciar sesión)"
    )
    is_superuser: bool = Field(
        default=False,
        description="Si el usuario tiene permisos de superusuario"
    )

    # Timestamps
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Fecha y hora de creación"
    )
    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Fecha y hora de última actualización"
    )

    # Para futuras relaciones, ejemplo:
    # tokens: list["Token"] = Relationship(back_populates="user")


# ============================================================================
# SCHEMAS DE ENTRADA (Input Schemas)
# ============================================================================

class UserCreate(SQLModel):
    """
    Schema para crear un nuevo usuario.

    Se usa en el endpoint de registro. Solo contiene los campos
    que el cliente debe enviar. La contraseña viene en texto plano
    y será hasheada por el servicio antes de guardarla.
    """
    email: str = Field(
        max_length=255,
        description="Email del usuario"
    )
    password: str = Field(
        min_length=8,
        max_length=100,
        description="Contraseña en texto plano (mínimo 8 caracteres)"
    )
    full_name: str | None = Field(
        default=None,
        max_length=255,
        description="Nombre completo del usuario (opcional)"
    )

    # Validación extra de email (Pydantic)
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "email": "usuario@example.com",
                    "password": "password123",
                    "full_name": "Juan Pérez"
                }
            ]
        }
    }


class UserUpdate(SQLModel):
    """
    Schema para actualizar un usuario existente.

    Todos los campos son opcionales para permitir actualizaciones parciales.
    """
    email: str | None = Field(
        default=None,
        max_length=255,
        description="Nuevo email (opcional)"
    )
    full_name: str | None = Field(
        default=None,
        max_length=255,
        description="Nuevo nombre completo (opcional)"
    )
    password: str | None = Field(
        default=None,
        min_length=8,
        max_length=100,
        description="Nueva contraseña en texto plano (opcional)"
    )
    is_active: bool | None = Field(
        default=None,
        description="Nuevo estado activo/inactivo (opcional)"
    )


# ============================================================================
# SCHEMAS DE SALIDA (Output Schemas)
# ============================================================================

class UserPublic(SQLModel):
    """
    Schema para devolver información de usuario al cliente.

    NO incluye campos sensibles como hashed_password.
    Este es el schema que se retorna en las respuestas de API.
    """
    id: int = Field(description="ID del usuario")
    email: str = Field(description="Email del usuario")
    full_name: str | None = Field(description="Nombre completo")
    is_active: bool = Field(description="Estado activo del usuario")
    is_superuser: bool = Field(description="Si es superusuario")
    created_at: datetime = Field(description="Fecha de creación")
    updated_at: datetime = Field(description="Fecha de última actualización")

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "id": 1,
                    "email": "usuario@example.com",
                    "full_name": "Juan Pérez",
                    "is_active": True,
                    "is_superuser": False,
                    "created_at": "2024-01-15T10:30:00",
                    "updated_at": "2024-01-15T10:30:00"
                }
            ]
        }
    }


class UserWithPassword(UserPublic):
    """
    Schema que incluye el hashed_password.

    Solo se usa internamente en servicios, NUNCA se retorna en API.
    Útil cuando necesitamos el modelo completo para verificaciones internas.
    """
    hashed_password: str = Field(description="Contraseña hasheada")
