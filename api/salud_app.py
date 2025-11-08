from datetime import datetime, timezone

from fastapi import FastAPI, APIRouter
from schemas.salud_app import AppHealthData, Timeseries, Metrics

app = FastAPI()
router = APIRouter(prefix="/api/app-health", tags=["app-health"])


def get_mock_data() -> AppHealthData:
    return AppHealthData.parse_obj(
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


@router.get("/", response_model=AppHealthData)
async def get_app_health():
    return get_mock_data()


@router.get("/timeseries", response_model=Timeseries)
async def get_timeseries():
    return get_mock_data().timeseries


@router.get("/metrics", response_model=Metrics)
async def get_metrics():
    return get_mock_data().metrics


app.include_router(router)
