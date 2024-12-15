import logging
from logging.handlers import RotatingFileHandler

# Configuración básica de logging
LOG_FILE = "fastapi_app.log"  # Archivo donde se guardarán los logs
LOG_LEVEL = logging.INFO      # Nivel de los logs

# Configuración de un manejador para escribir en un archivo
file_handler = RotatingFileHandler(
    LOG_FILE, maxBytes=5 * 1024 * 1024, backupCount=5  # Máximo 5 MB por archivo, 5 copias de respaldo
)
file_handler.setLevel(LOG_LEVEL)
file_handler.setFormatter(
    logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
)

# Configuración de logging global
logging.basicConfig(
    level=LOG_LEVEL,
    handlers=[file_handler, logging.StreamHandler()]  # También log en la consola
)

# Logger para FastAPI
logger = logging.getLogger("fastapi_app")
