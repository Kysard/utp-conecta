from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import autentificador, blogAPI, conexion, usuarioAPI

app = FastAPI()

# Configuración de CORS para desarrollo
# Ajusta esto según tus necesidades de producción
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Ajusta según tu frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Configuración de routers
app.include_router(
    autentificador.router,
    prefix="/api/auth",
    tags=["Autenticación"]
)

app.include_router(
    conexion.router,
    prefix="/api/conexion",
    tags=["Conexión a la base de datos"]
)

app.include_router(
    usuarioAPI.router,
    prefix="/api/usuario",
    tags=["Gestion de usuarios"]
)


app.include_router(
    blogAPI.router,
    prefix="/api/blog",
    tags=["Gestion de blogs"]
)


# Comando para ejecutar el servidor:
# uvicorn app.main:app --reload --port 8002

# Comando para ver la documentación interactiva:
# http://127.0.0.1:8002/docs
