from fastapi import FastAPI
from api.router import enrutador_api
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Ruta Lince API",
    description="API REST para el Dashboard Ruta Lince",
    version="1.0.0",
)

# CORS: Todos los orígenes para el desarrollo en localhost
origenes = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origenes,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", tags=["Salud"])
async def raiz():
    # Este endpoint sirve para verificar rápidamente si la API está funcionando
    # Hay que usarlo cuando tengamos duda sobre si el servidor está respondiendo.
    return {
        "mensaje": "La API está funcionando",
        "version": "1.0.0",
        "estado": "ok"
    }


app.include_router(enrutador_api, prefix="/api")
