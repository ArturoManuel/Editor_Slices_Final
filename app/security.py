from fastapi import HTTPException, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

# Crear una instancia de HTTPBearer para manejar la autenticación
bearer_scheme = HTTPBearer()

# Definir un token fijo (puedes cambiarlo a uno más seguro o usar un sistema dinámico)
FIXED_BEARER_TOKEN = "B4gL8nP2Ys9WuR6TkHp3QcJrI7ZmP5Wq"

# Dependencia que valida el token
def get_current_token(credentials: HTTPAuthorizationCredentials = Security(bearer_scheme)):
    if credentials.credentials != FIXED_BEARER_TOKEN:
        raise HTTPException(
            status_code=401, detail="Invalid or missing token"
        )
    return credentials.credentials