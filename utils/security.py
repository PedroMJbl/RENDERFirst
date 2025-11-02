
                                            # Desde Aquí #
'''                                          
import bcrypt
from typing import Optional

# --- Configuración de Bcrypt (Coste de Hashing) ---
# 12 es el valor de coste estándar y seguro.
SALT_ROUNDS = 12 

# --- Funciones de Seguridad ---

def hash_password(password: str) -> str:
    """
    Hashea una contraseña de texto plano usando Bcrypt.
    """
    # Codifica la contraseña a bytes y genera el hash
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt(SALT_ROUNDS))
    # Decodifica el hash a string para guardarlo en la DB
    return hashed.decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifica una contraseña de texto plano contra el hash guardado.
    """
    # Si la contraseña hasheada no es un string vacío, procede a la verificación
    if hashed_password:
        return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))
    return False

def is_password_needs_rehash(hashed_password: str) -> bool:
    """
    Comprueba si el hash necesita ser regenerado (e.g., por un cambio en el coste).
    Actualmente no se usa, pero es buena práctica de seguridad.
    """
    # Por ahora, simplemente compara el coste actual con el coste estándar
    return bcrypt.checkpw.get_rounds(hashed_password.encode('utf-8')) != SALT_ROUNDS
'''
                                       # Hasta Aquí #


import bcrypt

# Función para hashear la contraseña
def hash_password(password: str) -> str:
    """
    Convierte una contraseña de texto plano en una cadena hasheada segura usando bcrypt.
    """
    # Codifica la contraseña a bytes y genera el hash con un salt aleatorio
    password_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password_bytes, salt)
    
    # Devuelve el hash decodificado a string para guardarlo en la DB
    return hashed.decode('utf-8')

# Función para verificar la contraseña (necesaria para el login, lo añadimos ahora)
def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Compara una contraseña de texto plano con un hash existente.
    """
    # Codifica las contraseñas a bytes antes de la comparación
    plain_password_bytes = plain_password.encode('utf-8')
    hashed_password_bytes = hashed_password.encode('utf-8')
    
    return bcrypt.checkpw(plain_password_bytes, hashed_password_bytes)



