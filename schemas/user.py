from sqlmodel import SQLModel, Field
from pydantic import EmailStr, field_validator


class UserCreate(SQLModel):
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


class UserLogin(SQLModel):
    email: EmailStr
    contrasena: str


class UserRead(SQLModel):
    id: int
    email: str
    activo: bool
    verificado: bool

    model_config = {"from_attributes": True}


class Token(SQLModel):
    access_token: str
    token_type: str = "bearer"
    user: UserRead
