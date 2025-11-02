'''
from fastapi import APIRouter, HTTPException, status
from db.models.user import User
#from ..db.models.user import User # Modificado por Gemini # miércoles, 1 de octubre de 2025 06:13 
from db.schemas.user import user_schema
from db.client import db_client
from bson import ObjectId

# --- CONFIGURACIÓN DEL ROUTER ---
#router = APIRouter(prefix="/usersdb"  # Moure
router = APIRouter(prefix="/userdb",   #Gemini
                   #tags=["users_db"]  # Moure
                   tags=["user_db"],  # Gemini
                   responses={status.HTTP_404_NOT_FOUND: {"message": "No encontrado"}})

# --- FUNCIÓN DE BÚSQUEDA DE ID (AUXILIAR) ---

# Función auxiliar para buscar por el _id de MongoDB (que es un ObjectId)
def search_user_by_id(id: str):
    try:
        # Busca el documento en la colección 'users'
        user = db_client.local.users.find_one({"_id": ObjectId(id)})
        if user:
            # Si lo encuentra, lo pasa por el esquema para limpiarlo y devolverlo
            return user_schema(user)
    except:
        return None
'''
# --- ENDPOINTS (RUTAS) ---
'''
@router.get("/", response_model=list[User])
async def users():
    """Obtiene todos los usuarios de la base de datos."""
    return user_schema(db_client.local.users.find())   # corregido de 'users_schema' a 'user_schema'
'''
'''
@router.get("/")          # GET 1 Código propuesto por Gemini   
async def users():
    """Obtiene todos los usuarios de la base de datos."""
    users_list = user_schema(db_client.local.users.find())
    
    # 🟢 Aquí limpiamos la lista: iteramos y forzamos el model_dump en cada usuario
    cleaned_list = [
        User(**user).model_dump(exclude_none=True) for user in users_list
    ]
    
    return cleaned_list

@router.get("/{id}")#, response_model=User) # GET 2 Se usa el id de MongoDB (ObjectId) # Eliminado per Gemnini miércoles, 1 de octubre de 2025
async def user(id: str):
    """Busca y obtiene un usuario por su ID de MongoDB."""
    user = search_user_by_id(id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No se ha encontrado el usuario")
    #return user
    return User(**user).model_dump(exclude_none=True) # A propuesta de Gemnini miércoles, 1 de octubre de 2025
'''
'''                                   Moure
@router.post("/", response_model=User, status_code=status.HTTP_201_CREATED)
async def create_user(user: User):
    """Crea un nuevo usuario en la base de datos."""
    user_dict = dict(user)
    
    # 1. Eliminar el ID para que MongoDB genere uno nuevo (_id)
    del user_dict["id"]
    
    # 2. Insertar el documento y obtener el ID generado
    try:
        result = db_client.local.users.insert_one(user_dict)
    except Exception as e:
        # Puede haber errores de unicidad si usa índices
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Error al crear usuario: {e}")

    # 3. Recuperar el usuario con el ID generado para devolver el objeto User completo
    new_user = search_user_by_id(result.inserted_id)

    return User(**new_user)
'''

                                    # Gemini #
'''
# users_db.py (Asegúrate de importar 'router' de APIRouter y la función 'user_schema')
from fastapi import APIRouter, status
from db.models.user import User # El modelo Pydantic
from db.schemas.user import user_schema # El serializador de MongoDB
from db.client import db_client # El cliente de MongoDB

router = APIRouter(prefix="/userdb", 
                   tags=["users_db"],
                   responses={status.HTTP_404_NOT_FOUND: {"message": "No encontrado"}}) # ⬅️ ¡Aquí se corrigió el prefijo!
'''

'''
@router.post('/', response_model=User, status_code=status.HTTP_201_CREATED)
async def user(user: User):

    user_dict = dict(user)
    
    # 🛑 El paso clave: elimina el ID que vino en la petición.
    del user_dict['id']
    
    # Inserta el documento (MongoDB genera el _id)
    id = db_client.local.users.insert_one(user_dict).inserted_id

    # Busca el documento recién creado para obtener el _id generado
    new_user = user_schema(db_client.local.users.find_one({"_id": id}))
    
    # Devuelve el objeto ya serializado al modelo Pydantic
    return User(**new_user)
'''                           
'''                              # Gemini 1? #
@router.post('/', response_model=User, status_code=status.HTTP_201_CREATED)
async def user(user: User):

    user_dict = dict(user)

    print("DICCIONARIO ANTES DE ELIMINAR ID:", user_dict) # ⬅️ AÑADE ESTA LÍNEA
    
    # 🛑 El paso clave: elimina el ID que vino en la petición.
    del user_dict['id']

    print("DICCIONARIO ANTES DE INSERTAR:", user_dict) # ⬅️ AÑADE ESTA LÍNEA
    
    # Inserta el documento (MongoDB genera el _id)
    id = db_client.local.users.insert_one(user_dict).inserted_id

    # Busca el documento recién creado para obtener el _id generado
    new_user = user_schema(db_client.local.users.find_one({"_id": id}))
    
    # Devuelve el objeto ya serializado al modelo Pydantic
    return User(**new_user)
'''

                             # Gemini 2? #

# Archivo: routers/users_db.py

#@router.post('/',response_model=User,status_code=status.HTTP_201_CREATED)
'''
@router.post('/',status_code=status.HTTP_201_CREATED)
async def user(user:User):

    # 🛑 Cambiamos a .model_dump() (o .dict() en Pydantic v1) 
    # para una conversión más limpia.
    #user_dict = user.model_dump() Comentado por Gemini jueves, 2 de octubre de 2025
    user_dict = user.model_dump(exclude_none=True)

    # ⚠️ CAMBIO CLAVE: Usamos .pop() para eliminar 'id' de forma segura si existe
    user_dict.pop('id', None) # Elimina 'id' y devuelve None si no lo encuentra (no falla)
    
    # Mantenemos el resto del código del profesor
    id = db_client.local.users.insert_one(user_dict).inserted_id

    new_user = user_schema(db_client.local.users.find_one({"_id":id}))
    
    return User(**new_user).model_dump(exclude_none=True)
'''
'''
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from typing import Optional, List
from bson import ObjectId
#from db.schemas.client import db_client
from db.client import db_client
users_collection = db_client.users.users
#from db.client import users_collection # Importamos la colección de MongoDB
#from db.schemas.client import users_collection

# --- Esquema de Datos (Modelo Pydantic) ---

# Modelo base para la entrada de datos (no incluye el id)
class User(BaseModel):
    username: str
    email: str

# Modelo usado para devolver datos desde la base de datos (incluye el id)
class UserDB(User):
    id: Optional[str] = None # El ID es opcional al crear, pero siempre estará al leer

# --- Funciones Auxiliares ---

# Transforma un documento de MongoDB (diccionario con _id: ObjectId) a un objeto UserDB
def user_schema(user) -> UserDB:
    # Convertimos el ObjectId de MongoDB a string para el campo 'id' de Pydantic
    return UserDB(
        id=str(user["_id"]),
        username=user["username"],
        email=user["email"]
    )

# Busca un usuario en la DB por cualquier campo
def search_user(field: str, key: any):
    try:
        user = users_collection.find_one({field: key})
        if user:
            # Si encuentra el usuario, lo convierte al esquema UserDB para devolverlo
            return user_schema(user)
    except:
        return None # Retorna None si hay un error o no se encuentra

# --- Inicialización del Router ---
#router = APIRouter(prefix="/user", tags=["users"])
# AHORA (Funciona en /userdb)
router = APIRouter(prefix="/userdb", tags=["users"])

# --- Ruta POST: Crear Usuario (con validación de unicidad) ---

@router.post("/", response_model=UserDB, status_code=status.HTTP_201_CREATED)
async def create_user(user: User):
    # 1. Validación de Unicidad: Buscar si el email ya existe
    existing_user = search_user("email", user.email)
    if existing_user:
        # Si el usuario existe, lanzamos un error 409 Conflict
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"El usuario con email {user.email} ya existe."
        )
    
    # Convertimos el modelo Pydantic a un diccionario para MongoDB
    user_dict = user.model_dump()
    
    try:
        # 2. Inserción en la base de datos (USANDO users_collection)
        result = users_collection.insert_one(user_dict)
    except Exception as e:
        # Manejo de error de la base de datos si ocurre un problema de inserción
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error interno al insertar en la base de datos.")

    # 3. Recuperar el usuario recién insertado para obtener el ID
    new_user = users_collection.find_one({"_id": result.inserted_id})
    
    # 4. Devolver el usuario con el ID de MongoDB
    return user_schema(new_user)

# --- Próxima Ruta: GET (Lectura) ---
# ... (Aquí irá la lógica GET en el siguiente paso)
'''
'''

                                                      # Aquí 
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from typing import Optional, List
from bson import ObjectId
# Importación corregida para tu estructura de archivos:
from db.client import db_client 
# Inicializamos la colección (db_client.nombre_db.nombre_coleccion)
users_collection = db_client.users.users

# --- Esquema de Datos (Modelo Pydantic) ---

# Usa 'username' para que coincida con tu envío JSON.
class User(BaseModel):
    username: str
    email: str


class User(BaseModel):   # Cambiado código para JWT
    username: str
    email: str
    password: str  # <--- Este es el cambio clave

# Modelo usado para devolver datos desde la base de datos (incluye el id)
class UserDB(User):
    id: Optional[str] = None # El ID es opcional al crear, pero siempre estará al leer

# --- Funciones Auxiliares ---

# Transforma un documento de MongoDB (diccionario con _id: ObjectId) a un objeto Pydantic UserDB
def user_schema(user) -> UserDB:
    # CLAVE CORREGIDA: Usamos 'username'
    return UserDB(
        id=str(user["_id"]),
        username=user["username"], 
        email=user["email"]
    )

# Transforma una lista de documentos de MongoDB a una lista de objetos Pydantic UserDB
def users_schema(users) -> List[UserDB]:
    return [user_schema(user) for user in users]

# Busca un usuario en la DB por cualquier campo
def search_user(field: str, key: any):
    try:
        # Busca el documento en MongoDB
        user = users_collection.find_one({field: key})
        if user:
            # Si encuentra el usuario, lo convierte al esquema UserDB para devolverlo
            return user_schema(user)
    except Exception as e:
        # Nota: Este error captura problemas de conexión si MongoDB falla
        print(f"Error al buscar usuario: {e}")
        return None 

# --- Inicialización del Router ---
# PREFIJO DEFINITIVO: La ruta base es '/userdb'
router = APIRouter(prefix="/userdb", tags=["users"])

# --- Ruta POST: Crear Usuario (con validación de unicidad) ---

@router.post("/", response_model=UserDB, status_code=status.HTTP_201_CREATED)
async def create_user(user: User):
    # 1. Validación de Unicidad: Buscar si el email ya existe
    existing_user = search_user("email", user.email)
    if existing_user:
        # Si el usuario existe, lanzamos un error 409 Conflict
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"El usuario con email {user.email} ya existe."
        )
    
    # Convertimos el modelo Pydantic a un diccionario para MongoDB
    # user_dict = user.model_dump(exclude_none=True)
    user_dict["password"] = crypt.hash(user_dict["password"])  # Cambiado código para JWT 
    
    try:
        # 2. Inserción en la base de datos (USANDO users_collection)
        result = users_collection.insert_one(user_dict)
    except Exception as e:
        # Manejo de error de la base de datos
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error interno al insertar: {e}")

    # 3. Recuperar el usuario recién insertado para obtener el ID y validar la salida
    new_user = users_collection.find_one({"_id": result.inserted_id})
    
    # 4. Devolver el usuario con el ID de MongoDB
    return user_schema(new_user)

# --- Ruta GET: Leer Todos los Usuarios ---
@router.get("/", response_model=List[UserDB])
async def get_all_users():
    # Usamos find() sin argumentos para obtener todos los documentos
    return users_schema(users_collection.find())

# --- Ruta GET: Leer por ID ---
@router.get("/{id}", response_model=UserDB)
async def get_user(id: str):
    # Intentamos buscar el usuario usando el ID convertido a ObjectId
    try:
        user = users_collection.find_one({"_id": ObjectId(id)})
        if user:
            return user_schema(user)
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado")
    except Exception:
        # Esto captura si el ID no es un formato válido de ObjectId
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Formato de ID inválido.")

# --- Ruta PUT: Actualizar Usuario ---
@router.put("/", response_model=UserDB)
async def update_user(user: UserDB):
    # 1. Búsqueda y Validación
    if not user.id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El ID del usuario es requerido para la actualización.")

    user_dict = user.model_dump(exclude_none=True)
    del user_dict["id"] # Eliminamos el campo ID antes de la actualización en MongoDB

    try:
        # Intentamos convertir el ID a ObjectId
        user_id = ObjectId(user.id)
    except:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Formato de ID inválido.")

    # 2. Actualización en la base de datos
    try:
        # Usamos $set para actualizar solo los campos provistos
        updated_result = users_collection.find_one_and_update(
            {"_id": user_id},
            {"$set": user_dict},
            return_document=True # Devuelve el documento después de la actualización
        )
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error interno al actualizar: {e}")

    # 3. Respuesta
    if updated_result:
        return user_schema(updated_result)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado para actualizar.")

# --- Ruta DELETE: Eliminar Usuario ---
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_user(id: str):
    try:
        # Intentamos convertir el ID a ObjectId
        user_id = ObjectId(id)
    except:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Formato de ID inválido.")
        
    # 2. Eliminación
    try:
        delete_result = users_collection.find_one_and_delete({"_id": user_id})
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error interno al eliminar: {e}")
        
    # 3. Respuesta
    if delete_result:
        # 204 No Content es la respuesta estándar para un DELETE exitoso
        return
    else:
        # Si no se encontró un usuario con ese ID para borrar
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado para eliminar.")
'''
                             # AQUÍ #
'''
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from typing import Optional, List
from passlib.context import CryptContext 
from bson import ObjectId

# Importamos la variable 'users_collection' directamente desde tu client.py
# Esto soluciona el problema de la colección no definida y el crash de Uvicorn.
try:
    from db.client import users_collection 
    # Aseguramos que la colección está lista, si no lo está se gestionará abajo
except ImportError:
    print("ERROR FATAL: No se pudo importar 'users_collection' de 'db.client'.")
    # Si la importación falla, users_collection se trata como None
    users_collection = None 


# --- Esquema de Datos (Modelo Pydantic) ---

# Contexto para hashear (codificar) y verificar contraseñas
password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# Modelo base para la entrada de datos (usado en POST/PUT)
class User(BaseModel):
    username: str
    email: str
    password: str 

# Modelo usado para devolver datos desde la base de datos (incluye el id y el password hasheado)
class UserDB(User):
    id: Optional[str] = None 


# --- Funciones Auxiliares (Esquemas y Búsqueda) ---

def user_schema(user) -> dict:
    """Transforma un objeto de MongoDB (con _id) a un diccionario estándar."""
    return {
        "id": str(user["_id"]),
        "username": user["username"],
        "email": user["email"],
        # Incluimos el hash del password
        "password": user["password"]
    }

def users_schema(users: list) -> list:
    """Transforma una lista de objetos de MongoDB a una lista de diccionarios."""
    return [user_schema(user) for user in users]

def search_user(field: str, key):
    """Busca un usuario por un campo dado (ej: email o username) y devuelve el objeto UserDB."""
    global users_collection
    
    if users_collection is None:
        return None
        
    try:
        # Busca el documento en la base de datos
        user_doc = users_collection.find_one({field: key})
        if user_doc:
            # Transforma el documento a un esquema (incluye el ID y hash) y luego a un objeto UserDB
            return UserDB(**user_schema(user_doc))
        return None
    except Exception as e:
        print(f"Error buscando usuario: {e}")
        return None


# --- Funciones de Hashing ---

def get_password_hash(password: str) -> str:
    """Hashea una contraseña para almacenamiento seguro."""
    return password_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifica si una contraseña plana coincide con el hash almacenado."""
    return password_context.verify(plain_password, hashed_password)

# --- Inicialización del Router ---
router = APIRouter(prefix="/userdb", tags=["MongoDB Users"])

# --- Ruta POST: Crear Usuario (con validación de unicidad y hashing) ---

@router.post("/", response_model=UserDB, status_code=status.HTTP_201_CREATED)
async def create_user(user: User):
    if users_collection is None:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Servicio de base de datos no disponible.")
        
    # 1. Validación: Comprobar si el usuario ya existe por email o username
    # Usamos user.username y user.email directamente, ya que el BaseModel está limpio
    if search_user("email", user.email) or search_user("username", user.username):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="El usuario o email ya está registrado.")
    
    # 2. Hashing: Codificar la contraseña
    hashed_password = get_password_hash(user.password)
    
    # 3. Preparar el nuevo usuario para la inserción
    new_user_dict = user.model_dump()
    new_user_dict["password"] = hashed_password # Reemplazar el password plano por el hash

    # 4. Inserción en MongoDB
    try:
        result = users_collection.insert_one(new_user_dict)
    except Exception as e:
        # Esto captura errores de conexión o de base de datos
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error al insertar en DB: {e}")

    # 5. Obtener y devolver el usuario creado con el ID
    new_user = users_collection.find_one({"_id": result.inserted_id})
    
    # Devolvemos el usuario
    return UserDB(**user_schema(new_user))
'''
'''
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field
from typing import List, Optional # <-- CORRECCIÓN: Añadida la importación de Optional
from passlib.context import CryptContext
from bson import ObjectId # Para manejar IDs de MongoDB

# Importamos el cliente de la base de datos
from db.client import db_client as client

# --- Configuración de Seguridad ---
# Contexto para hashing de contraseñas (utiliza bcrypt por defecto)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# --- Esquemas Pydantic ---

# 1. Modelo para recibir datos del usuario (password en texto plano para hashing)
class User(BaseModel):
    # Field(alias="_id") permite que Pydantic maneje _id de MongoDB
    id: Optional[str] = Field(alias="_id", default=None) 
    username: str
    email: str
    password: str # Se recibe en texto plano

# 2. Modelo para devolver datos del usuario (password hasheado)
class UserDB(BaseModel):
    # Permite el alias del campo interno "_id" de MongoDB
    id: Optional[str] = Field(alias="_id", default=None) 
    username: str
    email: str
    password: str # Se devuelve hasheado

    # Configuración para permitir la asignación de _id desde MongoDB
    class Config:
        populate_by_name = True
        json_encoders = {ObjectId: str}
        # Habilita la conversión de tipos (necesario para manejar el _id de MongoDB)
        arbitrary_types_allowed = True


# --- Funciones de Utilidad ---

def user_schema(user: UserDB) -> dict:
    """Transforma un objeto UserDB a un diccionario serializable."""
    return {
        "id": str(user.id),
        "username": user.username,
        "email": user.email,
        "password": user.password
    }

def users_schema(users: List[UserDB]) -> List[dict]:
    """Transforma una lista de objetos UserDB a una lista de diccionarios serializables."""
    return [user_schema(user) for user in users]

def search_user(field: str, key: str) -> Optional[UserDB]:
    """Busca un usuario por campo y clave. Retorna el objeto Pydantic UserDB."""
    try:
        # Accedemos a la colección 'users' dentro de la base de datos 'fastapi_db'
        user_dict = client.fastapi_db.users.find_one({field: key})
        if user_dict:
            # Reemplazamos el ObjectId por su string para Pydantic
            user_dict["_id"] = str(user_dict["_id"])
            return UserDB(**user_dict)
    except Exception as e:
        # En caso de error de conexión o base de datos
        print(f"Error al buscar en MongoDB: {e}")
        return None
    return None

def hash_password(password: str) -> str:
    """Hashea una contraseña."""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifica una contraseña hasheada."""
    return pwd_context.verify(plain_password, hashed_password)


# --- Inicialización del Router ---
router = APIRouter(tags=["MongoDB Users"])

# --- COLECCIÓN DE MONGODB ---
# Nota: La colección se llama 'users'
users_collection = client.fastapi_db.users


# --- ENDPOINTS ---

# Endpoint: POST /userdb/ (Crear un usuario)
@router.post("/", response_model=UserDB, status_code=status.HTTP_201_CREATED)
async def create_user(user: User):
    """
    Crea un nuevo usuario y lo inserta en la base de datos de MongoDB.
    """
    # 1. Validación de unicidad de username/email antes de hashear
    if search_user("username", user.username) is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="El nombre de usuario ya existe"
        )
    if search_user("email", user.email) is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="El email ya está registrado"
        )

    # 2. Hashear la contraseña
    hashed_password = hash_password(user.password)

    # 3. Preparar el diccionario para la inserción
    user_dict = user.model_dump(exclude_none=True)
    user_dict["password"] = hashed_password
    
    # Eliminamos el campo 'id' antes de insertar (MongoDB usa '_id')
    user_dict.pop("id", None) 

    try:
        # 4. Inserción en MongoDB
        result = users_collection.insert_one(user_dict)

        # 5. Obtener el usuario insertado (con el _id generado)
        new_user = users_collection.find_one({"_id": result.inserted_id})
        
        # 6. Transformar a modelo Pydantic para la respuesta
        if new_user:
            new_user["_id"] = str(new_user["_id"])
            return UserDB(**new_user)

    except Exception as e:
        print(f"Error en POST /: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al conectar o insertar en la base de datos."
        )


# Endpoint: GET /userdb/ (Leer todos los usuarios)
@router.get("/", response_model=List[UserDB])
async def get_users():
    """
    Devuelve todos los usuarios registrados en la colección.
    """
    # Consulta a la base de datos y convertimos los resultados a una lista
    # Usamos .find() sin parámetros para obtener todos
    users_cursor = users_collection.find()
    
    # Convertimos cada documento (dict) a UserDB, asegurando que _id sea string
    user_list = []
    for user_dict in users_cursor:
        user_dict["_id"] = str(user_dict["_id"])
        user_list.append(UserDB(**user_dict))
        
    return user_list


# Endpoint: GET /userdb/{id} (Leer un usuario por ID)
@router.get("/{id}", response_model=UserDB)
async def get_user(id: str):
    """
    Busca un usuario por su ID de MongoDB.
    """
    # 1. Convertir el ID de string a ObjectId para la búsqueda
    try:
        object_id = ObjectId(id)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Formato de ID inválido."
        )

    # 2. Buscar por _id
    user_in_db = users_collection.find_one({"_id": object_id})
    
    if user_in_db is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado."
        )

    # 3. Transformar a Pydantic
    user_in_db["_id"] = str(user_in_db["_id"])
    return UserDB(**user_in_db)


# Endpoint: PUT /userdb/ (Actualizar un usuario)
@router.put("/", response_model=UserDB)
async def update_user(user: UserDB):
    """
    Actualiza la información de un usuario existente.
    """
    # 1. Buscamos el usuario por su ID
    user_to_update = search_user("_id", user.id)
    if user_to_update is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado para actualizar."
        )

    # 2. Hasheamos la nueva contraseña (si se proporciona)
    # NOTA: En este modelo, asumimos que siempre se envía la contraseña (hash o texto plano)
    hashed_password = hash_password(user.password) 

    # 3. Creamos el diccionario de actualización
    update_data = user.model_dump(exclude_unset=True)
    update_data["password"] = hashed_password
    update_data.pop("id", None) # Quitamos el campo 'id' antes de la actualización

    try:
        # 4. Actualización en MongoDB
        users_collection.find_one_and_replace({"_id": ObjectId(user.id)}, update_data)
        
        # 5. Devolver el usuario actualizado
        updated_user_dict = users_collection.find_one({"_id": ObjectId(user.id)})
        
        updated_user_dict["_id"] = str(updated_user_dict["_id"])
        return UserDB(**updated_user_dict)

    except Exception as e:
        print(f"Error en PUT /: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al conectar o actualizar en la base de datos."
        )


# Endpoint: DELETE /userdb/{id} (Eliminar un usuario)
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(id: str):
    """
    Elimina un usuario por su ID de MongoDB.
    """
    # 1. Intentar convertir a ObjectId
    try:
        object_id = ObjectId(id)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Formato de ID inválido."
        )

    # 2. Eliminar el documento
    delete_result = users_collection.delete_one({"_id": object_id})

    # 3. Verificar si se eliminó algo
    if delete_result.deleted_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado."
        )
    # Retorna 204 No Content si es exitoso
'''
'''
                                               # AQUÍ #
from fastapi import APIRouter, HTTPException, status
from db.models.user import UserDB, User, UserUpdate
from db.client import db_client
from db.db_helpers import user_to_userdb, search_user_for_login, search_user_by_id
from bson import ObjectId
from utils.security import hash_password

users_collection = db_client.fastapi_db["users"]

# --- Inicialización del Router ---
# CORRECCIÓN: Se elimina 'prefix=/userdb' ya que se añade en main.py,
# evitando el doble prefijo que causaba el 404.
router = APIRouter(tags=['userdb'], 
                   responses={status.HTTP_404_NOT_FOUND: {'message': 'Usuario no encontrado'}})

# --- Base de Datos ---
# Seleccionamos la colección de usuarios
users_collection = db_client.users

# --- GET: Listar todos los usuarios ---
# Endpoint: GET /userdb/ (gracias al prefix en main.py)
@router.get('/', response_model=list[UserDB])
async def users():
    """
    Lista todos los usuarios en la base de datos 'users' y los devuelve como una lista de UserDB.
    """
    try:
        # Recupera todos los documentos, los convierte a UserDB y luego a lista
        return [UserDB(**user) for user in users_collection.find()]
    except Exception as e:
        print(f"Error al listar usuarios: {e}")
        # Si la colección está vacía o hay un error, devuelve una lista vacía
        return []

# --- GET: Búsqueda por ID (Path Parameter) ---
# Endpoint: GET /userdb/60a7d9b7f5e8f4c3a2b1c0d9
@router.get('/{id}', response_model=UserDB)
async def user(id: str):
    """
    Busca un usuario por su ID de MongoDB.
    """
    found_user = search_user_by_id(id)
    if not found_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Usuario con ID {id} no encontrado"
        )
    return found_user

# --- POST: Creación de un nuevo usuario ---
# Endpoint: POST /userdb/
'''

'''
# Asegúrate de que esta línea esté al inicio del archivo:
# from utils.security import hash_password 
# y que users_collection esté definida globalmente (o localmente)

@router.post('/', response_model=UserDB, status_code=status.HTTP_201_CREATED)
async def user(user: User):
    """
    Crea un nuevo usuario en la base de datos, hasheando la contraseña.
    Verifica si el username o email ya existen.
    """
    
    # 1. Validación de existencia (username o email)
    # NOTA: Asumimos que users_collection está definido globalmente o se inicializa justo antes.
    if users_collection.find_one({"username": user.username}) or users_collection.find_one({"email": user.email}):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="El usuario o el email ya existe."
        )
        
    # 2. Convertir a diccionario
    user_dict = user.model_dump()
    
    # --------------------------------------------------------
    # 3. HASHING DE CONTRASEÑA E INSERCIÓN DE SEGURIDAD (CÓDIGO CLAVE)
    # --------------------------------------------------------
    
    # 3.1. Hashear la contraseña. Usamos un try-except para detectar fallos de bcrypt/importación.
    try:
        hashed_password = hash_password(user_dict["password"]) 
    except Exception:
        # Esto debería capturar errores si bcrypt no está instalado o si la importación falló
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error de seguridad al hashear la contraseña. ¿Está 'bcrypt' instalado y Uvicorn reiniciado?"
        )
    
    # 3.2. Eliminar la contraseña en texto plano del diccionario antes de guardar
    del user_dict["password"] 
    
    # 3.3. Añadir la contraseña hasheada al diccionario
    user_dict["password"] = hashed_password 
    
    # 4. Insertar en MongoDB
    try:
        result = users_collection.insert_one(user_dict)
        
        # 5. Obtener el documento recién creado (incluyendo el ID)
        new_user = users_collection.find_one({"_id": result.inserted_id})
        
        # 6. Construir la respuesta (UserDB)
        return UserDB(**new_user)
        
    except Exception as e:
        # Manejo de errores de inserción
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al crear el usuario en la DB: {e}"
        )

# --- PUT: Actualización de un usuario ---
# Endpoint: PUT /userdb/{id}
@router.put('/{id}', response_model=UserDB)
async def user(id: str, user_update: UserUpdate):
    """
    Actualiza los datos de un usuario existente por su ID.
    """
    
    # 1. Convertir Pydantic a diccionario para MongoDB
    update_data = user_update.model_dump(exclude_unset=True) # Excluye campos que no se proporcionaron
    
    # 2. Buscar si existe
    if not search_user_by_id(id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Usuario con ID {id} no encontrado."
        )
        
    # 3. Actualizar
    try:
        # Usa $set para actualizar solo los campos proporcionados
        users_collection.update_one({"_id": ObjectId(id)}, {"$set": update_data})
        
        # 4. Devolver el usuario actualizado
        return search_user_by_id(id)
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al actualizar el usuario: {e}"
        )

# --- DELETE: Eliminación de un usuario ---
# Endpoint: DELETE /userdb/{id}
@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def user(id: str):
    """
    Elimina un usuario de la base de datos por su ID.
    """
    
    # 1. Buscar si existe
    result = users_collection.delete_one({"_id": ObjectId(id)})
    
    # 2. Verificar si se eliminó (n = número de documentos eliminados)
    if result.deleted_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Usuario con ID {id} no encontrado."
        )
    
    # Devuelve 204 No Content si fue exitoso (no devuelve cuerpo)
                              # HASTA AQUÍ #
'''
'''
from fastapi import APIRouter, HTTPException, status
from typing import List, Optional
from bson import ObjectId # Importamos ObjectId para el manejo de IDs de MongoDB
from bson import errors # Importamos errores para capturar específicamente el error de formato de ID

# Importamos las funciones de seguridad
from utils.security import hash_password 

# Importamos los modelos de Pydantic
from db.models.user import User, UserDB, UserUpdate
# Importamos la conexión a la base de datos
from db.client import db_client 

# NOTA IMPORTANTE: Se elimina el prefijo duplicado en main.py. Si tu main.py tiene:
# app.include_router(users_db.router, tags=["MongoDB Users"], prefix="/userdb")
# ENTONCES el prefijo DEBE ir aquí, como está actualmente.
router = APIRouter(prefix='/userdb', tags=['usersdb'], responses={
    status.HTTP_404_NOT_FOUND: {'message': 'Usuario no encontrado'},
    status.HTTP_409_CONFLICT: {'message': 'El usuario o email ya existe'}
})

# Nombre de la colección en MongoDB
COLLECTION_NAME = "users"

# --- Función Auxiliar de Conversión ---
def user_to_userdb(user: dict) -> UserDB:
    """
    Convierte un documento de MongoDB (dict) en un modelo Pydantic UserDB.
    Asegura que el _id de MongoDB (ObjectId) se mapee a 'id' (str) en el modelo.
    """
    return UserDB(
        id=str(user["_id"]),
        username=user["username"],
        email=user["email"],
        password=user["password"]
    )

# --- Función Auxiliar de Búsqueda para Login/Validación ---
def search_user_for_login(field: str, key: str) -> Optional[dict]:
    """
    Busca un usuario en la base de datos por un campo (username o email).
    Devuelve el documento de MongoDB (dict), o None si no se encuentra.
    """
    try:
        # Aquí usamos db_client y seleccionamos la colección
        user_doc = db_client[COLLECTION_NAME].find_one({field: key}) 
        return user_doc # Retorna el diccionario de MongoDB, o None si no lo encuentra
    except Exception:
        # Si hay un error de conexión, la función retorna None
        return None

# --- Rutas CRUD Completas ---

# Endpoint: GET /userdb/ (Leer todos los usuarios)
@router.get("/", response_model=List[UserDB])
async def get_users():
    """
    Devuelve la lista completa de todos los usuarios registrados, omitiendo documentos corruptos.
    """
    valid_users = []
    
    # 🛑 Verificar conexión
    if db_client is None:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Conexión a MongoDB fallida. Verifique que el servicio esté activo.")

    # 🟢 Usamos la notación de diccionario para obtener la colección
    for user_doc in db_client[COLLECTION_NAME].find():
        try:
            # Intentamos convertir el documento
            userdb_model = user_to_userdb(user_doc)
            valid_users.append(userdb_model)
        except KeyError as e:
            # Si falta un campo (como username o password), este documento se omite.
            print(f"Error al convertir documento con ID {user_doc.get('_id')}: Falta el campo {e}")
            continue # Pasa al siguiente documento
        except Exception as e:
            print(f"Error desconocido al convertir un documento: {e}")
            continue

    return valid_users # Devuelve solo los usuarios válidos

# Endpoint: GET /userdb/{id} (Leer un usuario por ID)
@router.get("/{id}", response_model=UserDB)
async def get_user_by_id(id: str):
    """
    Busca un usuario por su ID de MongoDB.
    """
    # 🛑 Verificar conexión
    if db_client is None:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Conexión a MongoDB fallida.")

    # 🔴 LÍNEA DE DEBUGGING: Muestra el ID recibido
    print(f"DEBUG: ID recibido por el endpoint: {id}") 

    try:
        # Intentamos convertir el string ID a ObjectId para la búsqueda en MongoDB
        user_id_object = ObjectId(id)
    except errors.InvalidId: # Capturamos el error específico de formato de ID
        # Si el ID no es válido (ej. tiene longitud incorrecta), lanzamos 404
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Formato de ID inválido.")
    except Exception as e:
        # Otros errores de BSON o conexión
        print(f"Error inesperado al intentar crear ObjectId: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error interno al procesar el ID.")

    # Ahora buscamos el documento
    user_doc = db_client[COLLECTION_NAME].find_one({"_id": user_id_object})

    if user_doc is None:
        # Si no se encuentra el documento
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado.")

    # Convertimos el documento de MongoDB a UserDB
    return user_to_userdb(user_doc)

# Endpoint: GET /userdb/search?username=... (Búsqueda por Query)
@router.get("/search", response_model=UserDB)
async def search_user(username: Optional[str] = None, email: Optional[str] = None):
    """
    Busca un usuario por username o email usando query parameters.
    """
    # 🛑 Verificar conexión
    if db_client is None:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Conexión a MongoDB fallida.")
    
    # Definimos el campo y la clave de búsqueda
    search_field = None
    search_key = None

    if username:
        search_field = "username"
        search_key = username
    elif email:
        search_field = "email"
        search_key = email
    else:
        # Si no se proporciona ni username ni email, es una petición incorrecta
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Se requiere 'username' o 'email' para la búsqueda.")

    # 1. Hacemos la búsqueda simple
    user_doc = db_client[COLLECTION_NAME].find_one({search_field: search_key})

    if user_doc is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado.")

    return user_to_userdb(user_doc)


# Endpoint: POST /userdb/ (Crear un nuevo usuario)
@router.post("/", response_model=UserDB, status_code=status.HTTP_201_CREATED)
async def create_user(user: User):
    """
    Crea un nuevo usuario con contraseña hasheada, verificando unicidad de username y email.
    """
    # 🛑 Verificar conexión
    if db_client is None:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Conexión a MongoDB fallida.")
        
    # 1. Verificar unicidad antes de insertar
    if search_user_for_login("username", user.username) or search_user_for_login("email", user.email):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="El usuario o email ya existe.")
    
    # 2. Hash de la contraseña
    # Asegúrate de que utils/security.py esté importado y tenga la función hash_password
    hashed_password = hash_password(user.password)

    # 3. Preparar documento para MongoDB
    user_dict = user.model_dump() # Usar model_dump() en Pydantic v2
    del user_dict["password"] # Eliminamos el texto plano antes de reemplazarlo
    user_dict["password"] = hashed_password

    # 4. Insertar en MongoDB
    try:
        result = db_client[COLLECTION_NAME].insert_one(user_dict)
        
        # 5. Obtener el documento recién creado (incluyendo el ID)
        new_user_doc = db_client[COLLECTION_NAME].find_one({"_id": result.inserted_id})

        # 6. Devolver el modelo Pydantic del nuevo usuario
        return user_to_userdb(new_user_doc)

    except Exception as e:
        print(f"Error al insertar en MongoDB: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error en la base de datos al crear el usuario.")

# Endpoint: PUT /userdb/ (Actualizar un usuario)
@router.put("/", response_model=UserDB)
async def update_user(user_update: UserUpdate):
    """
    Actualiza la información de un usuario existente por su ID.
    Solo actualiza los campos proporcionados (excepto el ID).
    """
    # 🛑 Verificar conexión
    if db_client is None:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Conexión a MongoDB fallida.")
    
    # 1. Obtenemos el diccionario del usuario, excluyendo los valores que no fueron seteados (muy importante para PUT)
    # y también excluyendo el campo 'id' que solo usamos para la búsqueda
    user_dict = user_update.model_dump(exclude_unset=True, exclude={'id'}) # Usar model_dump()

    # 2. Manejo especial de la contraseña
    if 'password' in user_dict:
        # Si se proporciona la contraseña, la hasheamos
        user_dict["password"] = hash_password(user_dict["password"])

    # 3. Verificar que el ID sea válido para MongoDB antes de buscar/actualizar
    try:
        user_id_object = ObjectId(user_update.id)
    except:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Formato de ID inválido.")
    
    # 4. Construir la consulta de actualización de MongoDB
    update_query = {"$set": user_dict}

    # 5. Ejecutar la actualización
    result = db_client[COLLECTION_NAME].update_one(
        {"_id": user_id_object}, 
        update_query
    )

    if result.matched_count == 0:
        # Si no se encontró el usuario para actualizar
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado.")

    # 6. Devolver el documento actualizado
    updated_user_doc = db_client[COLLECTION_NAME].find_one({"_id": user_id_object})
    return user_to_userdb(updated_user_doc)

# Endpoint: DELETE /userdb/{id} (Eliminar un usuario)
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(id: str):
    """
    Elimina un usuario por su ID de MongoDB.
    """
    # 🛑 Verificar conexión
    if db_client is None:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Conexión a MongoDB fallida.")

    # 1. Verificar que el ID sea válido para MongoDB
    try:
        user_id_object = ObjectId(id)
    except:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Formato de ID inválido.")
    
    # 2. Ejecutar la eliminación
    result = db_client[COLLECTION_NAME].delete_one({"_id": user_id_object})

    if result.deleted_count == 0:
        # Si no se eliminó nada, es porque no existía
        raise HTTPException(status_code=status.HTTP_404_NOT_NOT_FOUND, detail="Usuario no encontrado.")
    
    # 3. Devolver 204 No Content (No devuelve cuerpo de respuesta)
    return
'''
'''
from fastapi import APIRouter, HTTPException, status
from db.models.user import UserDB, User, UserUpdate
from db.client import db_client # Necesario para obtener la conexión a la DB
from db.db_helpers import user_to_userdb, search_user_for_login, search_user_by_id
from bson import ObjectId
from utils.security import hash_password # ¡La clave de la seguridad!

# --- Configuración del Router (Definición obligatoria) ---
# Esta línea debe ser la primera después de las importaciones.
router = APIRouter(prefix="/userdb", tags=["MongoDB Users"])

# --- COLECCIÓN DE MONGODB (DEFINICIÓN GLOBAL CORREGIDA) ---
# Se define la colección de forma global, asumiendo que db_client ya ha sido inicializado.
users_collection = db_client.fastapi_db["users"] 

# --- FUNCIONES AUXILIARES DE LA RUTA ---

def find_user_by_id(user_id: str):
    """Busca un usuario por su ID (str de ObjectId) y lo devuelve como UserDB."""
    try:
        # La colección ya está definida globalmente
        
        # Convierte la cadena ID a ObjectId de BSON
        user_doc = users_collection.find_one({"_id": ObjectId(user_id)})
        
        if user_doc:
            # Convierte el documento de MongoDB (dict) a un modelo Pydantic (UserDB)
            # FIX: Aseguramos la conversión del _id a string
            user_doc["_id"] = str(user_doc["_id"]) 
            return UserDB(**user_doc)
        return None
    except Exception:
        # Devuelve None si el ID no es válido (ej. cadena de 12 bytes no válida)
        return None

def find_user_by_username(username: str):
    """Busca un usuario por su nombre de usuario."""
    # La colección ya está definida globalmente
    user_doc = users_collection.find_one({"username": username})
    if user_doc:
        # FIX: Aseguramos la conversión del _id a string
        user_doc["_id"] = str(user_doc["_id"]) 
        return UserDB(**user_doc)
    return None

# --- ENDPOINTS (CRU D) ---

# Ruta GET (Leer todos los usuarios - Solo para desarrollo/debugging)
@router.get('/', response_model=list[UserDB])
async def users():
    """Devuelve la lista completa de usuarios de la base de datos."""
    # La colección ya está definida globalmente
    
    # Mapea todos los documentos encontrados a la lista de modelos UserDB
    users_list = []
    for user_doc in users_collection.find():
        # FIX: Conversión obligatoria de _id a str para evitar error Pydantic
        user_doc["_id"] = str(user_doc["_id"])
        users_list.append(UserDB(**user_doc))

    return users_list

# Ruta GET (Leer un usuario por ID)
@router.get('/{user_id}', response_model=UserDB)
async def user_by_id(user_id: str):
    """Busca un usuario por su ID de MongoDB (ObjectId)."""
    user = find_user_by_id(user_id)
    if user:
        return user
    
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Usuario con ID '{user_id}' no encontrado"
    )

# Ruta POST (Crear un nuevo usuario - CON HASHING)
@router.post('/', response_model=UserDB, status_code=status.HTTP_201_CREATED)
async def user(user: User):
    """
    Crea un nuevo usuario en la base de datos, hasheando la contraseña.
    Verifica si el username o email ya existen.
    """
    # La colección ya está definida globalmente

    # 1. Validación de existencia (username o email)
    if users_collection.find_one({"username": user.username}) or users_collection.find_one({"email": user.email}):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="El usuario o el email ya existe."
        )
        
    # 2. Convertir a diccionario
    user_dict = user.model_dump()
    
    # --------------------------------------------------------
    # 3. HASHING DE CONTRASEÑA Y PREPARACIÓN PARA INSERCIÓN
    # --------------------------------------------------------
    
    # 3.1. Hashear la contraseña. 
    try:
        # Nota: Accedemos directamente al campo 'password' del diccionario/modelo.
        hashed_password = hash_password(user_dict["password"]) 
    except Exception as e:
        # Muestra el error específico para debugging.
        print(f"ERROR DE HASHING: {e}") 
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error de seguridad: Fallo al hashear la contraseña. Confirma instalación de 'bcrypt'."
        )
    
    # 3.2. Eliminar la contraseña en texto plano del diccionario antes de guardar
    del user_dict["password"] 
    
    # 3.3. Añadir la contraseña hasheada al diccionario
    user_dict["password"] = hashed_password 
    
    # 4. Insertar en MongoDB
    try:
        result = users_collection.insert_one(user_dict)
        
        # 5. Obtener el documento recién creado (incluyendo el ID)
        new_user = users_collection.find_one({"_id": result.inserted_id})
        
        # 6. Construir la respuesta (UserDB)
        # FIX CLAVE: Convertir el ObjectId a string antes de pasarlo al modelo
        new_user["_id"] = str(new_user["_id"]) 
        return UserDB(**new_user)
        
    except Exception as e:
        # Manejo de errores de inserción
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al crear el usuario en la DB: {e}"
        )
        
# Ruta PUT (Actualizar un usuario)
@router.put('/', response_model=UserDB)
async def user_put(user_update: UserUpdate):
    """Actualiza los datos de un usuario existente por ID. Permite cambiar el password (se hashea)."""
    # La colección ya está definida globalmente
    
    # 1. Validar que el ID sea un ObjectId válido
    try:
        object_id = ObjectId(user_update.id)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"ID '{user_update.id}' no es un ObjectId de MongoDB válido."
        )

    # 2. Convertir el modelo de actualización a diccionario, eliminando campos None
    update_data = user_update.model_dump(exclude_none=True, exclude={'id'})
    
    # 3. Hashing: Si la contraseña está presente en la actualización, hashearla
    if "password" in update_data:
        try:
            hashed_password = hash_password(update_data["password"])
            update_data["password"] = hashed_password
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error de seguridad al hashear la contraseña: {e}"
            )
            
    # 4. Aplicar la actualización en MongoDB
    try:
        # Usamos $set para actualizar solo los campos proporcionados
        update_result = users_collection.update_one(
            {"_id": object_id},
            {"$set": update_data}
        )
    except Exception as e:
         raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error de base de datos durante la actualización: {e}"
        )
        
    # 5. Verificar si se actualizó algo
    if update_result.matched_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Usuario con ID '{user_update.id}' no encontrado para actualizar."
        )

    # 6. Devolver el documento actualizado
    updated_user_doc = users_collection.find_one({"_id": object_id})
    # FIX CLAVE: Convertir el ObjectId a string antes de pasarlo al modelo
    updated_user_doc["_id"] = str(updated_user_doc["_id"]) 
    return UserDB(**updated_user_doc)

# Ruta DELETE (Eliminar un usuario)
@router.delete('/{user_id}', status_code=status.HTTP_204_NO_CONTENT)
async def user_delete(user_id: str):
    """Elimina un usuario por ID y devuelve una respuesta vacía si tiene éxito."""
    # La colección ya está definida globalmente
    
    # 1. Validar que el ID sea un ObjectId válido
    try:
        object_id = ObjectId(user_id)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"ID '{user_id}' no es un ObjectId de MongoDB válido."
        )
        
    # 2. Ejecutar la eliminación
    delete_result = users_collection.delete_one({"_id": object_id})
    
    # 3. Verificar si se eliminó
    if delete_result.deleted_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Usuario con ID '{user_id}' no encontrado para eliminar."
        )
    
    # 4. Devolver una respuesta vacía (204 NO_CONTENT)
    return
'''


                                      # DESDE AQUÍ
'''
from fastapi import APIRouter, HTTPException, status
# Se elimina la importación de BaseModel ya que UserAuth ya no se usa
from db.models.user import UserDB, User, UserUpdate
from db.client import db_client 
from bson import ObjectId
# Se mantiene hash_password y verify_password ya que se usan para crear/actualizar
from utils.security import hash_password, verify_password 

# --- Configuración del Router (Definición obligatoria) ---
router = APIRouter(prefix="/userdb", tags=["MongoDB Users"])

# --- COLECCIÓN DE MONGODB ---
users_collection = db_client.fastapi_db["users"] 

# --- Funciones Auxiliares ---

def find_user_by_id(user_id: str):
    """Busca un usuario por su ID (str de ObjectId) y lo devuelve como UserDB."""
    try:
        user_doc = users_collection.find_one({"_id": ObjectId(user_id)})
        if user_doc:
            user_doc["_id"] = str(user_doc["_id"]) 
            return UserDB(**user_doc)
        return None
    except Exception:
        return None

# --- ENDPOINTS (Solo CRUD bajo /userdb) ---

# 1. Ruta GET (Leer todos los usuarios)
@router.get('/', response_model=list[UserDB])
async def users():
    """Devuelve la lista completa de usuarios de la base de datos."""
    users_list = []
    for user_doc in users_collection.find():
        user_doc["_id"] = str(user_doc["_id"])
        users_list.append(UserDB(**user_doc))
    return users_list


# 2. Ruta POST (Crear un nuevo usuario - REGISTRO)
@router.post('/', response_model=UserDB, status_code=status.HTTP_201_CREATED)
async def user(user: User):
    """Crea un nuevo usuario en la base de datos, hasheando la contraseña."""

    # 1. Validación de existencia (username o email)
    if users_collection.find_one({"username": user.username}) or users_collection.find_one({"email": user.email}):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="El usuario o el email ya existe."
        )
        
    user_dict = user.model_dump()
    
    try:
        hashed_password = hash_password(user_dict["password"]) 
        del user_dict["password"] 
        user_dict["password"] = hashed_password 
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error de seguridad: Fallo al hashear la contraseña."
        )
    
    try:
        result = users_collection.insert_one(user_dict)
        new_user = users_collection.find_one({"_id": result.inserted_id})
        new_user["_id"] = str(new_user["_id"]) 
        return UserDB(**new_user)
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al crear el usuario en la DB: {e}"
        )


# 3. Ruta GET (Leer un usuario por ID)
@router.get('/{user_id}', response_model=UserDB)
async def user_by_id(user_id: str):
    """Busca un usuario por su ID de MongoDB (ObjectId)."""
    user = find_user_by_id(user_id)
    if user:
        return user
    
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Usuario con ID '{user_id}' no encontrado"
    )

# 4. Ruta PUT (Actualizar un usuario)
@router.put('/', response_model=UserDB)
async def user_put(user_update: UserUpdate):
    """Actualiza los datos de un usuario existente por ID. Permite cambiar el password (se hashea)."""
    
    try:
        object_id = ObjectId(user_update.id)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"ID '{user_update.id}' no es un ObjectId de MongoDB válido."
        )

    update_data = user_update.model_dump(exclude_none=True, exclude={'id'})
    
    if "password" in update_data:
        try:
            hashed_password = hash_password(update_data["password"])
            update_data["password"] = hashed_password
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error de seguridad al hashear la contraseña: {e}"
            )
            
    try:
        update_result = users_collection.update_one(
            {"_id": object_id},
            {"$set": update_data}
        )
    except Exception as e:
         raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error de base de datos durante la actualización: {e}"
        )
        
    if update_result.matched_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Usuario con ID '{user_update.id}' no encontrado para actualizar."
        )

    updated_user_doc = users_collection.find_one({"_id": object_id})
    updated_user_doc["_id"] = str(updated_user_doc["_id"]) 
    return UserDB(**updated_user_doc)

# 5. Ruta DELETE (Eliminar un usuario)
@router.delete('/{user_id}', status_code=status.HTTP_204_NO_CONTENT)
async def user_delete(user_id: str):
    """Elimina un usuario por ID y devuelve una respuesta vacía si tiene éxito."""
    
    try:
        object_id = ObjectId(user_id)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"ID '{user_id}' no es un ObjectId de MongoDB válido."
        )
        
    delete_result = users_collection.delete_one({"_id": object_id})
    
    if delete_result.deleted_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Usuario con ID '{user_id}' no encontrado para eliminar."
        )
    
    return                             # HASTA AQUÍ
'''
from fastapi import APIRouter, HTTPException, status
# Se elimina la importación de BaseModel ya que UserAuth ya no se usa
from db.models.user import UserDB, User, UserUpdate
from db.client import db_client 
from bson import ObjectId
# Se mantiene hash_password y verify_password ya que se usan para crear/actualizar
from utils.security import hash_password, verify_password 

# --- Configuración del Router (Definición obligatoria) ---
router = APIRouter(prefix="/userdb", tags=["MongoDB Users"])

# --- COLECCIÓN DE MONGODB ---
#users_collection = db_client.fastapi_db["users"]     # Para localhost
users_collection = db_client.Pedro_db_user["users"]  # Para Mongo-ATLAS
#users_collection = db_client.fastapi_db["users"]      # Para Mongo-ATLAS

# --- Funciones Auxiliares ---

def find_user_by_id(user_id: str):
    """Busca un usuario por su ID (str de ObjectId) y lo devuelve como UserDB."""
    try:
        user_doc = users_collection.find_one({"_id": ObjectId(user_id)})
        if user_doc:
            user_doc["_id"] = str(user_doc["_id"]) 
            return UserDB(**user_doc)
        return None
    except Exception:
        return None

# --- FUNCIONES AUXILIARES PARA AUTENTICACIÓN (JWT) ---
# ESTA FUNCIÓN ES CRUCIAL PARA EL LOGIN JWT
def search_user_for_login(field: str, key):
    """
    Busca un usuario por un campo específico (e.g., 'username')
    y devuelve el documento completo de MongoDB (dict)
    incluyendo el hash de la contraseña para el proceso de Login.
    """
    try:
        # Aquí se usa find_one para buscar el documento completo
        user_doc = users_collection.find_one({field: key})
        return user_doc if user_doc else None
    except Exception as e:
        print(f"Error al buscar usuario para login: {e}")
    return None

# --- ENDPOINTS (Solo CRUD bajo /userdb) ---

# 1. Ruta GET (Leer todos los usuarios)
@router.get('/', response_model=list[UserDB])
async def users():
    """Devuelve la lista completa de usuarios de la base de datos."""
    users_list = []
    for user_doc in users_collection.find():
        user_doc["_id"] = str(user_doc["_id"])
        users_list.append(UserDB(**user_doc))
    return users_list


# 2. Ruta POST (Crear un nuevo usuario - REGISTRO)
@router.post('/', response_model=UserDB, status_code=status.HTTP_201_CREATED)
async def user(user: User):
    """Crea un nuevo usuario en la base de datos, hasheando la contraseña."""

    # 1. Validación de existencia (username o email)
    if users_collection.find_one({"username": user.username}) or users_collection.find_one({"email": user.email}):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="El usuario o el email ya existe."
        )
        
    user_dict = user.model_dump()
    
    try:
        hashed_password = hash_password(user_dict["password"]) 
        del user_dict["password"] 
        user_dict["password"] = hashed_password 
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error de seguridad: Fallo al hashear la contraseña."
        )
    
    try:
        result = users_collection.insert_one(user_dict)
        new_user = users_collection.find_one({"_id": result.inserted_id})
        new_user["_id"] = str(new_user["_id"]) 
        return UserDB(**new_user)
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al crear el usuario en la DB: {e}"
        )


# 3. Ruta GET (Leer un usuario por ID)
@router.get('/{user_id}', response_model=UserDB)
async def user_by_id(user_id: str):
    """Busca un usuario por su ID de MongoDB (ObjectId)."""
    user = find_user_by_id(user_id)
    if user:
        return user
    
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Usuario con ID '{user_id}' no encontrado"
    )

# 4. Ruta PUT (Actualizar un usuario)
@router.put('/', response_model=UserDB)
async def user_put(user_update: UserUpdate):
    """Actualiza los datos de un usuario existente por ID. Permite cambiar el password (se hashea)."""
    
    try:
        object_id = ObjectId(user_update.id)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"ID '{user_update.id}' no es un ObjectId de MongoDB válido."
        )

    update_data = user_update.model_dump(exclude_none=True, exclude={'id'})
    
    if "password" in update_data:
        try:
            hashed_password = hash_password(update_data["password"])
            update_data["password"] = hashed_password
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error de seguridad al hashear la contraseña: {e}"
            )
            
    try:
        update_result = users_collection.update_one(
            {"_id": object_id},
            {"$set": update_data}
        )
    except Exception as e:
           raise HTTPException(
             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
             detail=f"Error de base de datos durante la actualización: {e}"
         )
         
    if update_result.matched_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Usuario con ID '{user_update.id}' no encontrado para actualizar."
        )

    updated_user_doc = users_collection.find_one({"_id": object_id})
    updated_user_doc["_id"] = str(updated_user_doc["_id"]) 
    return UserDB(**updated_user_doc)

# 5. Ruta DELETE (Eliminar un usuario)
@router.delete('/{user_id}', status_code=status.HTTP_204_NO_CONTENT)
async def user_delete(user_id: str):
    """Elimina un usuario por ID y devuelve una respuesta vacía si tiene éxito."""
    
    try:
        object_id = ObjectId(user_id)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"ID '{user_id}' no es un ObjectId de MongoDB válido."
        )
        
    delete_result = users_collection.delete_one({"_id": object_id})
    
    if delete_result.deleted_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Usuario con ID '{user_id}' no encontrado para eliminar."
        )
    
    return


                           











