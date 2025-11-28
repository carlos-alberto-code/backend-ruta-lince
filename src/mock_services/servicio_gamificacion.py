from schemas.gamificacion import DatosGamificacion, DropRateByLevelSchema, FunnelDataSchema, GamificationMetricsSchema, \
    KpiSchema, \
    SuccessEvolutionSchema, WordAccuracyHeatmapSchema


class ServicioGamificacion:
    @staticmethod
    def obtener_datos() -> DatosGamificacion:
        """
        Genera y retorna datos mock simulados para el dashboard de Gamificación.
        """

        # 1. KPIs Principales
        metrics = GamificationMetricsSchema(
            completionRate=KpiSchema(
                label="Tasa de Finalización Global",
                value=68.5,
                unit="%",
                deltaPct=5.2,
                trend="up",
                meta="75%"
            ),
            avgAttemptsPerGame=KpiSchema(
                label="Intentos Promedio por Juego",
                value=2.4,
                unit=None,
                deltaPct=1.1,
                trend="down",  # 'down' es bueno aquí (menos intentos = mejor comprensión)
                meta="2.0"
            )
        )

        # 2. Funnel de Juegos (Debe ser decreciente en usuarios)
        funnel = FunnelDataSchema(
            stages=["Inicio", "Tutorial", "Nivel 1", "Nivel 2", "Boss Final"],
            users=[1200, 1150, 980, 850, 600],
            conversionPct=[100, 95.8, 85.2, 86.7, 70.5]
        )

        # 3. Evolución de Tasa de Éxito (Line Chart)
        success_evolution = SuccessEvolutionSchema(
            weeks=["Sem 1", "Sem 2", "Sem 3", "Sem 4", "Sem 5"],
            successRate=[45, 52, 68, 70, 78]  # Tendencia ascendente de aprendizaje
        )

        # 4. Tasa de Abandono por Nivel (Bar Chart)
        drop_rate = DropRateByLevelSchema(
            stages=["Nivel 1", "Nivel 2", "Nivel 3", "Nivel 4", "Nivel 5"],
            dropPct=[5, 12, 25, 18, 10]
        )

        # 5. Mapa de Calor (Aciertos por Palabra)
        # Filas = Niveles, Columnas = Palabras/Conceptos
        word_accuracy = WordAccuracyHeatmapSchema(
            rows=["Nivel 1", "Nivel 2", "Nivel 3"],
            cols=["Concepto A", "Concepto B", "Concepto C", "Concepto D"],
            values=[
                [90, 85, 70, 95],  # Valores para Nivel 1
                [80, 60, 55, 88],  # Valores para Nivel 2 (más difícil)
                [75, 50, 45, 82]  # Valores para Nivel 3 (aún más difícil)
            ]
        )

        return DatosGamificacion(
            metrics=metrics,
            funnel=funnel,
            successEvolution=success_evolution,
            dropRate=drop_rate,
            wordAccuracy=word_accuracy
        )
