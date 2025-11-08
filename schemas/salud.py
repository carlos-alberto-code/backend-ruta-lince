from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field

Trend = Literal['up', 'down', 'flat']


class Metric(BaseModel):
    label: str
    value: float | str
    unit: str | None = None
    meta: float | str | None = None
    delta_pct: float | None = Field(None, alias='deltaPct')
    trend: Trend | None = None

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "label": "Latencia p50",
                "value": 120,
                "unit": "ms",
                "meta": 100,
                "deltaPct": 20,
                "trend": "down"
            }
        }


class PieChartData(BaseModel):
    value: float
    meta: float

    class Config:
        schema_extra = {"example": {"value": 92, "meta": 95}}


class Timeseries(BaseModel):
    months: list[str]
    sessions_ok: list[float] = Field(..., alias='sessionsOK')
    p50: list[float]
    p95: list[float]

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "months": ["Jul", "Ago", "Sep", "Oct", "Nov"],
                "sessionsOK": [89, 91, 90, 92, 92],
                "p50": [140, 130, 125, 122, 120],
                "p95": [360, 345, 330, 325, 320],
            }
        }


class Metrics(BaseModel):
    latency_p50: Metric = Field(..., alias='latencyP50')
    latency_p95: Metric = Field(..., alias='latencyP95')
    app_store_rating: Metric = Field(..., alias='appStoreRating')
    play_store_rating: Metric = Field(..., alias='playStoreRating')

    class Config:
        allow_population_by_field_name = True


class AppHealthData(BaseModel):
    updated_at: datetime | None = Field(None, alias='updatedAt')
    pie_chart: PieChartData = Field(..., alias='pieChart')
    metrics: Metrics
    timeseries: Timeseries

    class Config:
        allow_population_by_field_name = True
