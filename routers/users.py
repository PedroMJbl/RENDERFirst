'''
#from typing import List
from fastapi import FastAPI
from pydantic import BaseModel
app = FastAPI()

# Iniciar el servidor: uvicorn users:app --reload

### miércoles, 25 de junio de 2025 17:54 Empiezo ###
# Entidad user



class User(BaseModel):
    name: str
    surname: str
    url: str
    age: int

users = [('Pedro','Moure','http:moure.dev',35)]

@app.get('/users')
async def users():
   #users = [('Pedro','Moure_Malax','http:moure.dev',35)]
   return users


   # return '¡Hola Pedro!'


### sábado, 21 de junio de 2025 19:58 Empiezo ###
### 22/06/2025 20:43 Acabo ###
### lunes, 23 de junio de 2025 07:56 Empiezo ###
### 23/06/2025 8:58 Acabo ###
### lunes, 23 de junio de 2025 19:58 Empiezo ###
### lunes, 23 de junio de 2025 19:58 Empiezo ###
### 24/06/2025 7:48 Acabo ###

### jueves, 3 de julio de 2025 19:27 Empiezo ### 03/07/2025 20:22 Acabo




@app.get('/usersjson')
async def users():

    return [{'name':'Brais','surneme':'Moure','url':'http://moure.dev','age':35},
            {'name':'Pedro','surneme':'Moure','url':'http://moure.dev','age':35},
            {'name':'Juan','surneme':'Moure','url':'http://moure.dev','age':35},
            {'name':'Mateo','surneme':'Moure','url':'http://moure.dev','age':35}]



### 25/06/2025 19:07 Acabo ##
### jueves, 26 de junio de 2025 19:09 Empiezo ###

@app.get('/New_list')
async def Usuarios():
    return [{'Pedrolas':'Brais','surneme':'Moure','url':'http://moure.dev.com'}, 
            {'MarcoAntonio':'Brais','surneme':'Malax','url':'http://moure.dev.com'}]




### 26/06/2025 20:55 Acabo ###
### viernes, 27 de junio de 2025 18:32 Empiezo ###
### 27/06/2025 20:29 Acabo ###
### sábado, 28 de junio de 2025 06:57 Empiezo ###
### 28/06/2025 8:12 Acabo ###

### domingo, 29 de junio de 2025 05:03 Empiezo ###

### 30/06/2025 7:26 Acabo ###

# miércoles, 2 de julio de 2025 18:02

### jueves, 3 de julio de 2025 06:40 Empiezo ###

### viernes, 4 de julio de 2025 05:35 Empiezo ###

# sábado, 5 de julio de 2025 07:19

                                    # lunes, 7 de julio de 2025 08:16 Empiezo #

from fastapi import FastAPI
app = FastAPI()

@app.get('/users')
async def users():
    return (users_list)



# lunes, 7 de julio de 2025 19:13 Empiezo

from fastapi import FastAPI
from pydantic import BaseModel
app = FastAPI()

@app.get('/users')
async def users():
    return (users_list)


@app.get ('/Pedro')
async def users ():
    return 'Hola Pedro!'
 
class User(BaseModel):
    name: str
    surname: str
    url: str
    age: int


### 07/07/2025 20:24 Acabo ###

### martes, 8 de julio de 2025 09:13 Empiezo ###
### 08/07/2025 10:27 Acabo ###


@app.get('/usersjson/{id}')
async def users():
    #return (users_list)

    users = filter(lambda user: user.id == id, users_list)
    try:
       return users_list (user)[0]
    except:
       return {'error': 'usuario no encontrado'}



    




    
    
    return [{'name':'Brais','surneme':'Moure','url':'http://moure.dev','age':35},
            {'name':'Pedro','surneme':'Moure','url':'http://moure.dev','age':35},
            {'name':'Juan','surneme':'Moure','url':'http://moure.dev','age':35},
            {'name':'Mateo','surneme':'Moure','url':'http://moure.dev','age':35}]
    
        


class User(BaseModel):
    id :int
    name: str
    surname: str
    url: str
    age: int

users_list = [User(id=1,name='Pedro',surname='Malax',url='https://moure.dev',age=68),
              User(id=2,name='Pedro',surname='Malax',url='https://moure.dev',age=58),
              User(id=3,name='Pedro',surname='Malax',url='https://moure.dev',age=48),
              User(id=4,name='Pedro',surname='Malax',url='https://moure.dev',age=38)]


@app.get ('/ANTONIO')
async def users ():
    return users_list
 

    #return [{'name':'Pedro','surname':'Malax','url':'https://moure.dev'},
            #{'name':'Pedro','surname':'Malax','url':'https://moure.dev'},
            #{'name':'Pedro','surname':'Malax','url':'https://moure.dev'}]
                       
                       ### martes, 8 de julio de 2025 09:13 Empiezo ###


class User(BaseModel):
    id: int
    name: str
    surname: str
    url: str
    age: int

users_list = [User(id=1, name='Pedro',surname='Malax',url='https://moure.dev',age=68),
              User(id=2, name='Pedro',surname='Malax',url='https://moure.dev',age=58),
              User(id=3, name='Pedro',surname='Malax',url='https://moure.dev',age=48),
              User(id=4, name='Pedro',surname='Malax',url='https://moure.dev',age=38)]





@app.get ('/Base/{id}')
async def user (id:int):
    users = filter(lambda user: user.id == id, users_list)
    return list (users)[0]

                    ### 09/07/2025 8:20 Acabo ###
                   ### miércoles, 9 de julio de 2025 19:48 Empiezo ###
                    ### 09/07/2025 20:51 Acabo ###
                    ### jueves, 10 de julio de 2025 07:06 implementando PATH Empiezo  ###





users_list = [User(id=1, name='Pedro',surname='Malax',url='https://moure.dev',age=68),
              User(id=2, name='Pedro',surname='Malax',url='https://moure.dev',age=58),
              User(id=3, name='Pedro',surname='Malax',url='https://moure.dev',age=48),
              User(id=4, name='Pedro',surname='Malax',url='https://moure.dev',age=38)]
              #User(id=5, name='Pablo',surname='Aguirre',url='https://aguirre.es',age=108)]

@app.get ('/user/{id}')
async def user (id:int):
    users = filter(lambda user: user.id == id, users_list)
    return list (users)[0]


@app.get ('/user/{id}')
async def user (id:int):
    users = filter(lambda user: user.id == id, users_list)
    try:
        return list (users)[0]
    except:
        return {'error':'usuario no encontrado'}

                                             ### 09/07/2025 8:20 Acabo, he cerrado el servidor y ahora no funciona ###
                                             ### viernes, 11 de julio de 2025 08:08 implementando PATH Empiezo  ###


         # PATH                              
@app.get ('/ANTONIO/{id}')
async def user (id:int):
    users = filter(lambda user: user.id == id, users_list)
    try:
        return list (users)[0]
    except:
        return {'error': 'usuario no encontrado'}
                                                   ### 09/07/2025 20:51 el próximo día QUERY Acabo ###
         # QUERY                                   ### viernes, 11 de julio de 2025 19:25 implementando PATH y QUERY Empiezo  ###
@app.get ('/ANTONIOquery/')
async def user (id:int):
    
    users = filter(lambda user: user.id == id, users_list)
    try:
        return list (users)[0]
    except:
        return {'error': 'usuario no encontrado'}    

                                         
@app.get ('/search_ANTONIO/')
async def user (id:int):
    return search_user(id)

def search_user(id:int):
    users = filter(lambda user: user.id == id, users_list)
    try:
        return list (users)[0]
    except:
        return {'error': 'usuario no encontrado'}

                                                ### 11/07/2025 20:45 Acabo ###
                                                ### sábado, 12 de julio de 2025 08:42 Empiezo ###
                     ### 12/07/2025 9:47 Acabo no carga lista MANOLO, arreglar la próxima hora ###

class Usuario(BaseModel):
    id: int
    name: str
    surname: str
    url: str
    age: int
    

@app.get ('/MANOLO/{id}')
async def Lista_usuarios (id:int):
    usuarios = filter(lambda usuario: usuario.id == id, Lista_usuarios)
    try:
        return list (usuarios)[0]
    except: 
        return {'error': 'usuario no encontrado'}        
    



    

Lista_usuarios = [User(id=6, name='Pedro',surname='Malax',url='https://moure.dev',age=68),
                  User(id=7, name='Pedro',surname='Malax',url='https://moure.dev',age=58),
                  User(id=8, name='Pedro',surname='Malax',url='https://moure.dev',age=48),
                  User(id=9, name='Pedro',surname='Malax',url='https://moure.dev',age=38)]

                                    ### domingo, 13 de julio de 2025 06:17 Empiezo ###

@app.get ('/Mi_lista/{id}')
async def Mi_lista_usuarios (id:int):
    usuarios = filter(lambda usuario: usuario.id == id, Mi_lista_usuarios)
    try:
        return list (usuarios)[0]
    except: 
        return {'error': 'usuario no encontrado'}   

Mi_lista_usuarios = [User(id=10, name='Pedro',surname='Malax',url='https://moure.dev',age=78),
                  User(id=11, name='Pedro',surname='Malax',url='https://moure.dev',age=88),
                  User(id=12, name='Pedro',surname='Malax',url='https://moure.dev',age=98),
                  User(id=13, name='Pedro',surname='Malax',url='https://moure.dev',age=108)]

                                           
                                            ### domingo, 13 de julio de 2025 07:17 Acabo ###
                                            ### domingo, 13 de julio de 2025 19:20 Empiezo ###

                                             # POST #
@app.post('/JORGE/')
async def Lista_usuarios(usuario:user):
    #usuarios=filter(lambda usuario:usuario.id==id, Lista_usuarios)
    if type(search_usuario(usuario.id))==usuario:
        return{'error':'El usuario ya existe'}
    else:
        Lista_usuarios.append(user)


def search_usuario(id:int):
    usuarios=filter(lambda usuario:usuario.id==id,Lista_usuarios)
    try:
        return list(usuarios)[0]
    except:
        return{'Error':'El usuario ya existe'}
    
    Lista_usuarios = [User(id=6, name='Pedro',surname='Malax',url='https://moure.dev',age=68),
                  User(id=7, name='Pedro',surname='Malax',url='https://moure.dev',age=58),
                  User(id=8, name='Pedro',surname='Malax',url='https://moure.dev',age=48),
                  User(id=9, name='Pedro',surname='Malax',url='https://moure.dev',age=38)]
                                                ### domingo, 13/07/2025 20:37 Acabo ### el POST no funciona
                                                ### martes, 15 de julio de 2025 08:35 Empiezo ###

#@app.post('/user/')
#async def user(user:User):
    #users_list.append(user)
                                              ### Lúnes 14/07/2025 9:05 Acabo ###
                                              ### domingo, 13 de julio de 2025 19:20 Empiezo ###
                                                                                           
#from fastapi import FastAPI, Request
#from pydantic import BaseModel

# Define el modelo de datos que se espera recibir en el cuerpo de la solicitud
#class Item(BaseModel):
 #   nombre: str
  #  precio: float
   # disponible: bool

class Item (BaseModel):
    id: int
    name: str
    surname: str
    url: str
    age: int

app = FastAPI()

@app.post("/items/{id}")
#async def Mi_lista_usuarios (id:int):
async def item(id:int):
    return {
        "mensaje": "Item creado exitosamente",
        "datos": item
    }
items = item     [user(id=10, name='Pedro',surname='Malax',url='https://moure.dev',age=78),
                  User(id=11, name='Pedro',surname='Malax',url='https://moure.dev',age=88),
                  User(id=12, name='Pedro',surname='Malax',url='https://moure.dev',age=98),
                  User(id=13, name='Pedro',surname='Malax',url='https://moure.dev',age=108)]


                             ### 15/07/2025 9:40  Acabo ### Sigo sin implementar -POST-
                             ### miércoles, 16 de julio de 2025 09:06 Empiezo ###

    @app.post ('/Mi_lista/{id}')
async def Mi_lista_usuarios (id:int):
    usuarios = filter(lambda usuario: usuario.id == id, Mi_lista_usuarios)
    try:
        return list (usuarios)[0]
    except: 
        return {'error': 'usuario no encontrado'}


@app.post ('/ANTONIO/')
async def user (user:User):
    if type(search_user.id)==User:
        return{'error':'El usuario ya existe'}
    else:
        users_list.append(user)
def search_user(ide:int):
    
    

        users = filter(lambda user: user.id == id, users_list)
        try:
         return list (users)[0]
        except:
         return {'error': 'usuario no encontrado'}
        
        #len(users_list)

                                        ### 15/07/2025 9:40  Acabo ### No he terminado de implementar -POST-
                                        ### jueves, 17 de julio de 2025 06:37 Empiezo ###

              #User(id=5, name='Pablo',surname='Aguirre',url='https://aguirre.es',age=108)]

              ### 17/07/2025 7:50 Acabo ### Sigo sin ver resultados en el -POST-
              ### viernes, 18 de julio de 2025 08:49 Empiezo ###
              ### 18/07/2025 9:51 Acabo ### No he terminado de implementar -POST-
              ### sábado, 19 de julio de 2025 05:53 Empiezo ###
              ### 19/07/2025 7:45  Acabo ### Sigo sin implementar -POST- 
              ### lunes, 21 de julio de 2025 ###

@app.get('/user/')
async def user(id:int):
    return search_user(id)

@app.post('/user/')
async def user(user:User):
    if type(search_user(user.id))==User:
        return {'Error':'El usuario ya existe'}
    else:
        users_list.append (user)


def search_user(id:int):
    users=filter (lambda user:user.id==id,users_list)
    try:
        return list(users)[0]
    except :
        {'Error':'No se ha encontrado el usuario'}

                                ### martes, 22 de julio de 2025 06:38 Empiezo ###

@app.get("/Marc")
async def root():
    return 'hola buenos días'

@app.post ('/ANTONIO/')
async def user (user:User):
    if type(search_user.id)==User:
        return{'error':'El usuario ya existe'}
    else:
        users_list.append(user)
def search_user(ide:int):
    users = filter(lambda user: user.id == id, users_list)
    try:
         return list (users)[0]
    except:
         return {'error': 'usuario no encontrado'}
        
        #len(users_list)

                                            ### jueves, 24 de julio de 2025 07:48 Empiezo ###


@app.get ('/user/')
async def user (id:int):
        return search_user(id)
    # PARA TERMINAR DE IMPLEMENTAR jueves, 24 de julio de 2025 08:50 Empiezo
@app.get ('/user/{id}')
async def user (id:int):
        return search_user(id)

@app.post ('/user/')
async def user (user:User):
    if type(search_user.id)==User:
        return{'error':'El usuario ya existe'}
    else:
        users_list.append(user)

def search_user(ide:int):
    users = filter(lambda user: user.id == id, users_list)
    try:
         return list (users)[0]
    except:
        return {'error': 'usuario no encontrado'}
   
users_list = [User(id=1, name='Pedro',surname='Malax',url='https://moure.dev',age=68),
              User(id=2, name='Pedro',surname='Malax',url='https://moure.dev',age=58),
              User(id=3, name='Pedro',surname='Malax',url='https://moure.dev',age=48),
              User(id=4, name='Pedro',surname='Malax',url='https://moure.dev',age=38)]

@app.get ('/JUEVES/{id}')
async def user (id:int):
        return users_list

@app.post ('/JUEVES/')
async def user (user:User):
    if type(search_user.id)==User:
        return{'error':'El usuario ya existe'}
    else:
        users_list.append(user)
'''
                                    ### DESDE EL PRINCIPIO DE LOS TIEMPOS ###
                                    ### viernes, 25 de julio de 2025 07:09 Empiezo ###
                                    ### domingo, 27 de julio de 2025 18:18 Empiezo ###



from fastapi import APIRouter ,HTTPException
#from fastapi import FastAPI
#app = FastAPI()
from pydantic import BaseModel
router = APIRouter()



#@app.get('/usersjson')
#async def usersjson():
    #return [{'name':'Brais','surneme':'Moure','url':'http://moure.dev','age':35},
            #{'name':'Pedro','surneme':'Moure','url':'http://moure.dev','age':35},
            #{'name':'Juan','surneme':'Moure','url':'http://moure.dev','age':35},
            #{'name':'Mateo','surneme':'Moure','url':'http://moure.dev','age':35}]
'''
class User(BaseModel):
    name: str
    surname: str
    url: str
    age: int


users_list= [User (name='Brais', surname='Moure', url='http://moure.dev',age=35),
              User (name='Brais', surname='Moure', url='http://moure.dev',age=35),
              User (name='Brais', surname='Moure', url='http://moure.dev',age=35),
              User (name='Brais', surname='Moure', url='http://moure.dev',age=35),
              User (name='Pedrolas', surname='Malaleche', url='http://Malaleche.com',age=25)]
'''
'''
@app.get('/usersclass')
async def usersclass():
    #return User(name='Brais',surnme='Moure',url='http://Moure.dev', age=35)
    return [{'name':'Brais','surneme':'Moure','url':'http://moure.dev','age':35}]

                                       ### lunes, 28 de julio de 2025 06:09 Empiezo ###

router.get('/usersjson')
async def usersjson():
    return [{'name':'Brais','surneme':'Moure','url':'http://moure.dev','age':35},
            {'name':'Pedro','surneme':'Moure','url':'http://moure.dev','age':35},
            {'name':'Juan','surneme':'Moure','url':'http://moure.dev','age':35},
            {'name':'Mateo','surneme':'Moure','url':'http://moure.dev','age':35}]
'''
                               # BaseModel devuelve -users_list- en json perfecto
@router.get('/users')
async def users():
    return users_list
    #return users_list

@router.get('/users/{id}')
async def users(id:int):
    return search_user (id)

                                        ### 28/07/2025 7:36 Acabo ###
                                        ### martes, 29 de julio de 2025 07:55 Empiezo ###

class User(BaseModel):
    id:int
    name: str
    surname: str
    url: str
    age: int

users_list=  [User (id=1,name='Brais', surname='Moure', url='http://moure.dev',age=35),
              User (id=2,name='Peter', surname='Moure', url='http://moure.dev',age=35),
              User (id=3,name='Manolo', surname='Moure', url='http://moure.dev',age=35),
              User (id=4,name='Jorge', surname='Moure', url='http://moure.dev',age=35),
              User (id=5,name='Miguelón', surname='Moure', url='http://moure.dev',age=35)]  
   
'''
@app.get('/user/{id}')
async def user(id:int):
    users = filter (lambda user: user.id == id, users_list)
    return list (users)[0]      ### 29/07/2025 8:54 Acabo ###
'''                        ### miércoles, 30 de julio de 2025 08:05 Empiezo ###

# Con PATH

@router.get('/user/{id}')

async def user(id:int):
    #return users_list

    return search_user (id)

'''    
    users = filter(lambda user: user.id == id, users_list)
    try:
        return list(users)[0]  #users_list [0]
    except:
        return ({'Error':'No se ha encontrado el usuario'})
'''     
    #return search_user (id) # tengo que definir esta función, para la query también.
    
#Con QUERY   
@router.get('/user/')
async def user(id:int):
    return search_user (id)

'''
    users = filter (lambda user: user.id == id, users_list)
    try:
        return list(users)[0]
    except:
        return ({'Error':'No se ha encontrado el usuario'})
 '''
                                        ### 30/07/2025 9:08 Acabo ###
                                        ### miércoles, 30 de julio de 2025 17:51 Empiezo ###

                                                         ### POST ###
                                                   
@router.post('/user/')
async def user(user:User):
    if type(search_user(user.id))==User:    
    
       return{'error': 'El ususario ya existe'}
    else:
        users_list.append(user)



def search_user(id:int):
    users = filter (lambda user: user.id == id, users_list)
    try:
        return list(users)[0]
    except:
        return {'Error':'No se ha encontrado el usuario'}

    
                                                    
   





    
                                       ### jueves, 31 de julio de 2025 07:07 Empiezo la hora ###
                                       ### viernes, 1 de agosto de 2025 06:20 Empiezo la hora ###
                                       ### sábado, 2 de agosto de 2025 08:07 Empiezo ###
#router.get ('/users')
#async def users():
    #return users_list
'''   
@app.post('/viernes/',status_code=201)
async def user(user:User):
    if type(search_user(user.id))==User:    
    
       return{'error': 'El ususario ya existe'}
    else:
        users_list.append(user)
        return user
 '''                                     
                                      ### 02/08/2025 9:11 Acabo ###
                                      ### sábado, 2 de agosto de 2025 18:56 Empiezo la hora ###
                                                        
                                                        # PUT #

@router.put('/user/')
async def user(user:User):
    found=False
    for index, saved_user in enumerate(users_list):
        if saved_user.id == user.id:
           users_list[index]=user
           found=True
    if not found:
        return {'Error': 'No se ha actualizado el usuario'} 
    else:
        return user

    
                                      ### domingo, 3 de agosto de 2025 07:29 Empiezo la hora ###

@router.delete('/user/{id}')
async def user(id:int):
    found=False
    for index, saved_user in enumerate(users_list):
        if saved_user.id == id:
            del users_list[index]
            found=True
    if not found:
           return {'Error': 'No se ha eliminado el usuario'} 
    return user
                                      
                                      ### martes, 5 de agosto de 2025 06:21 Empiezo la hora ###

                                                     # HTTP STATUS CODE #
'''
@app.post('/viernes/',status_code=201)
async def user(user:User):
    if type(search_user(user.id))==User:    
    
       return{'error': 'El ususario ya existe'}
    else:
        users_list.append(user)
        return user
'''
                                                     ### 05/08/2025 7:36 Acabo ###
                                                     ### martes, 5 de agosto de 2025 19:58 Empiezo la hora ###


@router.post('/viernes/',response_model=User,status_code=201)
async def user(user:User):
    if type(search_user(user.id))==User:
        raise HTTPException(status_code=404, detail='El usuario ya existe')        
      
       
    users_list.append(user)
    return user
                                                          ### 05/08/2025 20:55 Acabo ###
                                                          ### miércoles, 6 de agosto de 2025 07:30 Empiezo la hora ###
                                                          ### 06/08/2025 8:32 Acabo ###

                                                          ### miércoles, 6 de agosto de 2025 19:12 Empiezo la hora ###
                                                          ### 06/08/2025 20:26 Acabo la hora, ha petado todo ###


@router.get('/usersjson')
async def users():

    return [{'name':'Brais','surneme':'Moure','url':'http://moure.dev','age':35},
            {'name':'Pedro','surneme':'Moure','url':'http://moure.dev','age':35},
            {'name':'Juan','surneme':'Moure','url':'http://moure.dev','age':35},
            {'name':'Mateo','surneme':'Moure','url':'http://moure.dev','age':35}]                                  
                                                  
                                       
                                        
