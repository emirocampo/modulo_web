import psycopg2
def connect():
    try:
        conn = psycopg2.connect(
            host="localhost",
            port="5432",
            user="postgres",
            password="postgres",
            database="prueba_1"
        )
        return conn
    except (Exception, psycopg2.Error) as error:
        print("Error al conectar a la base de datos:", error)
        return None