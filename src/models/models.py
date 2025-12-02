from datetime import date, datetime
from sqlmodel import Field, JSON, Relationship, SQLModel, UniqueConstraint


class Usuario(SQLModel, table=True):
    __tablename__ = 'usuarios'

    id: int | None = Field(default=None, primary_key=True)
    nombre: str = Field(default="", nullable=False)
    apellidos: str = Field(default="", nullable=False)
    email: str = Field(unique=True, nullable=False, index=True, max_length=255)
    contrasena_hash: str = Field(nullable=False, max_length=255)


class Estudiante(SQLModel, table=True):
    __tablename__ = 'estudiantes'

    id: int | None = Field(default=None, primary_key=True)
    fecha_registro: datetime = Field(default_factory=datetime.utcnow)
    ultimo_login: datetime | None = Field(default=None)

    intentos_juego: list["IntentoDesafio"] = Relationship(back_populates="estudiante")
    intentos_simulador: list["IntentoSimulador"] = Relationship(back_populates="estudiante")


class DefinicionMetrica(SQLModel, table=True):
    __tablename__ = "dim_definicion_metricas"

    id: int | None = Field(default=None, primary_key=True)
    clave: str = Field(index=True, unique=True, max_length=50)
    nombre: str = Field(max_length=100)
    unidad: str | None = Field(default=None, max_length=20)
    es_incremento_bueno: bool = Field(default=True)

    registros: list["RegistroMetrica"] = Relationship(back_populates="definicion")


class RegistroMetrica(SQLModel, table=True):
    __tablename__ = "fact_registros_metricas"
    __table_args__ = (
        UniqueConstraint("definicion_id", "fecha", name="uq_metrica_fecha"),
    )

    id: int | None = Field(default=None, primary_key=True)
    fecha: date = Field(index=True)
    valor: float = Field(nullable=False)
    meta_objetivo: float | None = Field(default=None)
    definicion_id: int = Field(foreign_key="dim_definicion_metricas.id")

    definicion: DefinicionMetrica = Relationship(back_populates="registros")


class Video(SQLModel, table=True):
    __tablename__ = "videos"

    id: int | None = Field(default=None, primary_key=True)
    titulo: str = Field(index=True)
    duracion_segundos: int = Field(default=0)
    url_thumbnail: str | None = Field(default=None)
    vistas_totales: int = Field(default=0)
    likes_totales: int = Field(default=0)
    comentarios_totales: int = Field(default=0)


class NivelJuego(SQLModel, table=True):
    __tablename__ = "dim_niveles_juego"

    id: int | None = Field(default=None, primary_key=True)
    nombre: str
    orden: int = Field(unique=True)


class IntentoDesafio(SQLModel, table=True):
    __tablename__ = "fact_intentos_desafio"

    id: int | None = Field(default=None, primary_key=True)
    estudiante_id: int = Field(foreign_key="estudiantes.id", index=True)
    nivel_id: int = Field(foreign_key="dim_niveles_juego.id")
    fecha: datetime = Field(default_factory=datetime.utcnow)
    es_exitoso: bool = Field(default=False)
    puntaje: int = Field(default=0)
    detalle_palabras: dict | None = Field(default=None, sa_type=JSON)

    estudiante: Estudiante = Relationship(back_populates="intentos_juego")


class IntentoSimulador(SQLModel, table=True):
    __tablename__ = "fact_intentos_simulador"

    id: int | None = Field(default=None, primary_key=True)
    estudiante_id: int = Field(foreign_key="estudiantes.id", index=True)
    fecha: datetime = Field(default_factory=datetime.utcnow, index=True)
    tema: str = Field(index=True)
    puntaje_obtenido: float
    tiempo_segundos: int

    estudiante: Estudiante = Relationship(back_populates="intentos_simulador")


class CohorteMensual(SQLModel, table=True):
    __tablename__ = "fact_cohortes_mensuales"

    id: int | None = Field(default=None, primary_key=True)
    mes_cohorte: date = Field(index=True)
    usuarios_iniciales: int = Field(default=0)
    retencion_d1_pct: float = Field(default=0.0)
    retencion_w1_pct: float = Field(default=0.0)
    retencion_m1_pct: float = Field(default=0.0)
