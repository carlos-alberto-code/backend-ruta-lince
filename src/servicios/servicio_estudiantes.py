from typing import Any, Tuple

from sqlmodel import Session, desc, func, select

from database import get_session
from models.models import CohorteMensual, DefinicionMetrica, Estudiante, RegistroMetrica
from schemas.usuario_schemas import (
    DatosUsuarios, InstalacionRegistro, MetricaUsuario,
    MetricasPrincipales, RetencionCohorte, Tendencia, UsuariosActivos
)


def _calcular_tendencia(actual: float, previo: float) -> Tuple[float, Tendencia]:
    if previo == 0:
        return 0.0, "flat"

    delta = ((actual - previo) / previo) * 100
    if delta > 0.5:
        return delta, "up"
    elif delta < -0.5:
        return delta, "down"
    return delta, "flat"


def _obtener_valor_metrica_reciente(session: Session, clave_metrica: str) -> Tuple[float, float]:
    statement = (
        select(RegistroMetrica.valor)
        .join(DefinicionMetrica)
        .where(DefinicionMetrica.clave == clave_metrica)
        .order_by(desc(RegistroMetrica.fecha))
        .limit(2)
    )
    resultados = session.exec(statement).all()

    actual = resultados[0] if len(resultados) > 0 else 0.0
    previo = resultados[1] if len(resultados) > 1 else 0.0

    return actual, previo


def _construir_metrica_usuario(
        etiqueta: str,
        valor: float,
        previo: float,
        unidad: str = None,
        meta: Any = None
) -> MetricaUsuario:
    delta, tendencia = _calcular_tendencia(valor, previo)

    return MetricaUsuario(
        label=etiqueta,
        value=round(valor, 2),
        unit=unidad,
        deltaPct=round(delta, 1),
        trend=tendencia,
        meta=meta
    )


def obtener_metricas_estudiantes() -> DatosUsuarios:
    with get_session() as session:

        stmt_cohortes = select(CohorteMensual).order_by(CohorteMensual.mes_cohorte)
        cohortes = session.exec(stmt_cohortes).all()

        meses_fmt = [c.mes_cohorte.strftime("%b") for c in cohortes]
        d1_list = [c.retencion_d1_pct for c in cohortes]
        w1_list = [c.retencion_w1_pct for c in cohortes]
        m1_list = [c.retencion_m1_pct for c in cohortes]

        obj_retencion = RetencionCohorte(
            months=meses_fmt[-6:] if meses_fmt else [],
            d1=d1_list[-6:] if d1_list else [],
            w1=w1_list[-6:] if w1_list else [],
            m1=m1_list[-6:] if m1_list else []
        )

        ultima_cohorte = cohortes[-1] if cohortes else CohorteMensual()
        penultima_cohorte = cohortes[-2] if len(cohortes) > 1 else CohorteMensual()

        dau_actual, dau_previo = _obtener_valor_metrica_reciente(session, "DAU")
        mau_actual, mau_previo = _obtener_valor_metrica_reciente(session, "MAU")

        ratio_actual = (dau_actual / mau_actual) * 100 if mau_actual > 0 else 0
        ratio_previo = (dau_previo / mau_previo) * 100 if mau_previo > 0 else 0

        churn_actual = 100 - ultima_cohorte.retencion_m1_pct
        churn_previo = 100 - penultima_cohorte.retencion_m1_pct

        metricas_principales = MetricasPrincipales(
            ratioDaumau=_construir_metrica_usuario("Ratio DAU/MAU", ratio_actual, ratio_previo, "%", "> 20%"),
            churnRate=_construir_metrica_usuario("Tasa de Abandono", churn_actual, churn_previo, "%", "< 5%"),
            d1Ret=_construir_metrica_usuario("Retención D1", ultima_cohorte.retencion_d1_pct,
                                             penultima_cohorte.retencion_d1_pct, "%"),
            w1Ret=_construir_metrica_usuario("Retención W1", ultima_cohorte.retencion_w1_pct,
                                             penultima_cohorte.retencion_w1_pct, "%"),
            m1Ret=_construir_metrica_usuario("Retención M1", ultima_cohorte.retencion_m1_pct,
                                             penultima_cohorte.retencion_m1_pct, "%")
        )

        total_registros = session.exec(select(func.count(Estudiante.id))).one()

        stmt_installs = (
            select(func.sum(RegistroMetrica.valor))
            .join(DefinicionMetrica)
            .where(DefinicionMetrica.clave == "INSTALACIONES")
        )
        total_instalaciones = session.exec(stmt_installs).one() or 0

        conversion = 0.0
        if total_instalaciones > 0:
            conversion = (float(total_registros) / float(total_instalaciones)) * 100

        obj_funnel = InstalacionRegistro(
            conversionPct=round(conversion, 1),
            installs=int(total_instalaciones),
            registers=total_registros,
            targetPct=45.0
        )

        stmt_hist_dau = (
            select(RegistroMetrica.valor)
            .join(DefinicionMetrica)
            .where(DefinicionMetrica.clave == "DAU")
            .order_by(RegistroMetrica.fecha)
            .limit(6)
        )
        hist_dau = session.exec(stmt_hist_dau).all()

        while len(hist_dau) < len(meses_fmt[-6:]):
            hist_dau.insert(0, 0)

        hist_mau = [v * 3 for v in hist_dau]

        obj_activos = UsuariosActivos(
            months=meses_fmt[-6:],
            dau=[int(v) for v in hist_dau],
            mau=[int(v) for v in hist_mau]
        )

        return DatosUsuarios(
            metrics=metricas_principales,
            installVsRegister=obj_funnel,
            activeUsers=obj_activos,
            retention=obj_retencion
        )
