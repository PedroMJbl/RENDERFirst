from pymongo import MongoClient

# --- CONFIGURACIÓN ---
# 1. Reemplaza con tu cadena de conexión de Atlas (¡no olvides el usuario y la contraseña!)
#MONGO_URI = "mongodb+srv://Pedro_db_user:ArhjnM57i@cluster-de-pedro-atlas.w5yrex6.mongodb.net/" # Para Mongo-ATLAS
MONGO_URI = "mongodb+srv://fastapi_db_ATLAS:ArhjnM57i@cluster-de-pedro-atlas.w5yrex6.mongodb.net/" # Para Mongo-ATLAS

# 2. Define los nombres de las bases de datos
OLD_DB_NAME = "fastapi_db"
NEW_DB_NAME = "fastapi_db_ATLAS"
# ---------------------

def rename_database(uri, old_name, new_name):
    """Clona todas las colecciones de la DB antigua a una DB nueva y luego elimina la antigua."""
    
    try:
        # 1. Conexión a MongoDB Atlas
        client = MongoClient(uri)
        print("✅ Conexión a MongoDB Atlas exitosa.")

        # Obtener referencias a las bases de datos
        db_old = client[old_name]
        db_new = client[new_name]

        # 2. Obtener la lista de colecciones de la DB antigua
        collection_names = db_old.list_collection_names()
        
        if not collection_names:
            print(f"⚠️ La DB antigua '{old_name}' no contiene colecciones. No hay nada que renombrar.")
            client.close()
            return

        print(f"Encontradas {len(collection_names)} colecciones para copiar...")

        # 3. Copiar cada colección a la DB nueva
        for coll_name in collection_names:
            print(f"   - Copiando colección: '{coll_name}'...")
            
            # Usar la operación de agregación con $out para copiar la colección completa
            # $out es la forma más eficiente y moderna de hacer esto.
            pipeline = [
                {"$match": {}}, # Selecciona todos los documentos
                {"$out": {"db": new_name, "coll": coll_name}} # Envía la salida a la nueva DB/Colección
            ]
            
            # Ejecutar la agregación en la colección antigua
            db_old[coll_name].aggregate(pipeline)
            print(f"     -> Copia de '{coll_name}' completa.")
            
        print(f"\n🎉 ¡Copia completada! La DB '{old_name}' ha sido clonada como '{new_name}'.")

        # 4. (Opcional pero crucial) Eliminar la Base de Datos Antigua
        confirm = input(f"\n¿Estás SEGURO de querer ELIMINAR la DB antigua '{old_name}'? Escribe 'SI' para confirmar: ")

        if confirm.upper() == "SI":
            client.drop_database(old_name)
            print(f"🗑️ La Base de Datos antigua '{old_name}' ha sido ELIMINADA exitosamente.")
        else:
            print(f"❌ La DB antigua '{old_name}' NO fue eliminada. Por favor, revísala manualmente.")

    except Exception as e:
        print(f"\n🚫 ¡Ocurrió un error! {e}")
    finally:
        # 5. Cerrar la conexión
        client.close()
        print("Cerrando conexión.")


if __name__ == "__main__":
    rename_database(MONGO_URI, OLD_DB_NAME, NEW_DB_NAME)