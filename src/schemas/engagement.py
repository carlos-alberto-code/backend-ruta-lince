from typing import List, Optional, Union, Literal
from pydantic import BaseModel


class MetricDataSchema(BaseModel):
    label: str
    value: Union[float, str]  # Puede ser número o string ("14m 20s")
    unit: Optional[str] = None
    deltaPct: Optional[float] = None
    trend: Optional[Literal['up', 'down', 'neutral']] = None
    meta: Union[float, str]


class MetricsContainerSchema(BaseModel):
    sessionsPerUser: MetricDataSchema
    avgSessionTime: MetricDataSchema
    contentDepth: MetricDataSchema


class InteractionRatioSchema(BaseModel):
    value: float
    meta: float


class VideoMetricSchema(BaseModel):
    video: str
    vistas: int
    likeRatio: float
    commentRate: float


class SimpleSeriesSchema(BaseModel):
    data: List[float]


class StyledSeriesSchema(BaseModel):
    data: List[float]
    label: str
    color: str


class AvgSessionChartSchema(BaseModel):
    categories: List[str]
    series: List[SimpleSeriesSchema]


class VideoInteractionsChartSchema(BaseModel):
    categories: List[str]
    series: List[StyledSeriesSchema]


class DatosEngagement(BaseModel):
    metrics: MetricsContainerSchema
    interactionRatio: InteractionRatioSchema
    videoMetrics: List[VideoMetricSchema]
    avgSessionDuration: AvgSessionChartSchema
    videoInteractions: VideoInteractionsChartSchema
