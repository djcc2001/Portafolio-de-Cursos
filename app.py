from flask import Flask, render_template, request, redirect, url_for
from Data.conexion import conectar_sql_server

app = Flask(__name__, template_folder='Presentacion')

@app.route('/')
def inicio():
    return render_template('inicio.html')

@app.route('/crear_usuario', methods=['GET', 'POST'])
def crear_usuario():
    conexion = conectar_sql_server()
    if not conexion:
        return "Error en la conexión a la base de datos."
    cursor = conexion.cursor()
    if request.method == 'POST':
        id_rol = request.form['idRol']
        nombre = request.form['nombre']
        apellido_paterno = request.form['apellido_paterno']
        apellido_materno = request.form['apellido_materno']
        correo = request.form['correo']
        contrasenia = request.form['contrasenia']
        nombre_completo = f"{nombre} {apellido_paterno} {apellido_materno}"
        # Generar un nuevo IdUsuario (puedes mejorar esto usando autoincremento en la BD)
        cursor.execute("SELECT ISNULL(MAX(IdUsuario), 0) + 1 FROM Usuario")
        nuevo_id = cursor.fetchone()[0]
        cursor.execute(
            "INSERT INTO Usuario (IdUsuario, NombreCompleto, CorreoElectronico, Contrasenia, IdRol) VALUES (?, ?, ?, ?, ?)",
            (nuevo_id, nombre_completo, correo, contrasenia, id_rol)
        )
        conexion.commit()
        return redirect(url_for('crear_usuario'))
    # Obtener solo roles Docente y Administrador para el select
    cursor.execute("SELECT IdRol, NombreRol FROM Rol WHERE NombreRol IN ('Docente', 'Administrador')")
    roles = cursor.fetchall()
    return render_template('CrearUsuario.html', roles=roles)

@app.route('/gestionar_roles', methods=['GET', 'POST'])
def gestionar_roles():
    conexion = conectar_sql_server()
    if conexion:
        cursor = conexion.cursor()
        if request.method == 'POST':
            id_usuario = request.form['idUsuario']
            id_rol = request.form['idRol']
            cursor.execute("UPDATE Usuario SET IdRol = ? WHERE IdUsuario = ?", (id_rol, id_usuario))
            conexion.commit()
            return redirect(url_for('gestionar_roles'))
        
        cursor.execute("SELECT * FROM Usuario")
        usuarios = cursor.fetchall()
        cursor.execute("SELECT * FROM Rol")
        roles = cursor.fetchall()
        return render_template('GestionarRoles.html', usuarios=usuarios, roles=roles)
    return "Error en la conexión a la base de datos."

if __name__ == '__main__':
    app.run(debug=True)