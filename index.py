from flask import Flask, render_template, request, redirect, url_for, flash
import os
from datetime import datetime
from Business.respaldo import crear_respaldo_zip

# Crear la app
app = Flask(__name__, template_folder='Presentacion')
app.secret_key = 'clave_secreta_segura'

# Función para generar respaldo diario automático entre 8:00 y 9:00 AM
def respaldo_automático_diario():
    backups_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'backups')
    os.makedirs(backups_folder, exist_ok=True)

    hoy = datetime.now().strftime('%Y%m%d')
    hora_actual = datetime.now().hour

    # Ejecutar solo entre las 8:00 y 8:59 AM
    if 8 <= hora_actual < 9:
        archivos = os.listdir(backups_folder)
        ya_existe = any(hoy in archivo for archivo in archivos)

        if not ya_existe:
            print("[RESPALDO] Generando respaldo automático diario (8AM)...")
            crear_respaldo_zip(2)  # ⬅ Se reemplaza 2 por el ID de administrador
            print("[RESPALDO] ✔ Respaldo generado.")
        else:
            print("[RESPALDO] Ya existe respaldo para hoy.")
    else:
        print("[RESPALDO] Hora no válida para respaldo automático. (Esperado: 8AM)")

# Ejecutar respaldo al iniciar
respaldo_automático_diario()

# Agregar rutas
from Business.controlador_usuarios import usuario
app.register_blueprint(usuario)

# Ejecutar servidor
if __name__ == '__main__':
    app.run(debug=True)
