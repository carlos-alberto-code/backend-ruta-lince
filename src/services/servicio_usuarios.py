from schemas.usuario_schemas import DatosUsuarios, InstalacionRegistro, MetricaUsuario, MetricasPrincipales, \
    RetencionCohorte, \
    UsuariosActivos


class ServicioUsuarios:

    @classmethod
    def obtener_datos(cls) -> DatosUsuarios:
        # 1. Métricas Principales (KPIs superiores)
        mis_metricas = MetricasPrincipales(
            ratio_daumau=MetricaUsuario(
                etiqueta="Ratio DAU/MAU",
                valor=42.5,
                unidad="%",
                porcentaje_delta=1.5,
                tendencia="up",
                meta="> 40%"  # Ejemplo usando string como meta
            ),
            tasa_abandono=MetricaUsuario(
                etiqueta="Churn Rate",
                valor=5.8,
                unidad="%",
                porcentaje_delta=-0.5,  # Negativo es bueno en churn, trend indica dirección visual
                tendencia="down",  # Flecha hacia abajo (verde si la lógica de UI lo maneja así)
                meta=5.0  # Ejemplo usando float como meta
            ),
            retencion_d1=MetricaUsuario(
                etiqueta="Retención Día 1",
                valor=45.2,
                unidad="%",
                porcentaje_delta=2.1,
                tendencia="up",
                meta=45.0
            ),
            retencion_w1=MetricaUsuario(
                etiqueta="Retención Sem 1",
                valor=28.4,
                unidad="%",
                porcentaje_delta=0.1,
                tendencia="flat"
            ),
            retencion_m1=MetricaUsuario(
                etiqueta="Retención Mes 1",
                valor=15.0,
                unidad="%",
                porcentaje_delta=-1.2,
                tendencia="down"
            )
        )

        # 2. Funnel de Instalación vs Registro
        funnel = InstalacionRegistro(
            conversion_pct=65.0,
            instalaciones=1200,
            registros=780,
            objetivo_pct=70.0
        )

        # 3. Usuarios Activos (Gráfico de Barras o Líneas)
        activos = UsuariosActivos(
            meses=["Ene", "Feb", "Mar", "Abr", "May"],
            dau=[1050, 1100, 1150, 1300, 1450],  # Usuarios Diarios
            mau=[3100, 3250, 3400, 3800, 4100]  # Usuarios Mensuales
        )

        # 4. Curvas de Retención (Gráfico de Líneas comparativas)
        retencion_grafico = RetencionCohorte(
            meses=["Ene", "Feb", "Mar", "Abr", "May"],
            d1=[40.0, 42.0, 44.0, 45.0, 45.2],  # Mejora continua
            w1=[25.0, 26.0, 27.0, 28.0, 28.4],
            m1=[12.0, 13.0, 14.0, 14.5, 15.0]
        )

        # 5. Retorno del objeto padre
        return DatosUsuarios(
            metricas=mis_metricas,
            instalar_vs_registrar=funnel,
            usuarios_activos=activos,
            retencion=retencion_grafico
        )
