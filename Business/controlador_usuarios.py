from flask import Blueprint, request, jsonify, session, render_template, redirect, url_for
from Business.EmailSender import enviar_codigo_email
from Data.cUsuario import *
import random

from Data.conexion import conectar_sql_server # Asegúrate que esta importación sea necesaria aquí

usuario = Blueprint('usuario', __name__, template_folder='Presentacion')

# Iniciar Sesion
@usuario.route('/')
def Inicio():
    return render_template('IniciarSesion.html')

# Para iniciar sesion
@usuario.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        correo = request.form['correo']
        contrasenia = request.form['contrasenia']

        usuario = ConsultaUsuarioPorCorreo(correo, contrasenia)

        if usuario:
            session['rol'] = usuario[4]  # Guardamos el ID del rol
            session['nombre'] = usuario[1]
            return redirect(url_for('usuario.redirigir_por_rol'))
        else:
            return render_template('IniciarSesion.html', mensaje="Correo o contraseña incorrectos")

    return render_template('IniciarSesion.html')

# Recuperar Contraseña
@usuario.route('/recuperar-contrasenia')
def recuperar_contrasena():
    return render_template('RecuperarContraseña.html')

# Vistas de usuarios que tendran las opciones dentro en funcion de que rol tiene
# Aqui no tocar nada solo colocar las opciones en el html, tomar como referencia de admin que ya tiene opciones hechas
@usuario.route('/redirigir')
def redirigir_por_rol():
    rol_id = session.get('rol')

    if rol_id == 2:  # Administrador
        return redirect(url_for('usuario.vista_administrador'))
    elif rol_id == 1:  # Docente
        return redirect(url_for('usuario.vista_docente'))
    elif rol_id == 3:  # Evaluador
        return redirect(url_for('usuario.vista_evaluador'))
    else:
        return "Rol desconocido", 400

@usuario.route('/admin')
def vista_administrador():
    return render_template('admin.html')

@usuario.route('/docente')
def vista_docente():
    return render_template('docente.html')

@usuario.route('/evaluador')
def vista_evaluador():
    return render_template('evaluador.html')
    
# Crear Usuario
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
        cursor.close() # Cerrar cursor
        conexion.close() # Cerrar conexión
        return redirect(url_for('usuario.redirigir_por_rol')) # Considera redirigir a GestionarRoles
    
    # Método GET
    cursor.execute("SELECT IdRol, NombreRol FROM Rol")
    roles = cursor.fetchall()
    cursor.close() # Cerrar cursor
    conexion.close() # Cerrar conexión
    return render_template('CrearUsuario.html', roles=roles)

# Editar Usuario
@usuario.route('/editar_usuario/<int:idUsuario>', methods=['GET', 'POST'])
def editar_usuario(idUsuario):
    if request.method == 'POST':
        nombreCompleto = request.form['nombreCompleto']
        correo = request.form['correo']
        contrasenia = request.form['contrasenia'] 
        idRol = request.form['idRol']
        
        if ActualizarUsuario(idUsuario, nombreCompleto, correo, contrasenia, idRol):
            pass
        else:
            pass
        return redirect(url_for('usuario.redirigir_por_rol')) 

    datos_usuario = ConsultaUsuarioPorId(idUsuario)
    todos_los_roles = ConsultaRoles() 

    if not datos_usuario:
        return redirect(url_for('usuario.redirigir_por_rol'))

    return render_template('EditarUsuario.html', usuario=datos_usuario, roles=todos_los_roles)


@usuario.route('/ListarUsuarios', methods=['GET'])
def ListarUsuarios():
    # Obtener filtro de búsqueda si se proporciona
    buscar = request.args.get('buscar', '')

    # Consulta de usuarios filtrados o no
    if buscar:
        usuarios = ConsultaUsuariosFiltrados(buscar)
    else:
        usuarios = ConsultaUsuarioRoles()

    return render_template('ListarUsuarios.html', usuarios=usuarios)


# Gestionar Roles
@usuario.route('/gestion-roles')
def GestionarRoles():
    if(session['rol']!=2): # Comentado temporalmente para evitar KeyError
        return render_template('pagina404.html')
    
    # mostrar datos 
    DatosUser = ConsultaUsuarioRoles()
    DatosRoles = ConsultaRoles()
    return render_template('GestionarRoles.html', usuarios=DatosUser, roles=DatosRoles)

@usuario.route('/actualizar-rol', methods=['POST'])
def ActualizarRol():
    # if(session['rol']!="Administrador"): # Comentado temporalmente para evitar KeyError
    #     return render_template('pagina404.html')
    pass # Se permite el acceso temporalmente hasta implementar login

    # actualizar
    idUsuario = request.form['idUsuario']
    idRol = request.form['idRol']

    ConsultaActualizarRol(idUsuario, idRol)
    
    # Es mejor redirigir después de un POST en lugar de renderizar la plantilla de nuevo
    return redirect(url_for('usuario.GestionarRoles'))

# Ruta para cerrar sesión (básica hasta implementar login completo)
@usuario.route('/cerrar_sesion')
def CerrarSesion():
    session.pop('rol', None) # Elimina 'rol' de la sesión si existe
    # session.clear() # Para limpiar toda la sesión si es necesario
    return redirect(url_for('usuario.Inicio')) # Redirige a la página de inicio

# == eliminar usuario

# Paginas 404
@usuario.route('/pagina404')
def pagina404():
    return render_template('pagina404.html')
