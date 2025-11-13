# Ruta Lince API (Backend)

API REST construida con FastAPI + SQLModel para el Dashboard de Ruta Lince.

Este README te guía para levantar el servicio en local (Windows), preparar la base de datos y probar los endpoints.

## Requisitos

- Python 3.13 (ver `pyproject.toml`)
- Git
- Opcional: [uv](https://github.com/astral-sh/uv) para un flujo más rápido, o bien `pip` clásico

## Configuración rápida (Windows)

1. Clona el repositorio

2. Crea una variable de entorno `.env` en la raíz del repo con la URL de la base de datos 
   - Por defecto se usará una base SQLite local en `ruta_lince_database.sqlite` en la raíz del repo.

3. Instala dependencias

Con uv (rápido, sin activar venv manualmente):
```cmd
uv venv
uv pip install -r requirements.txt
```

Con pip (activando venv):
```cmd
py -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

4. Inicializa la base de datos y datos de demo
Esta debe ser proporcionada por el equipo

5. Levanta el servidor

Con uv (recomendado):
```cmd
uv run uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

Con pip/venv activado:
```cmd
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

6. Prueba la API

- Salud rápida:
  - GET http://127.0.0.1:8000/
- Rutas bajo prefijo `/api`:
  - Login: POST http://127.0.0.1:8000/api/auth/login

Ejemplo de request (login):
```http
POST http://127.0.0.1:8000/api/auth/login
Content-Type: application/json

{
  "email": "demo@example.com",
  "contrasena": "123"
}
```
## Configuración de base de datos

- Por defecto: `DATABASE_URL_PRE=sqlite:///ruta_lince_database.sqlite`
- Otras opciones comunes:
  - SQLite en memoria (solo para pruebas rápidas): `sqlite:///:memory:`
  - PostgreSQL: `postgresql+psycopg2://usuario:password@localhost:5432/ruta_lince`

Asegúrate de instalar el driver correspondiente si cambias de motor (por ejemplo, `psycopg2-binary` para Postgres).

## Desarrollo

- Ejecutar en modo recarga:
```cmd
uv run uvicorn main:app --reload
```
- Estándares: Python 3.13, FastAPI, SQLModel. Linter/formatter no definidos; puedes proponer `ruff`/`black`.
