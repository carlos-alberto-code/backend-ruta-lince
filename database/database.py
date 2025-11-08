from sqlmodel import SQLModel, create_engine, Session
from core.config import settings

# Crear el engine de la base de datos
engine = create_engine(
    settings.DATABASE_URL,
    connect_args={"check_same_thread": False}  # Necesario para SQLite
)


def crear_db_y_tablas():
    """
    Crea la base de datos y todas las tablas definidas en los modelos.
    Se debe llamar al iniciar la aplicación.
    """
    SQLModel.metadata.create_all(engine)


def get_session():
    """
    Generador que proporciona una sesión de base de datos.
    Se usa como dependencia en FastAPI.

    Yields:
        Session: Una sesión de SQLModel para interactuar con la BD
    """
    with Session(engine) as session:
        yield session

