                                       # 17/08/2025 9:01 Acabo #
                                  # domingo, 17 de agosto de 2025 17:53 Empiezo la  hora #
                                       # 17/08/2025 19:32 Acabo la hora #
                                  # lunes, 18 de agosto de 2025 08:26 Empiezo la hora #
'''
from fastapi import APIRouter,Depends,HTTPException,status

import secrets

from pydantic import BaseModel

from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm

from jose import jwt, JWTError

from passlib.context import CryptContext

from datetime import datetime, timedelta, timezone

ALGORITHM='HS256'
ACCESS_TOKEN_DURATION=1
SECRET = 'db31ba7985a2c51ba9126df828f4d15656b9530a429207e9f1267116adf35dd0'



router = APIRouter()

oauth2=OAuth2PasswordBearer(tokenUrl='login')

crypt = CryptContext(schemes=['bcrypt'])

class User(BaseModel):
    
    username: str
    full_name: str
    mail: str
    disabled: bool

class UserDB(User):
    password: str


users_db={
        'mouredev':{
            'username': 'mouredev',
            'full_name': 'Brais Moure',  
            'mail': 'BraisMoure@mouredev.com',
            'disabled': False,
            'password': '$2a$12$jmfNuQHaI72RB2uUmaQc..809ASXByS6yfVYMIqs5HM1oJRtiY/va'},
            
        'mouredev2':{
            'username': 'mouredev2',
            'full_name': 'Brais Moure2',  
            'mail': 'BraisMoure@mouredev2.com',
            'disabled': True,
            'password': '$2a$12$4ne.JBCTosloayadJbrLuehMN2WdqOaU6/HoYwNmww/WGZmY8/G3.'}
    }

                                              # 18/08/2025 9:47 Acabo la hora #
                                              # lunes, 18 de agosto de 2025 19:38 Empiezo la hora #

def search_user_db(username:str):
    if username in users_db:
        return UserDB(**users_db[username])                                              

@router.post('/login')
async def login (form:OAuth2PasswordRequestForm=Depends()):
    user_db=users_db.get(form.username)
    if not user_db:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='El usuario no es correcto')
    
    user=search_user_db(form.username)

    if not crypt.verify(form.password,user.password):
    
        raise HTTPException(status_code=400, detail='La contraseña no es correcta')
    
    # access_token_expiration=timedelta(minutes=ACCESS_TOKEN_DURATION)
    # expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_DURATION)
    
    #access_token = {'sub':user.username,
                    #'exp': datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_DURATION)}                    
    access_token = {'sub':user.username,
                    'exp': datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_DURATION)}        
    

    
    # return {'access_token':user.username,'token_type':'bearer'}
    # return {'access_token':access_token,'token_type':'bearer'}
    # return {'access_token':access_token,'token_type':'bearer'}
    # return {'access_token':jwt.encode(access_token,algorithm=ALGORITHM),'token_type':'bearer'}
    return {'access_token':jwt.encode(access_token,SECRET,algorithm=ALGORITHM),'token_type':'bearer'}
                                     # 18/08/2025 20:47 Acabo la hora #
                                     # martes, 19 de agosto de 2025 07:45 Empiezo la hora #

   # expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_DURATION)

                                     # 19/08/2025 8:50 Acabo #
                                     # martes, 19 de agosto de 2025 19:37 Empiezo #
                                     # 19/08/2025 20:59 Acabo la hora #
                                     # miércoles, 20 de agosto de 2025 07:27 Empiezo la hora #
                                     # 20/08/2025 8:41 Acabo la hora #
                                     # miércoles, 20 de agosto de 2025 19:51 Empiezo la hora #
                                     # 20/08/2025 20:31 Acabo #
                                     # jueves, 21 de agosto de 2025 08:39 Empiezo la hora #
                                     # 21/08/2025 10:09 Acabo #
                                     # viernes, 22 de agosto de 2025 19:20 Empiezo la hora #


def search_user(username:str):
    if username in users_db:
        return User(**users_db[username])
    
def search_user_db(username:str):
    if username in users_db:
        return UserDB(**users_db[username])

async def auth_user(token:str=Depends(oauth2)):

    Exception= HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                            detail='Credenciales de autenticación inválidas',
                            headers={'www-Authenticate':'Bearer'})

    try:        
       username=jwt.decode(token,SECRET,algorithms=[ALGORITHM]).get('sub')
       if username is None:
           raise Exception

       


    except JWTError:
        raise Exception  
    
    return search_user(username)
       



async def current_user(user:User=Depends(auth_user)):  
    
    if user.disabled:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, 
                            detail='Usuario inactivo')
    return user  

@router.get('/users/me')
async def me(user:User=Depends(current_user)):
    return user

                                       # 22/08/2025 20:51 Hasta aquí la hora #
                                       # sábado, 23 de agosto de 2025 06:22 Empiezo la hora #
                                       # domingo, 24 de agosto de 2025 07:36 Empiezo la hora #
'''

'''                                               
                                                ### AQUÍ ###

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from typing import Optional

# Importamos la conexión a MongoDB y el esquema de usuario que ya existe
# CORRECCIÓN: Ahora solo importamos las funciones que existen en users_db.py
from routers.users_db import search_user, user_schema
from db.client import users_collection 
from bson import ObjectId # Para manejar los IDs de MongoDB

# --- 1. Configuración del Token (Igual que el Profesor) ---

ALGORITHM = 'HS256'
ACCESS_TOKEN_DURATION = 1 # Duración del token en minutos (se recomienda más en producción)
# IMPORTANTE: Usamos la misma clave secreta, pero debería ser más larga y segura.
SECRET = 'db31ba7985a2c51ba9126df828f4d15656b9530a429207e9f1267116adf35dd0'

# --- 2. Herramientas de Seguridad ---

router = APIRouter(tags=["jwt-auth"])
oauth2 = OAuth2PasswordBearer(tokenUrl='login')
crypt = CryptContext(schemes=['bcrypt'])

# --- 3. Modelos (Simplificados para MongoDB) ---
# Usamos el modelo User que ya existe en users_db.py, pero lo re-declaramos para claridad
class User(BaseModel):
    id: Optional[str] = None
    username: str
    full_name: str
    mail: str
    disabled: bool = False

class UserDB(User):
    password: str

# --- 4. Funciones Auxiliares de Búsqueda para JWT ---

def search_user_db(username: str):
    """Busca un usuario en MongoDB y devuelve el objeto completo con la contraseña."""
    # En MongoDB, el username es el campo de búsqueda
    user_data = users_collection.find_one({"username": username})
    
    if user_data:
        # Convertimos el dict de MongoDB al modelo Pydantic UserDB
        return UserDB(**user_schema(user_data)) 
    return None

def get_user_from_db(username: str):
    """Busca un usuario en MongoDB y devuelve el objeto sin la contraseña."""
    # En MongoDB, el username es el campo de búsqueda
    user_data = users_collection.find_one({"username": username})
    
    if user_data:
        # Convertimos el dict de MongoDB al modelo Pydantic User
        return User(**user_schema(user_data)) 
    return None

# --- 5. Ruta POST: Login y Emisión del Token (Adaptada) ---

@router.post('/login')
async def login(form: OAuth2PasswordRequestForm = Depends()):
    # 1. Buscar usuario por username en MongoDB
    user_db = search_user_db(form.username)
    
    if not user_db:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Nombre de usuario o contraseña incorrectos')
    
    # 2. Verificar la contraseña hasheada (Usamos crypt del profesor)
    if not crypt.verify(form.password, user_db.password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Nombre de usuario o contraseña incorrectos')

    # 3. Crear el token JWT (Lógica del profesor)
    access_token = {
        'sub': user_db.username,
        'exp': datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_DURATION)
    }

    return {'access_token': jwt.encode(access_token, SECRET, algorithm=ALGORITHM), 'token_type': 'bearer'}

# --- 6. Funciones de Dependencia para Proteger Rutas (Adaptadas) ---

async def auth_user(token: str = Depends(oauth2)):
    exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                              detail='Credenciales de autenticación inválidas',
                              headers={'WWW-Authenticate': 'Bearer'})

    try:
        # Decodificar el token para obtener el username
        username = jwt.decode(token, SECRET, algorithms=[ALGORITHM]).get('sub')
        if username is None:
            raise exception
    except JWTError:
        raise exception
    
    # Buscar el usuario en MongoDB sin la contraseña
    user = get_user_from_db(username) 
    
    if user is None:
        raise exception
    
    return user

async def current_user(user: User = Depends(auth_user)):
    """Verifica si el usuario existe y no está deshabilitado."""
    if user.disabled:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, 
                            detail='Usuario inactivo')
    return user

# --- 7. Ruta de Prueba Protegida ---

@router.get('/users/me', response_model=User)
async def me(user: User = Depends(current_user)):
    """Devuelve la información del usuario autenticado."""
    return user
'''
'''
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import jwt, JWTError
from datetime import datetime, timedelta
from typing import Annotated
from pydantic import BaseModel # <-- ¡NUEVA IMPORTACIÓN!

from db.client import users_collection
from routers.users_db import search_user, user_schema
from passlib.context import CryptContext

# Configuración y Variables de Entorno (Reemplazar en producción)
ALGORITHM = "HS256"
ACCESS_TOKEN_DURATION = 15 # minutos
SECRET = "55e90d2345e0f11119b40742d458c0c8ed6697b416972750e50c487f5a31a98c"

# Definición del esquema OAuth2: Debe estar ANTES de current_user para que Depends lo encuentre.
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="jwt/login") 

# Router y Contexto de Hash
router = APIRouter(tags=["JWT Auth"]) 
crypt = CryptContext(schemes=["bcrypt"]) # Define el esquema de hashing

# Modelo de Token (¡AHORA HEREDA DE BASEMODEL!)
class Token(BaseModel):
    access_token: str
    token_type: str

# ----------------- Funciones Auxiliares -----------------

def authenticate_user(username: str, password: str):
    """
    Busca al usuario en MongoDB y verifica la contraseña.
    """
    # 1. Buscar usuario por username en la DB
    # CORRECCIÓN: Ahora pasamos el campo "username" explícitamente.
    user = search_user("username", username)
    
    if not user:
        # FastAPI exige que el retorno sea un diccionario o None/False para continuar
        return None 

    # 2. Verificar la contraseña con el hash guardado
    # El password recibido es texto plano. El password guardado en la DB es hasheado.
    if not crypt.verify(password, user['password']):
        return False
        
    # Si la verificación es exitosa, devuelve el usuario (diccionario)
    return user

def create_access_token(user: dict):
    """
    Crea el payload y genera el token JWT.
    """
    to_encode = {"sub": user['username'], "user_id": str(user['_id'])}
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_DURATION)
    to_encode.update({"exp": expire})
    
    encoded_jwt = jwt.encode(to_encode, SECRET, algorithm=ALGORITHM)
    return encoded_jwt

# current_user usa el esquema definido ANTES.
async def current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    """
    Verifica el token y devuelve el usuario autenticado.
    """
    exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Credenciales de autenticación inválidas",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        # 1. Decodificar el token
        payload = jwt.decode(token, SECRET, algorithms=[ALGORITHM])
        
        username: str = payload.get("sub")
        
        if username is None:
            raise exception
            
        # 2. Buscar al usuario por username (campo 'sub')
        # CORRECCIÓN: Ahora pasamos el campo "username" explícitamente.
        user = search_user("username", username)
        
        if user is None:
            raise exception
            
    except JWTError:
        raise exception
    
    # Devuelve el usuario como diccionario
    return user

# ----------------- Endpoints (Rutas) -----------------

@router.post("/jwt/login", status_code=status.HTTP_200_OK, response_model=Token)
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    """
    Endpoint para obtener el token de acceso.
    
    Requiere username y password (Form Data).
    """
    user = authenticate_user(form_data.username, form_data.password)
    
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )
    
    if user is False:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Contraseña incorrecta"
        )
    
    # Crear el token
    access_token = create_access_token(user)
    
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/jwt/users/me", response_model=user_schema)
async def me(user: Annotated[dict, Depends(current_user)]):
    """
    Endpoint para obtener los datos del usuario autenticado (ruta protegida).
    """
    # El decorador Depends(current_user) ya se encargó de la autenticación.
    # user contiene el diccionario del usuario de la DB.
    return user_schema(user)

# router.oauth2_scheme ya no es necesario aquí.
'''
                                                 # Aquí # Modificación para JWT
                                                            ## AQUÍ ##   

'''
from datetime import datetime, timedelta
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
from pydantic import BaseModel  # <--- IMPORTACIÓN AÑADIDA

# Importamos las funciones de la base de datos de usuarios
# Necesitamos: search_user y verify_password
from routers.users_db import search_user, UserDB, verify_password 

# --- Configuración de Seguridad ---

# Define la URL a donde se enviarán las credenciales (si no se usa Swagger)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="jwt/login")

# Clave secreta para firmar los tokens (¡CAMBIAR EN PRODUCCIÓN!)
SECRET_KEY = "tu_clave_secreta_aqui"
ALGORITHM = "HS256"


# --- Esquemas Pydantic para JWT ---

# CORRECCIÓN: El modelo Token ya NO hereda de UserDB. 
# Solo contendrá el token, que es lo que el endpoint de login devuelve.
class Token(BaseModel):
    """Modelo para la respuesta de un token (solo acceso y tipo)."""
    access_token: str
    token_type: str = "bearer"


# --- Funciones Auxiliares ---

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Crea el token de acceso con la información del usuario y el tiempo de expiración."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        # El token expira en 60 minutos para pruebas
        expire = datetime.utcnow() + timedelta(minutes=60)
    
    to_encode.update({"exp": expire})
    
    # Firma el token con la clave secreta y el algoritmo
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def authenticate_user(username: str, password: str) -> Optional[UserDB]:
    """
    Autentica al usuario buscando en la base de datos y verificando la contraseña.
    
    Args:
        username (str): Nombre de usuario introducido.
        password (str): Contraseña plana introducida.
        
    Returns:
        Optional[UserDB]: Objeto del usuario si la autenticación es exitosa, None en caso contrario.
    """
    # 1. Buscar usuario por username en MongoDB
    user_in_db = search_user("username", username)
    
    # 2. Si no se encuentra el usuario
    if not user_in_db:
        return None
        
    # 3. Verificar la contraseña
    if not verify_password(password, user_in_db.password):
        return None
        
    # 4. Si es exitoso, devolver el objeto UserDB
    return user_in_db


# --- Inicialización del Router ---
router = APIRouter(prefix="/jwt", tags=["JWT Auth"])


# --- Endpoint Principal de Login ---

@router.post("/login", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Endpoint para obtener el token de acceso (utiliza Form Data para Swagger).
    """
    # 1. Autenticar el usuario
    user = authenticate_user(form_data.username, form_data.password)
    
    # 2. Manejo de credenciales inválidas
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales inválidas",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
    # 3. Creación del Token
    # Incluimos solo datos no sensibles necesarios para el token (sub: subject)
    access_token_expires = timedelta(minutes=60) # Token más largo para pruebas
    access_token = create_access_token(
        data={"sub": user.username, "user_id": user.id}, 
        expires_delta=access_token_expires
    )
    
    # 4. Devolver el token. El retorno coincide con el nuevo modelo Token.
    return {"access_token": access_token, "token_type": "bearer"}


# --- Endpoint de Ejemplo Protegido por JWT ---

# La función 'get_current_user' está en el Canvas completo, pero la omito aquí 
# para enfocarnos en el login. Si la necesitas, dímelo.
# @router.get("/users/me/", response_model=UserDB)
# async def read_users_me(current_user: UserDB = Depends(get_current_user)):
#     return current_user
'''

'''
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from datetime import datetime, timedelta
from typing import Optional
from pydantic import BaseModel # <-- IMPORTACIÓN CORREGIDA AÑADIDA AQUÍ

# Importaciones de Modelos y Helpers
from db.models.user import UserDB
# Importación corregida: Rompemos la dependencia circular importando directo del helper
from db.db_helpers import search_user_for_login 

# --- Configuración de Seguridad ---

# Configuración del token (debe ser una variable de entorno en producción)
SECRET_KEY = "tu_super_clave_secreta_jwt"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30 # Token expira en 30 minutos

# Esquema de seguridad: Indica a FastAPI que esperaremos un token OAuth2
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

# --- Modelos de Token (Para Pydantic) ---

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

# --- Funciones Auxiliares JWT ---

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Crea el token JWT con tiempo de expiración."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    # 'sub' (subject) es una convención para el identificador principal (aquí usamos username)
    to_encode.update({"sub": data["username"]}) 
    
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme)):
    """Decodifica y valida el token JWT para obtener el usuario actual."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudieron validar las credenciales",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        # Decodificar el token para obtener los datos
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        
        if username is None:
            raise credentials_exception
        
        token_data = TokenData(username=username)
    
    except JWTError:
        # Si el token no es válido o está expirado
        raise credentials_exception
    
    # Buscar al usuario en la base de datos (usando la función del helper)
    user = search_user_for_login(token_data.username)
    
    if user is None:
        raise credentials_exception
        
    return user

# --- Inicialización del Router ---

router = APIRouter(prefix="/auth", tags=["auth"])

# --- Endpoint de Login (Genera el Token) ---

@router.post("/login", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Verifica las credenciales y genera un token JWT.
    OAuth2PasswordRequestForm espera 'username' y 'password'.
    """
    
    # 1. Buscar usuario por username (usando la función del helper)
    user = search_user_for_login(form_data.username)

    # 2. Verificar si el usuario existe y si la contraseña es correcta (AQUÍ DEBE USARSE HASH)
    # NOTA: Por ahora, solo comparamos el texto plano para simplificar la prueba de JWT.
    # En la siguiente fase, implementaremos el hashing de contraseñas.
    if not user or user.password != form_data.password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # 3. Crear el token de acceso
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"username": user.username}, expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}

# --- Endpoint Protegido (Test) ---

@router.get("/me", response_model=UserDB)
async def read_users_me(current_user: UserDB = Depends(get_current_user)):
    """
    Endpoint de prueba protegido por JWT. Devuelve los datos del usuario autenticado.
    """
    return current_user
'''
'''
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from datetime import datetime, timedelta
from typing import Optional
from pydantic import BaseModel 

# Importaciones de Modelos y Helpers
from db.models.user import UserDB
# Importación corregida: Rompemos la dependencia circular importando directo del helper
from db.db_helpers import search_user_for_login 
# NUEVA IMPORTACIÓN DE SEGURIDAD
from utils.security import verify_password 

# --- Configuración de Seguridad ---

# Configuración del token (debe ser una variable de entorno en producción)
SECRET_KEY = "tu_super_clave_secreta_jwt"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30 # Token expira en 30 minutos

# Esquema de seguridad: Indica a FastAPI que esperaremos un token OAuth2
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

# --- Modelos de Token (Para Pydantic) ---

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

# --- Funciones Auxiliares JWT ---

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Crea el token JWT con tiempo de expiración."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    # 'sub' (subject) es una convención para el identificador principal (aquí usamos username)
    to_encode.update({"sub": data["username"]}) 
    
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme)):
    """Decodifica y valida el token JWT para obtener el usuario actual."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudieron validar las credenciales",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        # Decodificar el token para obtener los datos
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        
        if username is None:
            raise credentials_exception
        
        token_data = TokenData(username=username)
    
    except JWTError:
        # Si el token no es válido o está expirado
        raise credentials_exception
    
    # Buscar al usuario en la base de datos (usando la función del helper)
    # CORRECCIÓN DE LA FUNCIÓN search_user_for_login
    user = search_user_for_login("username", token_data.username)
    
    if user is None:
        raise credentials_exception
        
    return user

# --- Inicialización del Router ---

router = APIRouter(prefix="/auth", tags=["auth"])

# --- Endpoint de Login (Genera el Token) ---

@router.post("/login", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Verifica las credenciales y genera un token JWT.
    OAuth2PasswordRequestForm espera 'username' y 'password'.
    """
    
    # 1. Buscar usuario por username (usando la función del helper)
    # CORRECCIÓN CLAVE: Pasamos el campo "username" y el valor form_data.username
    user = search_user_for_login("username", form_data.username)

    # 2. Verificar existencia del usuario (EVITA EL ERROR 500)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # 3. Verificar la contraseña hasheada (VERIFICACIÓN SEGURA)
    # CLAVE: La función verify_password compara el texto plano (form_data.password) 
    # con el hash (user.password) almacenado en la DB.
    if not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # 4. Crear el token de acceso
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"username": user.username}, expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}

# --- Endpoint Protegido (Test) ---

@router.get("/me", response_model=UserDB)
async def read_users_me(current_user: UserDB = Depends(get_current_user)):
    """
    Endpoint de prueba protegido por JWT. Devuelve los datos del usuario autenticado.
    """
    return current_user
'''
'''       # DESDE AQUÍ
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from datetime import datetime, timedelta
from typing import Optional
from pydantic import BaseModel 

# Importaciones de Modelos y Helpers
from db.models.user import UserDB
# Importación corregida: Rompemos la dependencia circular importando directo del helper
from db.db_helpers import search_user_for_login 
# IMPORTACIÓN CLAVE DE SEGURIDAD
from utils.security import verify_password 

# --- Configuración de Seguridad ---

# Configuración del token (debe ser una variable de entorno en producción)
SECRET_KEY = "tu_super_clave_secreta_jwt"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30 # Token expira en 30 minutos

# Esquema de seguridad: Indica a FastAPI que esperaremos un token OAuth2
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

# --- Modelos de Token (Para Pydantic) ---

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

# --- Funciones Auxiliares JWT ---

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Crea el token JWT con tiempo de expiración."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    # 'sub' (subject) es una convención para el identificador principal (aquí usamos username)
    to_encode.update({"sub": data["username"]}) 
    
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme)):
    """Decodifica y valida el token JWT para obtener el usuario actual."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudieron validar las credenciales",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        # Decodificar el token para obtener los datos
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        
        if username is None:
            raise credentials_exception
        
        token_data = TokenData(username=username)
    
    except JWTError:
        # Si el token no es válido o está expirado
        raise credentials_exception
    
    # Buscar al usuario en la base de datos 
    # CLAVE: Pasamos el campo "username" para que el helper sepa dónde buscar.
    user = search_user_for_login("username", token_data.username)
    
    if user is None:
        raise credentials_exception
        
    return user

# --- Inicialización del Router ---

router = APIRouter(prefix="/auth", tags=["auth"])

# --- Endpoint de Login (Genera el Token) ---

@router.post("/login", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Verifica las credenciales y genera un token JWT.
    OAuth2PasswordRequestForm espera 'username' y 'password'.
    """
    
    # 1. Buscar usuario por username
    # CLAVE: Pasamos el campo "username" y el valor form_data.username
    user = search_user_for_login("username", form_data.username)

    # 2. Verificar existencia del usuario (EVITA EL ERROR 500)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # 3. Verificar la contraseña hasheada (VERIFICACIÓN SEGURA)
    # CLAVE: La función verify_password compara el texto plano (form_data.password) 
    # con el hash (user.password) almacenado en la DB.
    if not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # 4. Crear el token de acceso
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"username": user.username}, expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}

# --- Endpoint Protegido (Test) ---

@router.get("/me", response_model=UserDB)
async def read_users_me(current_user: UserDB = Depends(get_current_user)):
    """
    Endpoint de prueba protegido por JWT. Devuelve los datos del usuario autenticado.
    """
    return current_user
                               # HASTA AQUÍ
'''

                 
'''
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta

# Importamos las funciones de seguridad (hashing y verificación)
from utils.security import verify_password
# Importamos la función de búsqueda (search_user_for_login) que ahora está en users_db
from routers.users_db import search_user_for_login

# Importamos las herramientas de JWT
from utils.jwt_tools import create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES

# --- Router y Esquema de Autenticación ---

router = APIRouter(prefix="/auth", tags=["auth"], responses={
    status.HTTP_401_UNAUTHORIZED: {"description": "Credenciales inválidas"}
})

# --- Función Auxiliar: Autenticar Usuario ---

def authenticate_user(username: str, password: str):
    """
    Busca al usuario por nombre de usuario y verifica su contraseña.
    Devuelve el documento del usuario (dict) si la autenticación es exitosa.
    """
    # 1. Buscar el usuario en la base de datos por el campo "username"
    user_doc = search_user_for_login("username", username)
    
    # 2. Si el usuario no existe O la contraseña hasheada no está disponible
    if not user_doc or "password" not in user_doc:
        return None # Usuario no encontrado o sin contraseña hasheada

    # 3. Verificar la contraseña
    # user_doc["password"] es la contraseña hasheada de la DB
    if not verify_password(password, user_doc["password"]):
        return None # Contraseña incorrecta

    # 4. Éxito: Devolvemos el documento del usuario de la DB
    return user_doc

# --- Endpoint de Login JWT ---

@router.post("/login", tags=["auth"])
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Endpoint para iniciar sesión y obtener un token JWT.
    Requiere username y password en formato x-www-form-urlencoded.
    """
    # Intentamos autenticar al usuario
    user = authenticate_user(form_data.username, form_data.password)

    # Si la autenticación falla (el usuario es None)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Si la autenticación es exitosa, creamos el token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    # El token lleva el 'username' como payload
    access_token = create_access_token(
        data={"sub": user["username"]}, expires_delta=access_token_expires
    )
    
    # Devolvemos el token
    return {"access_token": access_token, "token_type": "bearer"}
'''

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from typing import Optional
# Importamos la herramienta para ejecutar funciones síncronas sin bloquear el servidor
from starlette.concurrency import run_in_threadpool 

# Importamos las funciones de seguridad (hashing y verificación)
from utils.security import verify_password
# IMPORTANTE: Importamos la función de búsqueda desde el router de MongoDB
from routers.users_db import search_user_for_login
# 09/11/2025
from .users import User # <-- ¡CORRECTO!
# Importar la dependencia de JWT desde 'deps.py' (está en la misma carpeta)
from .deps import get_current_user

# Importamos las herramientas de JWT (requiere 'python-jose')
from utils.jwt_tools import create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES
# --- Router y Esquema de Autenticación ---


router = APIRouter(prefix="/auth", tags=["auth"], responses={
    status.HTTP_401_UNAUTHORIZED: {"description": "Credenciales inválidas"}
})

# --- Función Auxiliar: Autenticar Usuario (SIN async) ---
# Debe ser síncrona para que run_in_threadpool la pueda ejecutar
def authenticate_user(username: str, password: str) -> Optional[dict]:
    """
    Busca al usuario por nombre de usuario y verifica su contraseña.
    Esta función es SÍNCRONA e intensiva en CPU (por verify_password).
    """
    # 1. Buscar el usuario en la base de datos por el campo "username"
    # Esta función (search_user_for_login) hace una llamada de I/O síncrona (pymongo)
    user_doc = search_user_for_login("username", username)
    
    # 2. Si el usuario no existe O la contraseña hasheada no está disponible
    if not user_doc or "password" not in user_doc:
        return None # Usuario no encontrado o sin contraseña hasheada

    # 3. Verificar la contraseña (BLOQUEANTE/CPU INTENSIVO)
    # user_doc["password"] es la contraseña hasheada de la DB
    if not verify_password(password, user_doc["password"]):
        return None # Contraseña incorrecta

    # 4. Éxito: Devolvemos el documento del usuario de la DB
    return user_doc

#@router.get('/users/me')
@router.get('/me')
async def me(user: User = Depends(get_current_user)):
    return user

# --- Endpoint de Login JWT ---

@router.post("/login", tags=["auth"])
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Endpoint para iniciar sesión y obtener un token JWT.
    Requiere username y password en formato x-www-form-urlencoded.
    """
    # ---------------------------
    # CORRECCIÓN CLAVE: Ejecutamos la función de autenticación (que es bloqueante) 
    # en un thread de fondo para no congelar el servidor.
    # ---------------------------
    
    user = await run_in_threadpool(authenticate_user, form_data.username, form_data.password)

    # Si la autenticación falla (el usuario es None)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Si la autenticación es exitosa, creamos el token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    # El token lleva el 'username' como payload
    access_token = create_access_token(
        data={"sub": user["username"]}, expires_delta=access_token_expires
    )
    
    # Devolvemos el token
    return {"access_token": access_token, "token_type": "bearer"}




                                         
                                         


