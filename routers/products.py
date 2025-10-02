                                  
'''funciona 
from fastapi import APIRouter
router = APIRouter()

  

@router.get('/products')
async def products():
#async def routers():
    return ['producto 1','producto 2','producto 3','producto 4','producto 5']
'''

'''funciona
from fastapi import FastAPI
app = FastAPI()

  

@app.get('/products')
async def products():
    return products ['producto 1','producto 2','producto 3','producto 4','producto 5']
'''

# lunes, 11 de agosto de 2025 07:42 Empiezo la hora implementando nuevo código para dejar óptimo el ‘router’-products- #

from fastapi import APIRouter

router = APIRouter(prefix='/products',tags=['products'],responses={404:{'message':'No se ha encontrado el producto'}})

products_list = ['producto 1','producto 2','producto 3','producto 4','producto 5']

  

@router.get('/')
async def products():
#async def routers():
    return products_list

@router.get('/{id}')
async def products(id:int):
    return products_list[id]
#async def routers():

    

