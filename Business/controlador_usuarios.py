from flask import Blueprint, render_template, request, redirect, session, url_for

from Data.cUsuario import *
from Data.conexion import conectar_sql_server # Asegúrate que esta importación sea necesaria aquí

usuario = Blueprint('usuario', __name__, template_folder='Presentacion')

# Iniciar Sesion

@usuario.route('/')
def Inicio():
    return render_template('inicio.html')

# Editar Usuario

@usuario.route('/editar_usuario/<int:idUsuario>', methods=['GET', 'POST'])
def editar_usuario(idUsuario):
    # La verificación de rol ya está comentada aquí, lo cual es correcto para esta etapa.
    # if 'rol' not in session or session['rol'] != "Administrador":
    #     return render_template('pagina404.html') # O redirigir al login

    if request.method == 'POST':
        nombreCompleto = request.form['nombreCompleto']
        correo = request.form['correo']
        contrasenia = request.form['contrasenia'] 
        idRol = request.form['idRol']
        
        if ActualizarUsuario(idUsuario, nombreCompleto, correo, contrasenia, idRol):
            pass
        else:
            pass
        return redirect(url_for('usuario.GestionarRoles')) 

    datos_usuario = ConsultaUsuarioPorId(idUsuario)
    todos_los_roles = ConsultaRoles() 

    if not datos_usuario:
        return redirect(url_for('usuario.GestionarRoles'))

    return render_template('EditarUsuario.html', usuario=datos_usuario, roles=todos_los_roles)

# Gestionar Roles
@usuario.route('/gestion-roles')
def GestionarRoles():
    # if(session['rol']!="Administrador"): # Comentado temporalmente para evitar KeyError
    #     return render_template('pagina404.html')
    pass # Se permite el acceso temporalmente hasta implementar login
    
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
        return redirect(url_for('usuario.crear_usuario')) # Considera redirigir a GestionarRoles
    
    # Método GET
    cursor.execute("SELECT IdRol, NombreRol FROM Rol WHERE NombreRol IN ('Docente', 'Administrador')")
    roles = cursor.fetchall()
    cursor.close() # Cerrar cursor
    conexion.close() # Cerrar conexión
    return render_template('CrearUsuario.html', roles=roles)

# Ruta para cerrar sesión (básica hasta implementar login completo)
@usuario.route('/cerrar_sesion')
def CerrarSesion():
    session.pop('rol', None) # Elimina 'rol' de la sesión si existe
    # session.clear() # Para limpiar toda la sesión si es necesario
    return redirect(url_for('usuario.Inicio')) # Redirige a la página de inicio
