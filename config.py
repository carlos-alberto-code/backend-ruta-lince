from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    SECRET_KEY: str = "tu-clave-secreta-cambiala-en-produccion"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_DAYS: int = 1
    database_url_pre: str = "sqlite:///ruta_lince_database.sqlite"

    class Config:
        env_file = ".env"


settings = Settings()
