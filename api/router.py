from api import auth
from fastapi import APIRouter

api_router = APIRouter()

api_router.include_router(auth.router)
