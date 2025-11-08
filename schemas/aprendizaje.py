from pydantic import BaseModel, Field
from typing import List, Optional, Literal

Trend = Literal['up', 'down', 'flat']


class Metric(BaseModel):
    label: str
    value: float
    unit: Optional[str] = None
    meta: Optional[float] = None
    delta_pct: Optional[float] = Field(None, alias='deltaPct')
    trend: Optional[Trend] = None

    class Config:
        allow_population_by_field_name = True


class SimulatorsProgress(BaseModel):
    weeks: List[str]
    avg: List[float]
    min: List[float]
    max: List[float]


class BenchmarkPrep(BaseModel):
    topics: List[str]
    percent: List[float]


class TimesToPass(BaseModel):
    weeks: List[str]
    max: List[float]
    min: List[float]
    q3: List[float]
    q1: List[float]
    median: List[float]


class LearningMetrics(BaseModel):
    score_improvement: Metric = Field(..., alias='scoreImprovement')
    quiz_avg: Metric = Field(..., alias='quizAvg')
    egel_attempt_rate: Metric = Field(..., alias='egelAttemptRate')

    class Config:
        allow_population_by_field_name = True


class LearningData(BaseModel):
    metrics: LearningMetrics
    simulators_progress: SimulatorsProgress = Field(..., alias='simulatorsProgress')
    benchmark_prep: BenchmarkPrep = Field(..., alias='benchmarkPrep')
    times_to_pass: TimesToPass = Field(..., alias='timesToPass')

    class Config:
        allow_population_by_field_name = True
