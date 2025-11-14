from datetime import datetime, timezone

from fastapi import FastAPI, APIRouter
from src.schemas.salud import DatosSaludApp, SeriesTiempo, Metricas

app = FastAPI()

router = APIRouter(prefix="/salud", tags=["Salud de la App"])


def obtener_datos_ejemplo() -> DatosSaludApp:
    return DatosSaludApp.model_validate(
        {
            "updatedAt": datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z'),
            "pieChart": {"value": 92, "meta": 95},
            "metrics": {
                "latencyP50": {
                    "label": "Latencia p50",
                    "value": 120,
                    "unit": "ms",
                    "meta": 100,
                    "deltaPct": 20,
                    "trend": "down",
                },
                "latencyP95": {
                    "label": "Latencia p95",
                    "value": 320,
                    "unit": "ms",
                    "meta": 300,
                    "deltaPct": 6.7,
                    "trend": "down",
                },
                "appStoreRating": {
                    "label": "Rating App Store",
                    "value": 4.6,
                    "unit": "",
                    "meta": 4.5,
                    "deltaPct": 2.2,
                    "trend": "up",
                },
                "playStoreRating": {
                    "label": "Rating Play Store",
                    "value": 4.4,
                    "unit": "",
                    "meta": 4.5,
                    "deltaPct": -2.2,
                    "trend": "down",
                },
            },
            "timeseries": {
                "months": ["Jul", "Ago", "Sep", "Oct", "Nov"],
                "sessionsOK": [89, 91, 90, 92, 92],
                "p50": [140, 130, 125, 122, 120],
                "p95": [360, 345, 330, 325, 320],
            },
        }
    )


@router.get("/datos", response_model=DatosSaludApp)
async def obtener_salud_app():
    return obtener_datos_ejemplo()


@router.get("/timeseries", response_model=SeriesTiempo)
async def obtener_series_tiempo():
    return obtener_datos_ejemplo().series_tiempo


@router.get("/metrics", response_model=Metricas)
async def obtener_metricas():
    return obtener_datos_ejemplo().metricas
