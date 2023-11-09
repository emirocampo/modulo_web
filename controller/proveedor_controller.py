from db import connect

def get_proveedores():
    try:
        db = connect()
        proveedores = []
        cursor = db.cursor()
        query = "SELECT * FROM proveedor"
        cursor.execute(query)
        # Obtén los nombres de las columnas para utilizarlos como claves en los diccionarios
        column_names = [desc[0] for desc in cursor.description]

        for row in cursor.fetchall():
            # Crea un diccionario para cada fila
            proveedor = {}
            for i, value in enumerate(row):
                proveedor[column_names[i]] = value
            proveedores.append(proveedor)

        return proveedores
    except Exception as e:
        print("Error al obtener proveedores:", e)
    finally:
        if db:
            db.close()
            
def get_proveedor(id):
    try:
        db = connect()  # Función para establecer la conexión a la base de datos
        cursor = db.cursor()
        query = "SELECT * FROM proveedor WHERE id = %s"
        cursor.execute(query, [id,])
        proveedor = cursor.fetchone()

        if proveedor:
            # Obtén los nombres de las columnas para utilizarlos como claves en el diccionario
            column_names = [desc[0] for desc in cursor.description]
            
            # Crea un diccionario para representar el proveedor
            proveedor = {column_names[i]: value for i, value in enumerate(proveedor)}
            return proveedor
        else:
            return None  # En caso de que no se encuentre un proveedor con el ID
    except Exception as e:
        print("Error al consultar proveedor por ID:", e)
    finally:
        if db:
            db.close()

def insert_proveedor(nombre):
    try:
        db = connect()  # Función para establecer la conexión a la base de datos
        cursor = db.cursor()
        query = "INSERT INTO proveedor (nombre) VALUES (%s)"
        cursor.execute(query, [nombre])
        db.commit()
        return "Proveedor creado con éxito"
    except Exception as e:
        db.rollback()
        print("Error al insertar proveedor:", e)
    finally:
        if db:
            db.close()

def edit_proveedor(id, nombre):
    try:
        db = connect()  # Función para establecer la conexión a la base de datos
        cursor = db.cursor()
        # Verificar si la categoría con el ID existe antes de eliminarla
        query_exists = "SELECT id FROM proveedor WHERE id = %s"
        cursor.execute(query_exists, (id,))
        existing_proveedor = cursor.fetchone()

        if existing_proveedor:
            query = "UPDATE proveedor SET nombre = %s WHERE id = %s"
            cursor.execute(query, [nombre, id])
            db.commit()
            return "Proveedor editado con éxito"
        else:
            return "El proveedor no existe"
    except Exception as e:
        db.rollback()
        print("Error al editar proveedor:", e)
    finally:
        if db:
            db.close()

def delete_proveedor(id):
    try:
        db = connect()  # Función para establecer la conexión a la base de datos
        cursor = db.cursor()
        # Verificar si la proveedor con el ID existe antes de eliminarlo
        query_exists = "SELECT id FROM proveedor WHERE id = %s"
        cursor.execute(query_exists, (id,))
        existing_proveedor = cursor.fetchone()

        if existing_proveedor:
            query = "DELETE FROM proveedor WHERE id = %s"
            cursor.execute(query, [id,])
            db.commit()
            return "Proveedor eliminado con éxito"
        else:
            return "El proveedor no existe"
    except Exception as e:
        db.rollback()
        print("Error al eliminar proveedor:", e)
    finally:
        if db:
            db.close()
