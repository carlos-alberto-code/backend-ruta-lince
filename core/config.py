from pydantic_settings import BaseSettings, SettingsConfigDict


class Configuracion(BaseSettings):
    """
    Configuración de la aplicación.
    Las variables se pueden sobrescribir mediante variables de entorno.
    """
    # Configuración del proyecto
    NOMBRE_PROYECTO: str = "Ruta Lince API"
    VERSION: str = "0.1.0"
    API_V1_STR: str = "/api/v1"

    # Configuración de seguridad
    CLAVE_SECRETA: str = "tu-clave-secreta-super-segura-cambiala-en-produccion"
    ALGORITMO: str = "HS256"
    MINUTOS_EXPIRACION_TOKEN_ACCESO: int = 30

    # Configuración de la base de datos
    URL_BASE_DATOS: str = "sqlite:///./ruta_lince_database.sqlite"

    # Configuración de CORS
    ORIGENES_CORS_BACKEND: list[str] = [
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
configuracion = Configuracion()

