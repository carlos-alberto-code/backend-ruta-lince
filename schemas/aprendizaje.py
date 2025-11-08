from pydantic import BaseModel, Field
from typing import List, Optional, Literal

Tendencia = Literal['up', 'down', 'flat']


class Metrica(BaseModel):
    etiqueta: str = Field(..., alias='label')
    valor: float = Field(..., alias='value')
    unidad: Optional[str] = Field(None, alias='unit')
    meta: Optional[float] = None
    porcentaje_delta: Optional[float] = Field(None, alias='deltaPct')
    tendencia: Optional[Tendencia] = Field(None, alias='trend')

    model_config = {"populate_by_name": True}


class ProgresoSimuladores(BaseModel):
    semanas: List[str] = Field(..., alias='weeks')
    promedio: List[float] = Field(..., alias='avg')
    minimo: List[float] = Field(..., alias='min')
    maximo: List[float] = Field(..., alias='max')

    model_config = {"populate_by_name": True}


class PreparacionBenchmark(BaseModel):
    temas: List[str] = Field(..., alias='topics')
    porcentaje: List[float] = Field(..., alias='percent')

    model_config = {"populate_by_name": True}


class TiemposParaAprobar(BaseModel):
    semanas: List[str] = Field(..., alias='weeks')
    maximo: List[float] = Field(..., alias='max')
    minimo: List[float] = Field(..., alias='min')
    q3: List[float] = Field(..., alias='q3')
    q1: List[float] = Field(..., alias='q1')
    mediana: List[float] = Field(..., alias='median')

    model_config = {"populate_by_name": True}


class MetricasAprendizaje(BaseModel):
    mejora_puntaje: Metrica = Field(..., alias='scoreImprovement')
    promedio_quiz: Metrica = Field(..., alias='quizAvg')
    tasa_intento_egel: Metrica = Field(..., alias='egelAttemptRate')

    model_config = {"populate_by_name": True}


class DatosAprendizaje(BaseModel):
    metricas: MetricasAprendizaje = Field(..., alias='metrics')
    progreso_simuladores: ProgresoSimuladores = Field(..., alias='simulatorsProgress')
    preparacion_benchmark: PreparacionBenchmark = Field(..., alias='benchmarkPrep')
    tiempos_para_aprobar: TiemposParaAprobar = Field(..., alias='timesToPass')

    model_config = {"populate_by_name": True}
