from api import login
from fastapi import APIRouter

enrutador_api = APIRouter()

enrutador_api.include_router(auth.enrutador)
