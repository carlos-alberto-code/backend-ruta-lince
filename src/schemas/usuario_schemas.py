from pydantic import BaseModel, Field
from typing import List, Optional, Literal, Union

Tendencia = Literal['up', 'down', 'flat']


class MetricaUsuario(BaseModel):
    etiqueta: str = Field(..., alias='label')
    valor: float = Field(..., alias='value')
    unidad: Optional[str] = Field(None, alias='unit')
    porcentaje_delta: Optional[float] = Field(None, alias='deltaPct')
    tendencia: Optional[Tendencia] = Field(None, alias='trend')
    meta: Optional[Union[float, str]] = None

    model_config = {"populate_by_name": True}


class MetricasPrincipales(BaseModel):
    ratio_daumau: MetricaUsuario = Field(..., alias='ratioDaumau')
    tasa_abandono: MetricaUsuario = Field(..., alias='churnRate')
    retencion_d1: MetricaUsuario = Field(..., alias='d1Ret')
    retencion_w1: MetricaUsuario = Field(..., alias='w1Ret')
    retencion_m1: MetricaUsuario = Field(..., alias='m1Ret')

    model_config = {"populate_by_name": True}


class InstalacionRegistro(BaseModel):
    conversion_pct: float = Field(..., alias='conversionPct')
    instalaciones: int = Field(..., alias='installs')
    registros: int = Field(..., alias='registers')
    objetivo_pct: float = Field(..., alias='targetPct')

    model_config = {"populate_by_name": True}


class UsuariosActivos(BaseModel):
    meses: List[str] = Field(..., alias='months')
    dau: List[int] = Field(..., alias='dau')
    mau: List[int] = Field(..., alias='mau')

    model_config = {"populate_by_name": True}


class RetencionCohorte(BaseModel):
    meses: List[str] = Field(..., alias='months')
    d1: List[float] = Field(..., alias='d1')
    w1: List[float] = Field(..., alias='w1')
    m1: List[float] = Field(..., alias='m1')

    model_config = {"populate_by_name": True}


class DatosUsuarios(BaseModel):
    metricas: MetricasPrincipales = Field(..., alias='metrics')
    instalar_vs_registrar: InstalacionRegistro = Field(..., alias='installVsRegister')
    usuarios_activos: UsuariosActivos = Field(..., alias='activeUsers')
    retencion: RetencionCohorte = Field(..., alias='retention')

    model_config = {"populate_by_name": True}
