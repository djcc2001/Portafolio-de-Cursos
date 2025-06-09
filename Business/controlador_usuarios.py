from flask import Blueprint, render_template, request, redirect, session, url_for

from Data.cUsuario import *

usuario = Blueprint('usuario', __name__, template_folder='Presentacion')

# Iniciar Sesion


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
