from db import connect

def get_usuario(email,password):
    try:
        db = connect()  # Función para establecer la conexión a la base de datos
        cursor = db.cursor()
        query = "SELECT * FROM usuarios WHERE correo = %s AND contraseña = %s"
        cursor.execute(query, [email,password])
        usuario = cursor.fetchall()
        print(f"usuario: {usuario}")

        if usuario:            
            # devuelvo la tupla
            return True
        else:
            return False  # En caso de que no se encuentre un usuario con el email y password
    except Exception as e:
        print("Error al consultar usuarios", e)
    finally:
        if db:
            db.close()