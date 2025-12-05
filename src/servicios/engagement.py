from sqlmodel import select
from src.models.models import Video
from src.database.connection import get_session


def obtener_metricas_de_videos() -> list[Video]:
    """
    Devuelve una lista de objetos Video que representan las métricas de los videos en la app movil.
    Los videos son devueltos ordenados por la cantidad total de likes.
    """
    with get_session() as session:
        stmt = select(Video).order_by(Video.likes_totales)
        resultados = session.exec(stmt).all()
        return resultados
