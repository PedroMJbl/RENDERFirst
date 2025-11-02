
#from pymongo import MongoClient

#db_client = MongoClient ()

                                      # Gemini #

from pymongo import MongoClient
import os

# URI de conexión a MongoDB. 
# Si usas un puerto diferente o Atlas, ajusta esta línea.
# NOTA: Por defecto, se usa localhost.
MONGO_DB_URI = "mongodb://localhost:27017" # Para localhost
#MONGO_DB_URI = "mongodb+srv://Pedro_db_user:ArhjnM57i@cluster-de-pedro-atlas.w5yrex6.mongodb.net/" # Para Mongo-ATLAS
#MONGO_DB_URI = "mongodb+srv://fastapi_db:ArhjnM57i@cluster-de-pedro-atlas.w5yrex6.mongodb.net/" # Para Mongo-ATLAS
try:
    # Intenta conectar al cliente MongoDB
    db_client = MongoClient(MONGO_DB_URI)
    
    # Intenta acceder a una base de datos para confirmar la conexión
    db = db_client.fastapi_db
    #db = db_client.Pedro_db_user
    print("Conexión a MongoDB exitosa. Usando base de datos: fastapi_db")
    
except Exception as e:
    print(f"Error al conectar a MongoDB. Asegúrate de que el servicio de MongoDB esté activo: {e}")
    db_client = None 

