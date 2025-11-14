from typing import Literal
from datetime import datetime

from pydantic import BaseModel, Field

Tendencia = Literal['up', 'down', 'flat']


class Metrica(BaseModel):
    etiqueta: str = Field(..., alias='label')
    valor: float | str = Field(..., alias='value')
    unidad: str | None = Field(None, alias='unit')
    meta: float | str | None = None
    porcentaje_delta: float | None = Field(None, alias='deltaPct')
    tendencia: Tendencia | None = Field(None, alias='trend')

    model_config = {
        "populate_by_name": True,
        "json_schema_extra": {
            "example": {
                "label": "Latencia p50",
                "value": 120,
                "unit": "ms",
                "meta": 100,
                "deltaPct": 20,
                "trend": "down"
            }
        }
    }


class DatosGraficoCircular(BaseModel):
    valor: float = Field(..., alias='value')
    meta: float

    model_config = {
        "populate_by_name": True,
        "json_schema_extra": {"example": {"value": 92, "meta": 95}}
    }


class SeriesTiempo(BaseModel):
    meses: list[str] = Field(..., alias='months')
    sesiones_ok: list[float] = Field(..., alias='sessionsOK')
    p50: list[float]
    p95: list[float]

    model_config = {
        "populate_by_name": True,
        "json_schema_extra": {
            "example": {
                "months": ["Jul", "Ago", "Sep", "Oct", "Nov"],
                "sessionsOK": [89, 91, 90, 92, 92],
                "p50": [140, 130, 125, 122, 120],
                "p95": [360, 345, 330, 325, 320],
            }
        }
    }


class Metricas(BaseModel):
    latencia_p50: Metrica = Field(..., alias='latencyP50')
    latencia_p95: Metrica = Field(..., alias='latencyP95')
    rating_app_store: Metrica = Field(..., alias='appStoreRating')
    rating_play_store: Metrica = Field(..., alias='playStoreRating')

    model_config = {"populate_by_name": True}


class DatosSaludApp(BaseModel):
    actualizado_en: datetime | None = Field(None, alias='updatedAt')
    grafico_circular: DatosGraficoCircular = Field(..., alias='pieChart')
    metricas: Metricas = Field(..., alias='metrics')
    series_tiempo: SeriesTiempo = Field(..., alias='timeseries')

    model_config = {"populate_by_name": True}
