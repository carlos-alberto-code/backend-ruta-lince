from fastapi import APIRouter

from schemas.aprendizaje import BenchmarkPrep, LearningData, LearningMetrics, Metric, SimulatorsProgress, TimesToPass

router = APIRouter(prefix="/aprendizaje", tags=["aprendizaje"])


@router.get(
    "/datos",
    response_model=LearningData,
    summary="Obtener datos de aprendizaje",
    description="Devuelve métricas, progreso de simuladores, preparación para benchmark e intentos hasta aprobar."
)
async def obtener_datos_aprendizaje():
    """
    Endpoint para obtener datos completos de la pantalla de aprendizaje.

    Retorna:
    - **metrics**: Métricas principales (mejora de puntaje, promedio quiz, tasa EGEL)
    - **simulatorsProgress**: Progreso semanal de puntajes (avg, min, max)
    - **benchmarkPrep**: Porcentaje de usuarios preparados por tema
    - **timesToPass**: Estadísticas de intentos hasta aprobar (mediana, Q1, Q3, min, max)
    """
    # Mock data de ejemplo
    return LearningData(
        metrics=LearningMetrics(
            scoreImprovement=Metric(label="Mejora de Puntaje", value=15.5, unit="%", meta=12.0, deltaPct=8.3,
                                    trend="up"),
            quizAvg=Metric(label="Promedio Quiz", value=8.2, meta=8.0, deltaPct=2.5, trend="up"),
            egelAttemptRate=Metric(label="Tasa Intento EGEL", value=78.0, unit="%", meta=80.0, deltaPct=-2.5,
                                   trend="down")
        ),
        simulatorsProgress=SimulatorsProgress(
            weeks=["S1", "S2", "S3", "S4"],
            avg=[65.0, 70.0, 75.0, 78.0],
            min=[50.0, 55.0, 60.0, 65.0],
            max=[80.0, 85.0, 88.0, 90.0]
        ),
        benchmarkPrep=BenchmarkPrep(
            topics=["Medicina", "Derecho", "Ingeniería"],
            percent=[85.0, 72.0, 90.0]
        ),
        timesToPass=TimesToPass(
            weeks=["S1", "S2", "S3", "S4"],
            max=[5.0, 4.5, 4.0, 3.8],
            min=[1.0, 1.0, 1.0, 1.0],
            q3=[3.5, 3.2, 3.0, 2.8],
            q1=[1.8, 1.7, 1.5, 1.4],
            median=[2.5, 2.3, 2.0, 1.9]
        )
    )
