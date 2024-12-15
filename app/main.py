import logging
from fastapi import FastAPI, Request
from app.gestionar_vm.route import vm_router
from app.users_plantillas.route import users
from app.logs.route import logs

# Configuración de logging
LOG_FILE = "fastapi_app.log"  # Nombre del archivo de log
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE),  # Guardar logs en archivo
        logging.StreamHandler(),       # Mostrar logs en consola
    ],
)

# Obtener el logger para la app
logger = logging.getLogger("fastapi_app")

# Crear instancia de FastAPI
app = FastAPI()

# Middleware para registrar logs de solicitudes HTTP
@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"Incoming request: {request.method} {request.url}")
    response = await call_next(request)
    logger.info(f"Response status: {response.status_code}")
    return response

# Registrar logs al inicio de la aplicación
@app.on_event("startup")
async def startup_event():
    logger.info("FastAPI application is starting up")

# Registrar logs al apagar la aplicación
@app.on_event("shutdown")
async def shutdown_event():
    logger.info("FastAPI application is shutting down")

# Incluir los routers
app.include_router(vm_router)
app.include_router(users)
app.include_router(logs)


