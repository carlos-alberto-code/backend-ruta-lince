from fastapi import FastAPI
from api.router import api_router
from fastapi.middleware.cors import CORSMiddleware
from database.database import crear_db_y_tablas

app = FastAPI(
    title="Ruta Lince API",
    description="API REST para el sistema Ruta Lince",
    version="0.1.0",
)


@app.on_event("startup")
def on_startup():
    """
    Evento que se ejecuta al iniciar la aplicación.
    Crea las tablas de la base de datos si no existen.
    """
    crear_db_y_tablas()


# Configuración CORS para desarrollo en localhost
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
        "version": "0.1.0",
        "status": "ok"
    }


@app.get("/health", tags=["Health"])
async def health_check():
    # Endpoint de health check para monitoring y verificación de disponibilidad
    return {
        "status": "ok",
        "version": "0.1.0",
        "message": "Servidor activo y funcionando"
    }


app.include_router(api_router, prefix="/api/v1")
