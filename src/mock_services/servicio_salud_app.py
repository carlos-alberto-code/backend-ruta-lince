from datetime import datetime, timezone

from schemas.salud import DatosSaludApp


class ServicioSaludApp:

    @staticmethod
    def obtener_datos() -> DatosSaludApp:
        return DatosSaludApp.model_validate(
            {
                "updatedAt": datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z'),
                "pieChart": {"value": 92, "meta": 95},
                "metrics": {
                    "latencyP50": {
                        "label": "Latencia P50",
                        "value": 95,
                        "unit": "ms",
                        "meta": 300,
                        "deltaPct": 5,
                        "trend": "up",
                    },
                    "latencyP95": {
                        "label": "Latencia P95",
                        "value": 290,
                        "unit": "ms",
                        "meta": 300,
                        "deltaPct": 8,
                        "trend": "up",
                    },
                    "appStoreRating": {
                        "label": "App Store Rating (iOS)",
                        "value": 4.8,
                        "unit": "★",
                        "meta": 4.2,
                        "deltaPct": 2,
                        "trend": "up",
                    },
                    "playStoreRating": {
                        "label": "Play Store Rating (Android)",
                        "value": 4.6,
                        "unit": "★",
                        "meta": 4.2,
                        "deltaPct": 3,
                        "trend": "up",
                    },
                },
                "timeseries": {
                    "months": ["Ene", "Feb", "Mar", "Abr", "May", "Jun"],
                    "sessionsOK": [100, 98, 100, 100, 99, 100],
                    "p50": [20, 14, 15, 12, 11, 10],
                    "p95": [360, 350, 358, 320, 310, 285],
                },
            }
        )
