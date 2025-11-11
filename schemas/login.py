from sqlmodel import SQLModel, Field


class LoginUsuario(SQLModel):
    email: str
    contrasena: str


class UsuarioLeido(SQLModel):
    id: int
    nombre_completo: str

    model_config = {"from_attributes": True}


class Token(SQLModel):
    token_acceso: str = Field(..., alias='access_token')
    tipo_token: str = Field(..., alias='token_type')
    usuario: UsuarioLeido = Field(..., alias='user')

    model_config = {"from_attributes": True, "populate_by_name": True}
