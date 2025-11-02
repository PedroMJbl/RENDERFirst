from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from pydantic import BaseModel
from typing import Optional
from starlette.concurrency import run_in_threadpool 

# Importamos la función de búsqueda para el login (es síncrona)
from routers.users_db import search_user_for_login
from utils.jwt_tools import SECRET_KEY, ALGORITHM

# --- Esquema de Pydantic para el Payload (Contenido) del Token ---
# El token solo contiene el 'sub' (username)
class TokenData(BaseModel):
    username: Optional[str] = None

# --- Esquema de Seguridad para FastAPI/Swagger ---
# Le dice a Swagger que la API usa un token Bearer
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


# --- FUNCIÓN DEPENDENCY: Obtener Usuario Actual a partir del Token ---
async def get_current_user(token: str = Depends(oauth2_scheme)):
    """
    Función de dependencia que decodifica el token JWT y verifica al usuario en la DB.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudieron validar las credenciales",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        # 1. Decodificar el Token
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        
        if username is None:
            raise credentials_exception
        
        token_data = TokenData(username=username)

    except JWTError:
        # Esto ocurre si el token es inválido, ha expirado, o la firma no coincide
        raise credentials_exception
    
    # 2. Buscar al Usuario en la DB (usamos run_in_threadpool)
    # Buscamos el documento completo del usuario por su nombre de usuario
    user_doc = await run_in_threadpool(search_user_for_login, "username", token_data.username)

    if user_doc is None:
        # El usuario existe en el token, pero no en la DB (e.g., fue borrado)
        raise credentials_exception
    
    # 3. Retornar el documento del usuario
    # No devolvemos el objeto Pydantic UserDB, sino el dict de MongoDB, que es suficiente
    return user_doc
