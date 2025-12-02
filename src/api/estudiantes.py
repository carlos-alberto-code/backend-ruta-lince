from fastapi import APIRouter

from mock_services.servicio_estudiantes import ServicioUsuariosPrueba
from src.schemas.usuario_schemas import DatosUsuarios
from src.servicios.servicio_estudiantes import obtener_metricas_estudiantes

router = APIRouter(prefix="/usuarios", tags=["usuarios"])


@router.get(
    "/datos",
    response_model=DatosUsuarios,
    summary="Obtener datos de usuarios",
    description="Devuelve métricas de retención, DAU/MAU y conversión"
)
async def obtener_datos_usuarios() -> DatosUsuarios:
    env = {
        "mock": ServicioUsuariosPrueba(),
        "ok": obtener_metricas_estudiantes()
    }
    return env["mock"].obtener_datos()
