from fastapi import APIRouter

from schemas.aprendizaje import PreparacionBenchmark, DatosAprendizaje, MetricasAprendizaje, Metrica, ProgresoSimuladores, TiemposParaAprobar

enrutador = APIRouter(prefix="/aprendizaje", tags=["aprendizaje"])


@enrutador.get(
    "/datos",
    response_model=DatosAprendizaje,
    summary="Obtener datos de aprendizaje",
    description="Devuelve métricas, progreso de simuladores, preparación para benchmark e intentos hasta aprobar."
)
async def obtener_datos_aprendizaje():
    """
    Endpoint para obtener datos completos de la pantalla de aprendizaje.

    Retorna:
    - **metricas**: Métricas principales (mejora de puntaje, promedio quiz, tasa EGEL)
    - **progreso_simuladores**: Progreso semanal de puntajes (promedio, min, max)
    - **preparacion_benchmark**: Porcentaje de usuarios preparados por tema
    - **tiempos_para_aprobar**: Estadísticas de intentos hasta aprobar (mediana, Q1, Q3, min, max)
    """
    # Datos de ejemplo
    return DatosAprendizaje(
        metricas=MetricasAprendizaje(
            mejora_puntaje=Metrica(etiqueta="Mejora de Puntaje", valor=15.5, unidad="%", meta=12.0, porcentaje_delta=8.3,
                                    tendencia="up"),
            promedio_quiz=Metrica(etiqueta="Promedio Quiz", valor=8.2, meta=8.0, porcentaje_delta=2.5, tendencia="up"),
            tasa_intento_egel=Metrica(etiqueta="Tasa Intento EGEL", valor=78.0, unidad="%", meta=80.0, porcentaje_delta=-2.5,
                                   tendencia="down")
        ),
        progreso_simuladores=ProgresoSimuladores(
            semanas=["S1", "S2", "S3", "S4"],
            promedio=[65.0, 70.0, 75.0, 78.0],
            minimo=[50.0, 55.0, 60.0, 65.0],
            maximo=[80.0, 85.0, 88.0, 90.0]
        ),
        preparacion_benchmark=PreparacionBenchmark(
            temas=["Medicina", "Derecho", "Ingeniería"],
            porcentaje=[85.0, 72.0, 90.0]
        ),
        tiempos_para_aprobar=TiemposParaAprobar(
            semanas=["S1", "S2", "S3", "S4"],
            maximo=[5.0, 4.5, 4.0, 3.8],
            minimo=[1.0, 1.0, 1.0, 1.0],
            q3=[3.5, 3.2, 3.0, 2.8],
            q1=[1.8, 1.7, 1.5, 1.4],
            mediana=[2.5, 2.3, 2.0, 1.9]
        )
    )
