from fastapi import APIRouter

from schemas.engagement import DatosEngagement
from mock_services.engagement_service import ServicioEngagement

router = APIRouter(prefix="/engagement", tags=["engagement"])


@router.get(
    "/datos",
    response_model=DatosEngagement,
    summary="Obtener datos de engagement",
    description="Devuelve métricas, progreso de simuladores y otros datos"
)
async def obtener_datos_aprendizaje() -> DatosEngagement:
    return ServicioEngagement.obtener_datos()
