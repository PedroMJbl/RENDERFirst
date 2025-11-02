from typing import Optional
from bson import ObjectId, errors
from pydantic import BaseModel, EmailStr
from db.client import db_client 
# Asumimos que los modelos UserDB y User se definen en db/models/user
from db.models.user import UserDB, User 

COLLECTION_NAME = "users"

def user_to_userdb(user_doc: dict) -> UserDB:
    """Convierte un documento de MongoDB (dict) a un modelo Pydantic UserDB."""
    if user_doc:
        return UserDB(
            id=str(user_doc["_id"]), 
            username=user_doc.get("username", "N/A"),
            email=user_doc.get("email", "N/A"),
            password=user_doc.get("password", "") 
        )
    return None

def search_user_by_id(id: str) -> Optional[UserDB]:
    """Busca un usuario por su ID de MongoDB. Devuelve el modelo UserDB."""
    if db_client is None:
        return None
    
    try:
        user_id_object = ObjectId(id)
    except errors.InvalidId:
        return None # Devuelve None si el formato ID es inválido
    
    user_doc = db_client[COLLECTION_NAME].find_one({"_id": user_id_object})
    
    if user_doc is None:
        return None

    return user_to_userdb(user_doc)

def search_user_for_login(field: str, key: str) -> Optional[dict]:
    """Busca un usuario por campo (username o email). Devuelve el dict de MongoDB."""
    if db_client is None:
        return None
    
    # db_client es el objeto Database. Accedemos a la colección y buscamos.
    user_doc = db_client[COLLECTION_NAME].find_one({field: key})
    return user_doc
