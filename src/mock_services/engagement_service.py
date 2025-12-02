from src.schemas.engagement import (

    AvgSessionChartSchema, DatosEngagement, InteractionRatioSchema, MetricDataSchema, MetricsContainerSchema,
    SimpleSeriesSchema, StyledSeriesSchema, VideoInteractionsChartSchema, VideoMetricSchema)


class ServicioEngagement:
    @staticmethod
    def obtener_datos() -> DatosEngagement:
        """
        Genera y retorna datos mock simulados para el dashboard de engagement.
        """

        # 1. Métricas Principales (KPIs)
        metrics = MetricsContainerSchema(
            sessionsPerUser=MetricDataSchema(
                label="Sesiones por Usuario",
                value=4.5,
                unit="ses/sem",
                deltaPct=15.0,
                trend="up",
                meta=4.0
            ),
            avgSessionTime=MetricDataSchema(
                label="Tiempo Promedio",
                value="18m 30s",
                unit=None,
                deltaPct=3.2,
                trend="down",
                meta="20m 00s"
            ),
            contentDepth=MetricDataSchema(
                label="Profundidad de Contenido",
                value=5.1,
                unit="páginas",
                deltaPct=0.0,
                trend="neutral",
                meta=5.0
            )
        )

        # 2. Ratio de Interacción (Gauge Chart)
        # Ponemos value > meta para que salga verde en tu frontend, o al revés para probar rojo
        interaction_ratio = InteractionRatioSchema(
            value=72.5,
            meta=70.0
        )

        # 3. Tabla de Métricas de Video
        video_metrics = [
            VideoMetricSchema(video="Intro a la Arquitectura", vistas=1500, likeRatio=9.1, commentRate=1.5),
            VideoMetricSchema(video="Patrones de Diseño", vistas=1200, likeRatio=8.8, commentRate=2.2),
            VideoMetricSchema(video="Cybersecurity Basics", vistas=2300, likeRatio=9.5, commentRate=0.8),
            VideoMetricSchema(video="React Hooks", vistas=980, likeRatio=7.9, commentRate=3.5),
            VideoMetricSchema(video="Gestión de Bases de Datos", vistas=1750, likeRatio=8.2, commentRate=1.1),
        ]

        # 4. Gráfico de Barras: Duración de Sesión (Simple)
        avg_session_duration = AvgSessionChartSchema(
            categories=["Lun", "Mar", "Mié", "Jue", "Vie", "Sáb", "Dom"],
            series=[
                SimpleSeriesSchema(data=[15, 22, 18, 25, 20, 12, 10])
            ]
        )

        # 5. Gráfico de Barras: Interacciones por Video (Agrupado/Coloreado)
        # Nota: Los colores coinciden con lo que espera tu frontend para pintar las barras
        video_interactions = VideoInteractionsChartSchema(
            categories=["Likes", "Shares", "Comments", "Saves"],
            series=[
                StyledSeriesSchema(
                    data=[500, 220, 180, 350],
                    label="Interacciones Totales",
                    color="#2563EB"  # Azul
                ),
                StyledSeriesSchema(
                    data=[60, 40, 25, 55],
                    label="Interacciones Únicas",
                    color="#10B981"  # Verde
                )
            ]
        )

        return DatosEngagement(
            metrics=metrics,
            interactionRatio=interaction_ratio,
            videoMetrics=video_metrics,
            avgSessionDuration=avg_session_duration,
            videoInteractions=video_interactions
        )
