'''
from pydantic import BaseModel

class User(BaseModel):
    
    id:str | None
    username: str
    email: st
'''
                                                     # viernes, 29 de agosto de 2025 07:57 Empiezo la hora #

                                                    # Gemini sábado, 27 de septiembre de 2025 20:09 #

# Archivo: db/models/user.py

# Archivo: db/models/user.py

# Archivo: db/models/user.py

# Archivo: db/models/user.py
'''                                          Gemini
from pydantic import BaseModel

class User(BaseModel):
    id: str | None = None # Hacemos el ID opcional
    username: str
    email: str
    
    # AÑADE ESTOS CAMPOS FALTANTES y hazlos opcionales
    name: str | None = None
    surname: str | None = None
    url: str | None = None
    age: int | None = None
'''
                                         # Gemini 1 #
'''
# db/models/user.py

from pydantic import BaseModel

class User(BaseModel):
    # La clave 'id' es obligatoria en el JSON, pero puede ser null o string
    id: str | None 
    username: str
    # Corregimos el error de tipografía de 'st' a 'str'
    email: str
'''
                                       # Gemini 2 #
# Archivo: db/models/user.py
'''
from pydantic import BaseModel
# ... (otras importaciones)

class User(BaseModel):
    # ⚠️ CAMBIO CLAVE: Hacemos el ID opcional
    id: str | None = None 
    
    username: str
    email: str
    
    # Mantener los campos opcionales que corregimos antes
    name: str | None = None
    surname: str | None = None
    url: str | None = None
    age: int | None = None
'''

                                         # Gemini 3 #
'''
# Archivo: db/models/user.py

from pydantic import BaseModel

class User(BaseModel):
    # Ya está correcto: ID opcional para la creación
    id: str | None = None 
    
    username: str
    email: str
    
    name: str | None = None
    surname: str | None = None
    url: str | None = None
    age: int | None = None
    
    # 🚨 CAMBIO CLAVE: Configuración para excluir campos None en la respuesta
    class Config:
        json_encoders = {
            # Esto es necesario para manejar la serialización de ObjectId, aunque a veces no hace falta
            # Si tu profesor tiene un código similar, déjalo. Si no, puedes omitirlo.
            ObjectId: str
        }
        # 🟢 ESTO HACE QUE LOS CAMPOS CON VALOR 'None' SE OMITAN AL DEVOLVER EL JSON
        exclude_none = True
'''

                                         # Gemini 4 #

# Archivo: db/models/user.py
'''
from pydantic import BaseModel
# from bson import ObjectId # ⬅️ Si tuvieras que usarla, se importaría así

class User(BaseModel):
    # Ya está correcto: ID opcional para la creación
    id: str | None = None 
    
    username: str
    email: str
    
    name: str | None = None
    surname: str | None = None
    url: str | None = None
    age: int | None = None
    
    class Config:
        # 🚨 SOLUCIÓN: Quitamos la línea que da error
        # json_encoders = {
        #     ObjectId: str # ⬅️ ESTA LÍNEA DEBES QUITARLA O COMENTARLA
        # }
        
        # 🟢 ESTO HACE QUE LOS CAMPOS CON VALOR 'None' SE OMITAN AL DEVOLVER EL JSON
        exclude_none = True
'''

from pydantic import BaseModel, Field
from typing import Optional

# Modelo base para la entrada de datos (POST)
class User(BaseModel):
    # Nota: No incluimos 'id' porque lo genera MongoDB
    username: str
    email: str
    password: str # <-- Contraseña en texto plano para hashing en el router

# Modelo para la salida de datos de la base de datos (GET/POST/PUT Response)
# Incluye el 'id' generado por MongoDB
class UserDB(BaseModel):
    id: Optional[str] = Field(alias="_id") # Mapea el _id de MongoDB al campo 'id' de Pydantic
    username: str
    email: str
    password: str # <-- Contraseña hasheada (siempre debe estar presente)

# Modelo para la actualización de datos (PUT)
# Todos los campos son opcionales excepto el ID
class UserUpdate(BaseModel):
    id: str # <-- Este campo es obligatorio para saber a quién actualizar
    username: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None # <-- Contraseña en texto plano si se va a actualizar



