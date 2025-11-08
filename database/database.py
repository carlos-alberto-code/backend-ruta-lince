from sqlmodel import SQLModel, create_engine, Session
from core.config import configuracion

# Crear el motor de la base de datos
motor = create_engine(
    configuracion.URL_BASE_DATOS,
    connect_args={"check_same_thread": False}  # Necesario para SQLite
)


def crear_bd_y_tablas():
    """
    Crea la base de datos y todas las tablas definidas en los modelos.
    Se debe llamar al iniciar la aplicación.
    """
    SQLModel.metadata.create_all(motor)


def obtener_sesion():
    """
    Generador que proporciona una sesión de base de datos.
    Se usa como dependencia en FastAPI.

    Yields:
        Session: Una sesión de SQLModel para interactuar con la BD
    """
    with Session(motor) as sesion:
        yield sesion

