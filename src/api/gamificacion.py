from fastapi import APIRouter

from schemas.gamificacion import DatosGamificacion
from mock_services.servicio_gamificacion import ServicioGamificacion

router = APIRouter(prefix="/gamificacion", tags=["gamificacion"])


@router.get(
    "/datos",
    response_model=DatosGamificacion,
    summary="Obtener datos de gamificación",
    description="Devuelve métricas, embudos de conversión y mapas de calor"
)
async def obtener_datos_aprendizaje() -> DatosGamificacion:
    return ServicioGamificacion.obtener_datos()
