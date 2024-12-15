
from fastapi import APIRouter,HTTPException
from fastapi.responses import StreamingResponse
from fastapi.responses import FileResponse
import os

logs = APIRouter()

# Ruta al archivo de logs
LOG_FILE_PATH = "/home/ubuntu/editor_slices/fastapi_app.log"

@logs.get("/download-logs", response_class=FileResponse)
async def download_logs():
    if not os.path.exists(LOG_FILE_PATH):
        raise HTTPException(status_code=404, detail="Log file not found")
    
    def iter_file(file_path: str):
        with open(file_path, "rb") as file:
            while chunk := file.read(1024 * 1024):  # Leer en bloques de 1 MB
                yield chunk
    
    return StreamingResponse(
        iter_file(LOG_FILE_PATH),
        media_type="text/plain",
        headers={"Content-Disposition": "attachment; filename=fastapi_logs.txt"}
    )