from api import login, aprendizaje, salud
from fastapi import APIRouter

router = APIRouter()

router.include_router(login.router)
router.include_router(salud.router)
router.include_router(aprendizaje.router)
