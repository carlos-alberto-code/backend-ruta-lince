from fastapi import FastAPI
from api.router import api_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Ruta Lince API",
    description="API REST para el Dashboard Ruta Lince",
    version="1.0.0",
)

# CORS: Todos los orígenes para el desarrollo en localhost
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", tags=["Health"])
async def root():
    # Este endpoint sirve para verificar rápidamente si la API está funcionando
    # Hay que usarlo cuando tengamos duda sobre si el servidor está respondiendo.
    return {
        "message": "La API está funcionando",
        "version": "1.0.0",
        "status": "ok"
    }


app.include_router(api_router, prefix="/api")
