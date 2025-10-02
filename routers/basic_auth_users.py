
from fastapi import APIRouter,Depends,HTTPException,status

from pydantic import BaseModel

from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm

router = APIRouter()
oauth2=OAuth2PasswordBearer(tokenUrl='login')

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
            'password': '123456'},
            
        'mouredev2':{
            'username': 'mouredev2',
            'full_name': 'Brais Moure2',  
            'mail': 'BraisMoure@mouredev2.com',
            'disabled': True,
            'password': '654321'}
    }

def search_user_db(username:str):
    if username in users_db:
        return UserDB(**users_db[username])              
  
                                          # 12/08/2025 9:02 Se acabó la hora #
                                          # martes, 12 de agosto de 2025 17:32 Empiezo la hora #
def search_user(username:str):
    if username in users_db:
        return User(**users_db[username])                                       

async def current_user(token:str=Depends(oauth2)):
    user= search_user(token)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                            detail='Credenciales de autenticación inválidas',
                            headers={'www-Authenticate':'Bearer'})
    if user.disabled:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, 
                            detail='Usuario inactivo')
    return user
                            

    
                                         

@router.post('/login')
async def login (form:OAuth2PasswordRequestForm=Depends()):
    user_db=users_db.get(form.username)
    if not user_db:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='El usuario no es correcto')
    
    user=search_user_db(form.username)
    if not form.password==user.password:
        raise HTTPException(status_code=400, detail='La contraseña no es correcta')
    
    return {'aceess_token':user.username,'token_type':'bearer'}

                       # 12/08/2025 19:36 Acabo la hora, tiene mucho código esto de la -AUTORIZACIÓN OAUTH2 #
                       # miércoles, 13 de agosto de 2025 19:41 Empiezo la hora #


@router.get('/users/me')
async def me(user:User=Depends(current_user)):
    return user 
                     # 13/08/2025 20:57 Acabo la hora, estoy implementando/copiando el código de Moure para -AUTORIZACIÓN OAUTH2-, 
                     # ya casi  se ha terminado #
                     # jueves, 14 de agosto de 2025 08:14 Empiezo la hora #
                     # 14/08/2025 9:21 Se acabó la hora #
                     # jueves, 14 de agosto de 2025 19:19 Empiezo la hora #
                     # 14/08/2025 20:23 Hasta aquí la hora de hoy #
                     # sábado, 16 de agosto de 2025 07:31 Empiezo la hora terminando de repasar/ver
                     #  el código de Moure: -AUTORIZACIÓN OAUTH2- #
                     # 16/08/2025 9:03 Acabo la hora. He terminado de ver -AUTORIZACIÓN OAUTH2- #
                     # domingo, 17 de agosto de 2025 08:34 Empiezo #

                    


