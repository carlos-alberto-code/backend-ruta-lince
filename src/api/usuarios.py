from fastapi import APIRouter

from schemas.usuario_schemas import DatosUsuarios
from services.servicio_usuarios import ServicioUsuarios

router = APIRouter(prefix="/usuarios", tags=["usuarios"])


@router.get(
    "/datos",
    response_model=DatosUsuarios,
    summary="Obtener datos de usuarios",
    description="Devuelve métricas de retención, DAU/MAU y conversión"
)
async def obtener_datos_usuarios() -> DatosUsuarios:
    return ServicioUsuarios.obtener_datos()
