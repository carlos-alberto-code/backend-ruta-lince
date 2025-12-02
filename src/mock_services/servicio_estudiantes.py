from collections import defaultdict

from sqlmodel import select

from src.database.connection import get_session
from src.models.models import DefinicionMetrica, RegistroMetrica
from src.schemas.usuario_schemas import (
    DatosUsuarios, InstalacionRegistro,
    MetricaUsuario, MetricasPrincipales,
    RetencionCohorte, UsuariosActivos
)


class ServicioUsuariosPrueba:

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


def _obtener_historico_completo() -> list[tuple[RegistroMetrica, DefinicionMetrica]]:
    with get_session() as session:
        statement = (
            select(RegistroMetrica, DefinicionMetrica)
            .join(DefinicionMetrica)
            .order_by(RegistroMetrica.fecha)
        )
        return session.exec(statement).all()


def _agrupar_por_clave(resultados: list[tuple[RegistroMetrica, DefinicionMetrica]]) -> dict[
    str, list[RegistroMetrica]]:
    agrupado = defaultdict(list)
    for registro, definicion in resultados:
        # Adjuntamos la definición al registro temporalmente para tener acceso fácil
        registro.definicion = definicion
        agrupado[definicion.clave].append(registro)
    return agrupado


def _calcular_tendencia(actual: float, previo: float, es_bueno: bool) -> tuple[float, str]:
    if previo == 0:
        delta = 0.0
    else:
        delta = ((actual - previo) / previo) * 100

    delta = round(delta, 1)

    # Determinar dirección visual
    if delta > 0.1:
        trend = "up"
    elif delta < -0.1:
        trend = "down"
    else:
        trend = "flat"

    return delta, trend


def _crear_obj_metrica(clave: str, datos: list[RegistroMetrica]) -> MetricaUsuario:
    if not datos:
        return MetricaUsuario(etiqueta="N/A", valor=0, tendencia="flat")

    actual = datos[-1]
    previo = datos[-2] if len(datos) > 1 else actual

    delta, trend = _calcular_tendencia(
        actual.valor,
        previo.valor,
        actual.definicion.es_incremento_bueno
    )

    meta_val = actual.meta_objetivo if actual.meta_objetivo is not None else None

    return MetricaUsuario(
        etiqueta=actual.definicion.nombre,
        valor=actual.valor,
        unidad=actual.definicion.unidad,
        porcentaje_delta=delta,
        tendencia=trend,
        meta=meta_val
    )


def _construir_kpis(data: dict[str, list[RegistroMetrica]]) -> MetricasPrincipales:
    return MetricasPrincipales(
        ratio_daumau=_crear_obj_metrica('ratio_daumau', data.get('ratio_daumau', [])),
        tasa_abandono=_crear_obj_metrica('churn_rate', data.get('churn_rate', [])),
        retencion_d1=_crear_obj_metrica('ret_d1', data.get('ret_d1', [])),
        retencion_w1=_crear_obj_metrica('ret_w1', data.get('ret_w1', [])),
        retencion_m1=_crear_obj_metrica('ret_m1', data.get('ret_m1', []))
    )


def _construir_funnel(data: dict[str, list[RegistroMetrica]]) -> InstalacionRegistro:
    installs_list = data.get('installs', [])
    registers_list = data.get('registers', [])

    inst = installs_list[-1].valor if installs_list else 0
    reg = registers_list[-1].valor if registers_list else 0

    conv = (reg / inst * 100) if inst > 0 else 0.0

    target = registers_list[-1].meta_objetivo if registers_list and registers_list[-1].meta_objetivo else 70.0

    return InstalacionRegistro(
        conversion_pct=round(conv, 1),
        instalaciones=int(inst),
        registros=int(reg),
        objetivo_pct=target
    )


def _formatear_meses(registros: list[RegistroMetrica]) -> list[str]:
    meses_abbr = {1: "Ene", 2: "Feb", 3: "Mar", 4: "Abr", 5: "May", 6: "Jun",
                  7: "Jul", 8: "Ago", 9: "Sep", 10: "Oct", 11: "Nov", 12: "Dic"}
    return [meses_abbr.get(r.fecha.month, "") for r in registros]


def _construir_grafico_retencion(data: dict[str, list[RegistroMetrica]]) -> RetencionCohorte:
    ref_data = data.get('ret_d1', [])

    return RetencionCohorte(
        meses=_formatear_meses(ref_data),
        d1=[r.valor for r in data.get('ret_d1', [])],
        w1=[r.valor for r in data.get('ret_w1', [])],
        m1=[r.valor for r in data.get('ret_m1', [])]
    )


def _construir_grafico_activos(data: dict[str, list[RegistroMetrica]]) -> UsuariosActivos:
    dau_data = data.get('dau', [])
    mau_data = data.get('mau', [])

    return UsuariosActivos(
        meses=_formatear_meses(dau_data),
        dau=[int(r.valor) for r in dau_data],
        mau=[int(r.valor) for r in mau_data]
    )


def obtener_datos() -> DatosUsuarios:
    raw_data = _obtener_historico_completo()
    data_map = _agrupar_por_clave(raw_data)
    metricas_kpi = _construir_kpis(data_map)
    funnel = _construir_funnel(data_map)
    grafico_activos = _construir_grafico_activos(data_map)
    grafico_retencion = _construir_grafico_retencion(data_map)

    return DatosUsuarios(
        metricas=metricas_kpi,
        instalar_vs_registrar=funnel,
        usuarios_activos=grafico_activos,
        retencion=grafico_retencion
    )
