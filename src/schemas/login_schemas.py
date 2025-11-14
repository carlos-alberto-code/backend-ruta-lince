from sqlmodel import SQLModel


class LoginUsuario(SQLModel):
    email: str
    contrasena: str


class UsuarioLeido(SQLModel):
    id: int
    nombre_completo: str
    access_token: str
    token_type: str = "bearer"

    model_config = {"from_attributes": True}
