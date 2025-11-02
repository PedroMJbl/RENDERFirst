from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt

# --- Configuración de JWT ---

# Es fundamental usar una clave secreta fuerte y única. 
# En producción, esto debe cargarse desde una variable de entorno.
SECRET_KEY = "tu-clave-secreta-super-segura" 
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30 # El token expirará después de 30 minutos

# --- Funciones de Creación y Verificación de Tokens ---

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """
    Crea un token JWT de acceso.
    
    Args:
        data: El payload que se incluirá en el token (ejemplo: {"sub": "username"}).
        expires_delta: Objeto timedelta para definir el tiempo de expiración. 
                       Si es None, usa el valor por defecto.
    
    Returns:
        Un string que representa el token JWT codificado.
    """
    to_encode = data.copy()
    
    # Manejo de la expiración (exp)
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    
    # Codificamos el token
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    
    return encoded_jwt
    
# NOTA: La función para verificar el token (decode_access_token) se añadirá más adelante
# cuando implementemos la dependencia para proteger rutas.
