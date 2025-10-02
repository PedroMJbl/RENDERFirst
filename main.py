
### miércoles, 18 de junio de 2025 08:25 Empiezo ###

from fastapi import FastAPI
from routers import products,users,jwt_auth_users,basic_auth_users,users_db
from db.client import db_client # martes, 30 de septiembre de 2025 05:56
from fastapi.staticfiles import StaticFiles
#from routers import users
#from routers import users

app = FastAPI()

#Routers

app.include_router(products.router)
app.include_router(users.router)
app.include_router(jwt_auth_users.router)
app.include_router(basic_auth_users.router)
app.include_router(users_db.router)
app.mount('/Static',StaticFiles(directory='Static'),name='Static')




'''
@app.get('/')
async def root():
    #return '¡Hola FastAPI!'
    return '¡Hola Mundo!'
'''
'''
@app.get('/n')
async def root2():
    #return '¡Hola FastAPI!'
    return '¡Hola Mundo!2'

# url local http://127.0.0.1:8000
### 18/06/2025 9:15 Acabo ###
### 7:47 19/06/2025 Empiezo ###
'''

#@app.get('/url')
#async def url():
    
   # return '¡Hola FastAPI!'
    #return {'url':'https://mouredev.com/python'}

'''
@app.get('/url')
async def url():
   # return '¡Hola FastAPI!'
     return {'url':'https://mouredev.com/python'}
'''
### 19/06/2025 8:38 Acabo ###
### viernes, 20 de junio de 2025 18:57 Empiezo ###





                                            ### 20/06/2025 20:04 Acabo ###

                                    ### sábado, 21 de junio de 2025 08:15 Empiezo ###
                                    ### domingo, 27 de julio de 2025 06:57 Empiezo ###

                                      # Inicia el server: uvicorn main:app --reload
                                      # Detiene el server: CTRL+C

                                  # Documentación con Swagger: http://127.0.01:8000/docs
                                  # Documentación con Redocly: http://127.0.01:8000/redoc

#from fastapi import FastAPI
#from routers import products

#app = FastAPI()

# Routers

#app.include_router(products.router)

@app.get('/')
async def root():
    return '¡Hola FastAPI!'
    #return '¡Hola Mundo!'

#@app.get('/url')
#async def url():
   # return '¡Hola FastAPI!'
     #return {'url':'https://mouredev.com/python'}

                                    ### jueves, 7 de agosto de 2025 06:17 Empiezo ###

@app.get('/url')
async def url():
   # return '¡Hola FastAPI!'
     return {'url':'https://mouredev.com/python'}                                    
# lunes, 11 de agosto de 2025 19:27 Empiezo la hora #
# 11/08/2025 20:44 Se acabó la hora, mañana sigo #
# 12/08/2025 7:56:51 07:56 Empiezo la hora #
# 24/08/2025 9:00 Aquí lo dejo #
# domingo, 24 de agosto de 2025 19:31 Empieza la hora #
# 24/08/2025 20:51 Hasta aquí la hora de hoy #
# lunes, 25 de agosto de 2025 06:43 Empiezo #
# 25/08/2025 8:20 Acabo #
# lunes, 25 de agosto de 2025 19:19 Empiezo hora #
# 25/08/2025 20:52 Acabo #
# martes, 26 de agosto de 2025 07:32 Empiezo la hora #
# martes, 26 de agosto de 2025 19:43 Empiezo la hora #
# 26/08/2025 20:47 Acabo la hora #
# miércoles, 27 de agosto de 2025 08:07 Empiezo la hora #
# 27/08/2025 9:16 Acabo la hora #
# miércoles, 27 de agosto de 2025 19:58 Empiezo la hora #
# jueves, 28 de agosto de 2025 07:16 Empiezo la hora #

                                      # martes, 9 de septiembre de 2025 19:15 Empiezo hora #

'''
from pymongo import MongoClient

# Cadena de conexión anterior (que usaba localhost)
MONGO_URI = "mongodb://localhost:27017/"

# Nueva cadena de conexión usando la IP de tu Docker
DOCKER_MONGO_IP = "192.168.99.100"  # Confirma que esta es tu IP de Docker
MONGO_URI = f"mongodb://{DOCKER_MONGO_IP}:27017/"

# ...el resto de tu código
client = MongoClient(MONGO_URI)
db = client.users_db.py
'''

'''
def clear_mouredev_users():
     users_collection = db_client.local.users
     print(f"✅ Se han eliminado {result.deleted_count} usuarios con el nombre 'mouredev'.")
     result = users_collection.delete_many({"username": "mouredev"})
'''
'''
def clear_all_mouredev_users():
    pass
    users_collection = db_client.local.users
    
    # 1. 🟢 Primero, se ejecuta la operación de borrado.
    #    Esto crea la variable 'result'.
    result = users_collection.delete_many({"username": "mouredev"})
    
    # 2. 🟢 Segundo, se imprime el mensaje usando la variable 'result'.
    print(f"✅ Se han eliminado {result.deleted_count} usuarios con el nombre 'mouredev'.")
'''
    


# main.py

# 🚨 ASEGÚRATE DE QUE ESTA LÍNEA ESTÉ AL PRINCIPIO
from db.client import db_client 
# ... (otras importaciones) ...

# 🟢 Define la función de borrado (con el orden correcto)
def clear_all_mouredev_users():
    print("--- INICIANDO BORRADO ---") # ⬅️ Nuevo mensaje de inicio
    
    users_collection = db_client.local.users
    
    result = users_collection.delete_many({"username": "mouredev"})
    
    print(f"✅ Se han eliminado {result.deleted_count} usuarios con el nombre 'mouredev'.")
    print("--- BORRADO FINALIZADO ---") # ⬅️ Nuevo mensaje de fin

# ⚠️ LLAMADA A LA FUNCIÓN (Debe estar al mismo nivel que 'def')
#clear_all_mouredev_users()  Comentada por orden de Gemini

# ... (El resto de tu código de FastAPI, incluyendo app = FastAPI(), etc.)
