import pyodbc

def conectar_sql_server():
    try:
        conexion = pyodbc.connect(
            'DRIVER={ODBC Driver 17 for SQL Server};'
            'SERVER= server_name;'       # Servidor
            'DATABASE= DBPortafolioCursos;' # nombre de la BD
            'Trusted_Connection=yes;'
        )
        print("Conexión exitosa a la base de datos.")
        return conexion
    except pyodbc.Error as error:
        print("Error al conectar a la base de datos:", error)
        return None
    
