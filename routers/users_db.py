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

# --- ENDPOINTS (RUTAS) ---
'''
@router.get("/", response_model=list[User])
async def users():
    """Obtiene todos los usuarios de la base de datos."""
    return user_schema(db_client.local.users.find())   # corregido de 'users_schema' a 'user_schema'
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