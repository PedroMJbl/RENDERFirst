#def user_schema(user) -> dict: 
                                      ### 07/09/2025 19:01 Aquí lo dejo por hoy ###

                                      ### lunes, 8 de septiembre de 2025 07:28 Empiezo la hora ###
'''
def user_schema(user) -> dict:
    return{'id':str (user['_id']),
           'username':user['username'],
           'email':user['email']}
'''
'''
def user_schema(user) -> dict:
    return {
        "id": str(user["_id"]),
        "username": user["username"],
        "email": user["email"],
        "name": user["name"],
        "surname": user["surname"],
        "url": user["url"],
        "age": user["age"]
    }

def users_schema(users) -> list:
    return [user_schema(user) for user in users]
'''

# Archivo: db/schemas/user.py (SOLUCIÓN)
# Comentado el código inmediatamente debajo y funciona el POST sin problema e igual que con él -martes, 30 de septiembre de 2025 05:56-
'''
def user_schema(user) -> dict:
    return {
        'id': str(user['_id']),
        'username': user['username'],
        'email': user['email'],
        
        # ⚠️ SOLUCIÓN: Usar .get() para campos que podrían faltar
        'name': user.get('name'), 
        'surname': user.get('surname'),
        'url': user.get('url'),
        'age': user.get('age') # Asumiendo estos campos son parte del schema original
    }
'''
def user_schema(user) -> dict:
    return{'id':str (user['_id']),
           'username':user['username'],
           'email':user['email']}











