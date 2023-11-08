from bd import connect

def get_productos():
    try:
        db = connect()
        productos = []
        cursor = db.cursor()
        query = "SELECT * FROM producto"
        cursor.execute(query)
        # Obtén los nombres de las columnas para utilizarlos como claves en los diccionarios
        column_names = [desc[0] for desc in cursor.description]

        for row in cursor.fetchall():
            # Crea un diccionario para cada fila
            producto = {}
            for i, value in enumerate(row):
                producto[column_names[i]] = value
            productos.append(producto)

        return productos
    except Exception as e:
        print("Error al obtener productos: ", e)
    finally:
        if db:
            db.close()
            
def get_producto(id):
    try:
        db = connect()  # Función para establecer la conexión a la base de datos
        cursor = db.cursor()
        query = "SELECT * FROM producto WHERE id = %s"
        cursor.execute(query, [id,])
        producto = cursor.fetchone()

        if producto:
            # Obtén los nombres de las columnas para utilizarlos como claves en el diccionario
            column_names = [desc[0] for desc in cursor.description]
            
            # Crea un diccionario para representar el producto
            producto = {column_names[i]: value for i, value in enumerate(producto)}
            return producto
        else:
            return None  # En caso de que no se encuentre un producto con el ID
    except Exception as e:
        print("Error al consultar producto por ID: ", e)
    finally:
        if db:
            db.close()

def insert_producto(nombre, precio, id_categoria, id_proveedor, fecha_creacion):
    try:
        db = connect()  # Función para establecer la conexión a la base de datos
        cursor = db.cursor()
        query = "INSERT INTO producto (nombre, precio, id_categoria, id_proveedor, fecha_creacion) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(query, [nombre, precio, id_categoria, id_proveedor, fecha_creacion])
        db.commit()
        return "Producto creado con éxito"
    except Exception as e:
        db.rollback()
        print("Error al insertar producto: ", e)
    finally:
        if db:
            db.close()

def edit_producto(id, nombre, precio, id_categoria, id_proveedor, fecha_creacion):
    try:
        db = connect()  # Función para establecer la conexión a la base de datos
        cursor = db.cursor()
        # Verificar si la producto con el ID existe antes de eliminarlo
        query_exists = "SELECT id FROM producto WHERE id = %s"
        cursor.execute(query_exists, (id,))
        existing_producto = cursor.fetchone()

        if existing_producto:
            query = "UPDATE producto SET nombre = %s, precio = %s, id_categoria = %s, id_proveedor = %s, fecha_creacion = %s WHERE id = %s"
            cursor.execute(query, [nombre, precio, id_categoria, id_proveedor, fecha_creacion, id])
            db.commit()
            return "Producto editado con éxito"
        else:
            return "El producto no existe"
    except Exception as e:
        db.rollback()
        print("Error al editar producto: ", e)
    finally:
        if db:
            db.close()

def delete_producto(id):
    try:
        db = connect()  # Función para establecer la conexión a la base de datos
        cursor = db.cursor()
        # Verificar si la producto con el ID existe antes de eliminarlo
        query_exists = "SELECT id FROM producto WHERE id = %s"
        cursor.execute(query_exists, (id,))
        existing_producto = cursor.fetchone()

        if existing_producto:
            query = "DELETE FROM producto WHERE id = %s"
            cursor.execute(query, [id,])
            db.commit()
            return "Producto eliminado con éxito"
        else:
            return "El producto no existe"
    except Exception as e:
        db.rollback()
        print("Error al eliminar producto: ", e)
    finally:
        if db:
            db.close()
