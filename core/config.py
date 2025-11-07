from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Configuración de la aplicación.
    Las variables se pueden sobrescribir mediante variables de entorno.
    """
    # Configuración del proyecto
    PROJECT_NAME: str = "Ruta Lince API"
    VERSION: str = "0.1.0"
    API_V1_STR: str = "/api/v1"

    # Configuración de seguridad
    SECRET_KEY: str = "tu-clave-secreta-super-segura-cambiala-en-produccion"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # Configuración de la base de datos
    DATABASE_URL: str = "sqlite:///./ruta_lince_database.sqlite"

    # Configuración de CORS
    BACKEND_CORS_ORIGINS: list[str] = [
        "http://localhost:3000",
        "http://localhost:5173",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5173",
    ]

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True
    )


# Instancia global de configuración
settings = Settings()

