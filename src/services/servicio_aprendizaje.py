from src.schemas.aprendizaje import (
    DatosAprendizaje,
    MetricasAprendizaje,
    Metrica,
    ProgresoSimuladores,
    PreparacionBenchmark,
    TiemposParaAprobar
)


class ServicioAprendizaje:

    @classmethod
    def obtener_datos(cls) -> DatosAprendizaje:
        # 1. Construcción de KPIs (MetricasAprendizaje)
        # Nota: Usamos los nombres en español (snake_case) gracias a populate_by_name=True
        mis_metricas = MetricasAprendizaje(
            mejora_puntaje=Metrica(
                etiqueta="Mejora de Puntaje",
                valor=15.2,
                unidad="%",
                porcentaje_delta=2.5,
                tendencia="up",
                meta=20.0  # Asumiendo que la meta es numérica según tu modelo
            ),
            promedio_quiz=Metrica(
                etiqueta="Promedio Cuestionarios",
                valor=88.0,
                unidad="/100",
                porcentaje_delta=-1.2,
                tendencia="down",
                meta=90.0
            ),
            tasa_intento_egel=Metrica(
                etiqueta="Tasa Intento EGEL",
                valor=3.5,
                unidad="intentos",
                tendencia="flat",
                meta=5.0
            )
        )

        # 2. Progreso de Simuladores (Gráfico de líneas/área)
        progreso = ProgresoSimuladores(
            semanas=["Sem 1", "Sem 2", "Sem 3", "Sem 4", "Sem 5"],
            promedio=[60.0, 62.5, 70.0, 72.0, 78.5],
            minimo=[50.0, 55.0, 60.0, 65.0, 70.0],
            maximo=[80.0, 82.0, 88.0, 90.0, 95.0]
        )

        # 3. Preparación Benchmark (Radar o Barras)
        benchmark = PreparacionBenchmark(
            temas=[
                "Ing. Software",
                "Bases de Datos",
                "Redes",
                "Gestión de Proyectos",
                "Seguridad"
            ],
            porcentaje=[85.0, 92.5, 60.0, 75.0, 40.0]
        )

        # 4. Tiempos para Aprobar (Box Plot / Velas)
        # Lógica estadística básica: min <= q1 <= mediana <= q3 <= max
        tiempos = TiemposParaAprobar(
            semanas=["Ene", "Feb", "Mar", "Abr"],
            minimo=[10.0, 12.0, 15.0, 18.0],  # Bigote inferior
            q1=[20.0, 25.0, 28.0, 30.0],  # Base de la caja
            mediana=[35.0, 40.0, 42.0, 45.0],  # Línea media
            q3=[50.0, 55.0, 58.0, 60.0],  # Techo de la caja
            maximo=[60.0, 70.0, 75.0, 80.0]  # Bigote superior
        )

        # 5. Retorno del objeto padre completo
        return DatosAprendizaje(
            metricas=mis_metricas,
            progreso_simuladores=progreso,
            preparacion_benchmark=benchmark,
            tiempos_para_aprobar=tiempos
        )
