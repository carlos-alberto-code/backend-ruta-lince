from fastapi import APIRouter

from schemas.usuario_schemas import DatosUsuarios
from mock_services.servicio_estudiantes import ServicioUsuariosPrueba
from servicios.servicio_estudiantes import obtener_metricas_estudiantes

router = APIRouter(prefix="/usuarios", tags=["usuarios"])


@router.get(
    "/datos",
    response_model=DatosUsuarios,
    summary="Obtener datos de usuarios",
    description="Devuelve métricas de retención, DAU/MAU y conversión"
)
async def obtener_datos_usuarios() -> DatosUsuarios:
    env = {
        "mock": ServicioUsuariosPrueba.obtener_datos(),
        "real": obtener_metricas_estudiantes()
    }
    return env["real"]
