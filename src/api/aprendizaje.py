from fastapi import APIRouter

from src.schemas.aprendizaje import DatosAprendizaje
from src.services.servicio_aprendizaje import ServicioAprendizaje

router = APIRouter(prefix="/aprendizaje", tags=["aprendizaje"])


@router.get(
    "/datos",
    response_model=DatosAprendizaje,
    summary="Obtener datos de aprendizaje",
    description="Devuelve métricas, progreso de simuladores y otros datos"
)
async def obtener_datos_aprendizaje() -> DatosAprendizaje:
    return ServicioAprendizaje.obtener_datos()
