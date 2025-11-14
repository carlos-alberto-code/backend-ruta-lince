from pydantic import BaseModel


class LoginUsuario(BaseModel):
    email: str
    contrasena: str


class UsuarioLeido(BaseModel):
    id: int
    nombre_completo: str


class LoginRespuesta(BaseModel):
    access_token: str
    token_type: str = "bearer"
    usuario: UsuarioLeido

    model_config = {"from_attributes": True}
