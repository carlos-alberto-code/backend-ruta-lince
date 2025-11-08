from fastapi import FastAPI
from api.router import api_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Ruta Lince API",
    description="API REST para el Dashboard Ruta Lince",
    version="1.0.0",
)

# CORS para desarrollo en localhost
origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://localhost:8080",
    "http://localhost:5173",
    "http://127.0.0.1",
    "http://127.0.0.1:3000",
    "http://127.0.0.1:8080",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
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


app.include_router(api_router, prefix="/api/v1")
