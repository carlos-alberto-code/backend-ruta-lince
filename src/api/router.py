from fastapi import APIRouter
from src.api import login, aprendizaje, salud, usuarios

router = APIRouter()

router.include_router(login.router)
router.include_router(salud.router)
router.include_router(usuarios.router)
router.include_router(aprendizaje.router)
