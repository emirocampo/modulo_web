from bd import connect

def get_inventarios():
    try:
        db = connect()
        inventarios = []
        cursor = db.cursor()
        query = "SELECT * FROM inventario"
        cursor.execute(query)
        # Obtén los nombres de las columnas para utilizarlos como claves en los diccionarios
        column_names = [desc[0] for desc in cursor.description]

        for row in cursor.fetchall():
            # Crea un diccionario para cada fila
            inventario = {}
            for i, value in enumerate(row):
                inventario[column_names[i]] = value
            inventarios.append(inventario)

        return inventarios
    except Exception as e:
        print("Error al obtener inventarios: ", e)
    finally:
        if db:
            db.close()
            
def get_inventario(id):
    try:
        db = connect()  # Función para establecer la conexión a la base de datos
        cursor = db.cursor()
        query = "SELECT * FROM inventario WHERE id = %s"
        cursor.execute(query, [id,])
        inventario = cursor.fetchone()

        if inventario:
            # Obtén los nombres de las columnas para utilizarlos como claves en el diccionario
            column_names = [desc[0] for desc in cursor.description]
            
            # Crea un diccionario para representar el inventario
            inventario = {column_names[i]: value for i, value in enumerate(inventario)}
            return inventario
        else:
            return None  # En caso de que no se encuentre un inventario con el ID
    except Exception as e:
        print("Error al consultar inventario por ID: ", e)
    finally:
        if db:
            db.close()

def insert_inventario(stock, id_producto, id_proveedor, fecha_registro, fecha_vencimiento):
    try:
        db = connect()  # Función para establecer la conexión a la base de datos
        cursor = db.cursor()
        query = "INSERT INTO inventario (stock, id_producto, id_proveedor, fecha_registro, fecha_vencimiento) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(query, [stock, id_producto, id_proveedor, fecha_registro, fecha_vencimiento])
        db.commit()
        return "Inventario creado con éxito"
    except Exception as e:
        db.rollback()
        print("Error al insertar inventario: ", e)
    finally:
        if db:
            db.close()

def edit_inventario(id, stock, id_producto, id_proveedor, fecha_registro, fecha_vencimiento):
    try:
        db = connect()  # Función para establecer la conexión a la base de datos
        cursor = db.cursor()
        # Verificar si la inventario con el ID existe antes de eliminarlo
        query_exists = "SELECT id FROM inventario WHERE id = %s"
        cursor.execute(query_exists, (id,))
        existing_inventario = cursor.fetchone()

        if existing_inventario:
            query = "UPDATE inventario SET stock = %s, id_producto = %s, id_proveedor = %s, fecha_registro = %s, fecha_vencimiento = %s WHERE id = %s"
            cursor.execute(query, [stock, id_producto, id_proveedor, fecha_registro, fecha_vencimiento, id])
            db.commit()
            return "Inventario editado con éxito"
        else:
            return "El inventario no existe"
    except Exception as e:
        db.rollback()
        print("Error al editar inventario: ", e)
    finally:
        if db:
            db.close()
