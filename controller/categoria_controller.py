from bd import connect

def get_categorias():
    try:
        db = connect()
        categorias = []
        cursor = db.cursor()
        query = "SELECT * FROM categoria"
        cursor.execute(query)
        # Obtén los nombres de las columnas para utilizarlos como claves en los diccionarios
        column_names = [desc[0] for desc in cursor.description]

        for row in cursor.fetchall():
            # Crea un diccionario para cada fila
            categoria = {}
            for i, value in enumerate(row):
                categoria[column_names[i]] = value
            categorias.append(categoria)

        return categorias
    except Exception as e:
        print("Error al obtener categorias:", e)
    finally:
        if db:
            db.close()
            
def get_categoria(id):
    try:
        db = connect()  # Función para establecer la conexión a la base de datos
        cursor = db.cursor()
        query = "SELECT * FROM categoria WHERE id = %s"
        cursor.execute(query, [id,])
        categoria = cursor.fetchone()

        if categoria:
            # Obtén los nombres de las columnas para utilizarlos como claves en el diccionario
            column_names = [desc[0] for desc in cursor.description]
            
            # Crea un diccionario para representar el categoria
            categoria = {column_names[i]: value for i, value in enumerate(categoria)}
            return categoria
        else:
            return None  # En caso de que no se encuentre un categoria con el ID
    except Exception as e:
        print("Error al consultar categoria por ID:", e)
    finally:
        if db:
            db.close()

def insert_categoria(nombre):
    try:
        db = connect()  # Función para establecer la conexión a la base de datos
        cursor = db.cursor()
        query = "INSERT INTO categoria (nombre) VALUES (%s)"
        cursor.execute(query, [nombre])
        db.commit()
        return "Categoria creada con éxito"
    except Exception as e:
        db.rollback()
        print("Error al insertar categoria:", e)
    finally:
        if db:
            db.close()

def edit_categoria(id, nombre):
    try:
        db = connect()  # Función para establecer la conexión a la base de datos
        cursor = db.cursor()
        # Verificar si la categoría con el ID existe antes de eliminarla
        query_exists = "SELECT id FROM categoria WHERE id = %s"
        cursor.execute(query_exists, (id,))
        existing_category = cursor.fetchone()
        
        if existing_category:
            query = "UPDATE categoria SET nombre = %s WHERE id = %s"
            cursor.execute(query, [nombre, id])
            db.commit()
            return "Categoria editada con éxito"
        else:
            return "La categoría no existe"
    except Exception as e:
        db.rollback()
        print("Error al editar categoria:", e)
    finally:
        if db:
            db.close()

def delete_categoria(id):
    try:
        db = connect()  # Función para establecer la conexión a la base de datos
        cursor = db.cursor()
        # Verificar si la categoría con el ID existe antes de eliminarla
        query_exists = "SELECT id FROM categoria WHERE id = %s"
        cursor.execute(query_exists, (id,))
        existing_category = cursor.fetchone()
        if existing_category:
            # La categoría existe, podemos proceder con la eliminación
            query = "DELETE FROM categoria WHERE id = %s"
            cursor.execute(query, [id,])
            db.commit()
            return "Categoria eliminada con éxito"
        else:
            return "La categoría no existe"
    except Exception as e:
        db.rollback()
        print("Error al eliminar categoria:", e)
    finally:
        if db:
            db.close()
