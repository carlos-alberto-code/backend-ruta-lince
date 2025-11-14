from sqlmodel import SQLModel, Field


class Usuario(SQLModel, table=True):
    __tablename__ = 'usuarios'

    id: int | None = Field(default=None, primary_key=True)
    nombre: str = Field(default="", nullable=False)
    apellidos: str = Field(default="", nullable=False)
    email: str = Field(unique=True, nullable=False, index=True, max_length=255)
    contrasena_hash: str = Field(nullable=False, max_length=255)
