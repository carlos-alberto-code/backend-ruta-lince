from typing import List, Optional, Literal
from pydantic import BaseModel


class KpiSchema(BaseModel):
    label: str
    value: float
    unit: Optional[str] = None
    deltaPct: Optional[float] = None
    trend: Optional[Literal['up', 'down', 'flat']] = None
    meta: Optional[str] = None


class GamificationMetricsSchema(BaseModel):
    completionRate: KpiSchema
    avgAttemptsPerGame: KpiSchema


class FunnelDataSchema(BaseModel):
    stages: List[str]
    users: List[int]
    conversionPct: List[float]


class SuccessEvolutionSchema(BaseModel):
    weeks: List[str]
    successRate: List[float]


class DropRateByLevelSchema(BaseModel):
    stages: List[str]
    dropPct: List[float]


class WordAccuracyHeatmapSchema(BaseModel):
    rows: List[str]
    cols: List[str]
    values: List[List[float]]  # Matriz de números para el heatmap


# --- Modelo Principal (Response Model) ---

class DatosGamificacion(BaseModel):
    metrics: GamificationMetricsSchema
    funnel: FunnelDataSchema
    successEvolution: SuccessEvolutionSchema
    dropRate: DropRateByLevelSchema
    wordAccuracy: WordAccuracyHeatmapSchema
