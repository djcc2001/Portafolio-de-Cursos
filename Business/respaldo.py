import os, zipfile, shutil
from datetime import datetime
from flask import current_app
from Data.conexion import conectar_sql_server

def crear_respaldo_zip(id_usuario):
    fecha = datetime.now().strftime('%Y%m%d_%H%M%S')
    nombre_zip = f"backup_{fecha}.zip"
    ruta_backups = os.path.join(current_app.root_path, 'backups')
    os.makedirs(ruta_backups, exist_ok=True)
    ruta_zip = os.path.join(ruta_backups, nombre_zip)

    carpetas = ['public/materiales', 'public/silabos', 'public/trabajos_estudiantiles']
    with zipfile.ZipFile(ruta_zip, 'w') as zipf:
        for carpeta in carpetas:
            carpeta_absoluta = os.path.join(current_app.root_path, carpeta)
            for folder, _, files in os.walk(carpeta_absoluta):
                for file in files:
                    ruta_completa = os.path.join(folder, file)
                    ruta_relativa = os.path.relpath(ruta_completa, current_app.root_path)
                    zipf.write(ruta_completa, ruta_relativa)

    tamaño_mb = os.path.getsize(ruta_zip) / (1024 * 1024)

    conn = conectar_sql_server()
    cursor = conn.cursor()
    cursor.execute("SELECT ISNULL(MAX(IdBackup), 0) + 1 FROM BackupRegistro")
    nuevo_id = cursor.fetchone()[0]
    cursor.execute("""
        INSERT INTO BackupRegistro (IdBackup, NombreArchivo, RutaArchivo, FechaBackup, TamañoMB, IdUsuario)
        VALUES (?, ?, ?, GETDATE(), ?, ?)
    """, (nuevo_id, nombre_zip, ruta_zip, tamaño_mb, id_usuario))
    conn.commit()
    cursor.close()
    conn.close()

    return True, nombre_zip

def restaurar_desde_zip(nombre_zip):
    ruta_zip = os.path.join(current_app.root_path, 'backups', nombre_zip)
    if not os.path.exists(ruta_zip):
        return False

    with zipfile.ZipFile(ruta_zip, 'r') as zipf:
        zipf.extractall(current_app.root_path)

    return True

def listar_backups():
    conn = conectar_sql_server()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT 
            IdBackup,
            NombreArchivo,
            FechaBackup,
            TamañoMB,
            u.NombreCompleto,
            u.IdUsuario
        FROM BackupRegistro br
        JOIN Usuario u ON br.IdUsuario = u.IdUsuario
        ORDER BY FechaBackup DESC
    """)
    datos = cursor.fetchall()
    cursor.close()
    conn.close()
    return datos
