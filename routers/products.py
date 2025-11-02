                                  
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
'''
'''
from fastapi import APIRouter, HTTPException, status
from typing import Optional, List # Necesario para el tipado correcto
from pydantic import BaseModel # Necesario para la validación de objetos

# --- Modelo de Producto (Obligatorio para el tipado y búsqueda) ---
class Product(BaseModel):
    id: int
    name: str

# --- Inicialización y Datos ---

router = APIRouter(prefix='/products', tags=['products'], responses={404: {'message': 'Producto no encontrado'}})

# La lista de productos debe contener objetos Product, no strings simples
products_list = [
    Product(id=1, name='producto 1'),
    Product(id=2, name='producto 2'),
    Product(id=3, name='producto 3'),
    Product(id=4, name='producto 4'),
    Product(id=5, name='producto 5')
]

# --- Función Auxiliar de Búsqueda Segura ---
def search_product_by_id(id: int):
    """Busca el producto por el valor del atributo id de forma segura."""
    # next() busca el primer elemento que cumpla la condición. Si no encuentra nada, devuelve None.
    return next((p for p in products_list if p.id == id), None)

# --- Ruta GET: Implementa la Búsqueda por Query Parameter (?id=) ---
# Acepta opcionalmente 'id' de la query string o devuelve la lista completa.
@router.get('/', response_model=List[Product] | Product)
async def get_products(id: Optional[int] = None):
    
    # 1. Si se proporciona ID en la query string (?id=3)
    if id is not None:
        product = search_product_by_id(id)
        if product:
            return product
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Producto con ID {id} no encontrado"
            )

    # 2. Si NO se proporciona ID, devuelve la lista completa
    return products_list

# --- Ruta GET: Implementa la Búsqueda por Path Parameter (/{id}) ---
@router.get('/{id}', response_model=Product)
async def get_product_by_path(id: int):
    """
    Busca un producto usando el Path Parameter. 
    Se utiliza la búsqueda segura para evitar errores de índice.
    """
    product = search_product_by_id(id)
    
    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Producto con ID {id} no encontrado"
        )
    
    return product

'''
'''
                                       # Este código es el que funciona como el Gemini (mejor) 7 de octubre de 2025 #
from fastapi import APIRouter, HTTPException, status
from typing import Optional, List # Todavía necesitamos estos para el tipado

# --- Inicialización y Datos (Lista de Strings) ---

router = APIRouter(prefix='/products', tags=['products'], responses={404: {'message': 'Producto no encontrado'}})

# La lista de productos es ahora una lista simple de strings (índice 0, 1, 2, 3, 4)
products_list = ['producto 1','producto 2','producto 3','producto 4','producto 5']

# --- Función Auxiliar de Búsqueda Segura por ÍNDICE ---
def search_product_by_index(index: int):
    """
    Busca el producto por el índice de la lista (no por un atributo ID).
    El índice debe estar dentro de los límites de la lista.
    """
    if 0 <= index < len(products_list):
        return products_list[index]
    return None # Devuelve None si el índice está fuera de rango

# --- Ruta GET: Implementa la Búsqueda por Query Parameter (?id=) ---
# Endpoint: GET /products/?id=3 -> Devuelve 'producto 3'
@router.get('/')
# response_model eliminado para devolver un string o lista de strings
async def get_products(id: Optional[int] = None):
    
    # 1. Si se proporciona ID en la query string (?id=3)
    if id is not None:
        # Aquí es donde aplicamos la lógica de tu profesor. 
        # Si pides ID=3, en una lista de productos (índice 0, 1, 2, 3) 
        # tienes que devolver el elemento en el índice (ID - 1) para que ID=1 devuelva el índice 0.
        index_to_search = id - 1 
        
        product_name = search_product_by_index(index_to_search)
        
        if product_name:
            # Devuelve solo el string (e.g., "producto 3")
            return product_name 
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Producto con ID {id} no encontrado"
            )

    # 2. Si NO se proporciona ID, devuelve la lista completa de strings
    return products_list

# --- Ruta GET: Implementa la Búsqueda por Path Parameter (/{id}) ---
# Endpoint: GET /products/3 -> Devuelve 'producto 3'
@router.get('/{id}')
async def get_product_by_path(id: int):
    """
    Busca un producto usando el Path Parameter, ajustando el ID a índice.
    """
    # Ajustamos ID a índice (ID 1 es el índice 0)
    index_to_search = id - 1
    product_name = search_product_by_index(index_to_search)
    
    if product_name is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Producto con ID {id} no encontrado"
        )
    
    return product_name # Devuelve solo el string
'''
                              # Este código es el que funciona como el de Moure 7 de octubre de 2025 #
from fastapi import APIRouter, HTTPException, status
from typing import Optional, List # Todavía necesitamos estos para el tipado

# --- Inicialización y Datos (Lista de Strings) ---

router = APIRouter(prefix='/products', tags=['products'], responses={404: {'message': 'Producto no encontrado'}})

# La lista de productos es ahora una lista simple de strings (índice 0, 1, 2, 3, 4)
products_list = ['producto 1','producto 2','producto 3','producto 4','producto 5']

# --- Función Auxiliar de Búsqueda Segura por ÍNDICE ---
def search_product_by_index(index: int):
    """
    Busca el producto por el índice de la lista. 
    Asegura que el índice esté dentro de los límites.
    """
    # Si 0 <= index (positivo o cero) Y index es menor que la longitud de la lista.
    if 0 <= index < len(products_list):
        return products_list[index]
    return None # Devuelve None si el índice está fuera de rango

# --- Ruta GET: Implementa la Búsqueda por Query Parameter (?id=) ---
# Endpoint: GET /products/?id=0 -> Devuelve 'producto 1'
@router.get('/')
# response_model eliminado para devolver un string o lista de strings
async def get_products(id: Optional[int] = None):
    
    # 1. Si se proporciona ID en la query string (?id=0)
    if id is not None:
        # Usamos el ID directamente como índice (ID 0 es índice 0)
        index_to_search = id 
        
        product_name = search_product_by_index(index_to_search)
        
        if product_name:
            # Devuelve solo el string (e.g., "producto 1" si id=0)
            return product_name 
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Producto con ID {id} no encontrado"
            )

    # 2. Si NO se proporciona ID, devuelve la lista completa de strings
    return products_list

# --- Ruta GET: Implementa la Búsqueda por Path Parameter (/{id}) ---
# Endpoint: GET /products/0 -> Devuelve 'producto 1'
@router.get('/{id}')
async def get_product_by_path(id: int):
    """
    Busca un producto usando el Path Parameter. El ID se usa directamente como índice.
    """
    # Usamos el ID directamente como índice (ID 0 es índice 0)
    index_to_search = id
    product_name = search_product_by_index(index_to_search)
    
    if product_name is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Producto con ID {id} no encontrado"
        )
    
    return product_name # Devuelve solo el string


