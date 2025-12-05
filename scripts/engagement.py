from database.repository import create_many
from src.models.models import Video
from src.database.repository import create


def crear_tabla(modelo):
    from src.database.connection import engine
    modelo.metadata.create_all(engine)


if __name__ == "__main__":
    videos_ejemplo = [
        Video(
            nombre="Introducción a Python",
            duracion=600.0,
            vistas_totales=1000,
            likes_totales=150,
            comentarios_totales=20
        ),
        Video(
            nombre="Aprendiendo FastAPI",
            duracion=900.0,
            vistas_totales=800,
            likes_totales=120,
            comentarios_totales=15
        ),
        Video(
            nombre="Bases de Datos con SQLModel",
            duracion=750.0,
            vistas_totales=950,
            likes_totales=130,
            comentarios_totales=18
        ),
        Video(
            nombre="Desarrollo Web con React",
            duracion=850.0,
            vistas_totales=1100,
            likes_totales=160,
            comentarios_totales=25
        ),
        Video(
            nombre="Introducción a Docker",
            duracion=700.0,
            vistas_totales=900,
            likes_totales=140,
            comentarios_totales=22
        ),
        Video(
            nombre="Kubernetes para Principiantes",
            duracion=950.0,
            vistas_totales=750,
            likes_totales=110,
            comentarios_totales=12
        )
    ]
    try:
        creados = create_many(videos_ejemplo)
        print([v.id for v in creados])
    except Exception as e:
        import traceback

        print("Error al crear los videos de ejemplo:", e)
        traceback.print_exc()
