from sqlmodel import SQLModel, Field
from pydantic import EmailStr, field_validator


class LoginUsuario(SQLModel):
    email: str
    contrasena: str


class LeerLoginUsuario(SQLModel):
    id: int
    verificado: bool
    nombre_completo: str

    model_config = {"from_attributes": True}


class Token(SQLModel):
    token_acceso: str = Field(..., alias='access_token')
    tipo_token: str = Field(..., alias='token_type')
    usuario: LeerLoginUsuario = Field(..., alias='user')

    model_config = {"from_attributes": True, "populate_by_name": True}


class CrearUsuario(SQLModel):
    email: EmailStr
    contrasena: str = Field(min_length=8, max_length=100)

    @field_validator('contrasena')
    @classmethod
    def validar_contrasena(cls, v: str) -> str:
        if not any(char.isdigit() for char in v):
            raise ValueError('La contraseña debe contener al menos un número')
        if not any(char.isalpha() for char in v):
            raise ValueError('La contraseña debe contener al menos una letra')
        return v
