from flask import Blueprint, render_template, request, redirect, session, url_for

from Data.cUsuario import *

usuario = Blueprint('usuario', __name__, template_folder='Presentacion')

# Iniciar Sesion

@usuario.route('/')
def Inicio():
    return render_template('inicio.html')

# Gestionar Roles
@usuario.route('/gestion-roles')
def GestionarRoles():
    if(session['rol']!="Administrador"):
        return render_template('pagina404.html')
    
    # mostrar datos 
    DatosUser = ConsultaUsuarioRoles()
    DatosRoles = ConsultaRoles()
    return render_template('GestionarRoles.html', usuarios=DatosUser, roles=DatosRoles)

@usuario.route('/actualizar-rol', methods=['POST'])
def ActualizarRol():
    if(session['rol']!="Administrador"):
        return render_template('pagina404.html')

    # actualizar
    idUsuario = request.form['idUsuario']
    idRol = request.form['idRol']

    ConsultaActualizarRol(idUsuario, idRol)
    
    # mostrar datos 
    DatosUser = ConsultaUsuarioRoles()
    DatosRoles = ConsultaRoles()
    return render_template('GestionarRoles.html', usuarios=DatosUser, roles=DatosRoles)

@usuario.route('/crear_usuario', methods=['GET', 'POST'])
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
        cursor.execute("SELECT ISNULL(MAX(IdUsuario), 0) + 1 FROM Usuario")
        nuevo_id = cursor.fetchone()[0]
        cursor.execute(
            "INSERT INTO Usuario (IdUsuario, NombreCompleto, CorreoElectronico, Contrasenia, IdRol) VALUES (?, ?, ?, ?, ?)",
            (nuevo_id, nombre_completo, correo, contrasenia, id_rol)
        )
        conexion.commit()
        return redirect(url_for('usuario.crear_usuario'))
    cursor.execute("SELECT IdRol, NombreRol FROM Rol WHERE NombreRol IN ('Docente', 'Administrador')")
    roles = cursor.fetchall()
    return render_template('CrearUsuario.html', roles=roles)