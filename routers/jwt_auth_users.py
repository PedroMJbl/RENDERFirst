                                       # 17/08/2025 9:01 Acabo #
                                  # domingo, 17 de agosto de 2025 17:53 Empiezo la  hora #
                                       # 17/08/2025 19:32 Acabo la hora #
                                  # lunes, 18 de agosto de 2025 08:26 Empiezo la hora #

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

