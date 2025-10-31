from sqlmodel import SQLModel, Field


class User(SQLModel, table=True):
    __tablename__ = 'usuarios'

    id: int | None = Field(default=None, primary_key=True)
    nombre: str = Field(nullable=False)
    apellidos: str = Field(nullable=False)
    email: str = Field(unique=True, nullable=False, index=True, max_length=255)
    contrasena: str = Field(nullable=False, max_length=255)
    activo: bool = Field(default=True, nullable=False)
    verificado: bool = Field(default=False, nullable=False)
