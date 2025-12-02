from fastapi import APIRouter

from src.schemas.salud import DatosSaludApp
from src.mock_services.servicio_salud_app import ServicioSaludApp

router = APIRouter(prefix="/salud", tags=["Salud de la App"])


@router.get("/datos", response_model=DatosSaludApp)
async def obtener_salud_app():
    return ServicioSaludApp.obtener_datos()
