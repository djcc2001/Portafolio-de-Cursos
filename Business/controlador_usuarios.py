from flask import Blueprint, request, jsonify, session, render_template, redirect, url_for, flash, send_from_directory, abort, current_app
from Business.EmailSender import *
from Data.cUsuario import *
import random
import os

from Data.conexion import conectar_sql_server # Asegúrate que esta importación sea necesaria aquí

usuario = Blueprint('usuario', __name__, template_folder='Presentacion')

# Pagina 404
@usuario.route('/pagina404')
def pagina404():
    return render_template('pagina404.html')

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
            session['idUsuario'] = usuario[0]
            return redirect(url_for('usuario.redirigir_por_rol'))
        else:
            return render_template('IniciarSesion.html', mensaje="Correo o contraseña incorrectos")

    return render_template('IniciarSesion.html')

# Vistas de usuarios que tendran las opciones dentro en funcion de que rol tiene
# Aqui no tocar nada solo colocar las opciones en el html, tomar como referencia de admin que ya tiene opciones hechas
@usuario.route('/redirigir')
def redirigir_por_rol():
    rol_id = session.get('rol')

    if rol_id not in [1, 2, 3]:  # Verifica si el rol es válido
        return redirect(url_for('usuario.pagina404'))

    return render_template('inicio.html')  # Vista unificada

# Recuperar Contraseña
@usuario.route('/recuperar-contrasenia')
def recuperar_contrasena():
    return render_template('RecuperarContraseña.html')

@usuario.route('/enviar-codigo', methods=['POST'])
def enviar_codigo():
    data = request.get_json()
    email = data.get('email')

    if not verificar_correo(email):
        return jsonify({'success': False, 'message': 'Correo no registrado'})

    codigo = ''.join([str(random.randint(0, 9)) for _ in range(6)])
    session['codigo_verificacion'] = codigo
    session['email_verificacion'] = email

    enviar_codigo_email(email, codigo)
    return jsonify({'success': True, 'message': 'Código enviado correctamente'})

@usuario.route('/verificar-codigo', methods=['POST'])
def verificar_codigo():
    data = request.get_json()
    codigo_usuario = data.get('codigo')
    if session.get('codigo_verificacion') == codigo_usuario:
        return jsonify({'success': True})
    return jsonify({'success': False, 'message': 'Código incorrecto'})

@usuario.route('/actualizar-password', methods=['POST'])
def actualizar_password():
    data = request.get_json()
    nueva = data.get('nueva')
    confirmar = data.get('confirmar')

    if nueva != confirmar:
        return jsonify({'success': False, 'message': 'Las contraseñas no coinciden'})

    email = session.get('email_verificacion')
    actualizar_contraseña(email, nueva)
    session.pop('codigo_verificacion', None)
    session.pop('email_verificacion', None)
    return jsonify({'success': True})
    
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

@usuario.route('/eliminar_usuario/<int:idUsuario>', methods=['POST'])
def eliminar_usuario_ruta(idUsuario):
    # Aquí deberías añadir una verificación de rol, por ejemplo, solo administradores
    if 'rol' not in session or session['rol'] != 2: # Suponiendo que 2 es el rol de Administrador
        flash('No tienes permiso para realizar esta acción.', 'danger')
        return redirect(url_for('usuario.ListarUsuarios'))

    if EliminarUsuario(idUsuario):
        flash('Usuario eliminado correctamente.', 'success')
    else:
        flash('Error al eliminar el usuario. Puede que tenga registros asociados.', 'danger')
    return redirect(url_for('usuario.ListarUsuarios'))


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
    #session.clear() # Para limpiar toda la sesión si es necesario
    return redirect(url_for('usuario.Inicio')) # Redirige a la página de inicio
    
@usuario.route('/crear_portafolio', methods=['GET', 'POST'])
def crear_portafolio_vista():
    if 'rol' not in session or session['rol'] != 2: # Solo Administradores
        flash('Acceso no autorizado.', 'danger')
        return redirect(url_for('usuario.redirigir_por_rol'))

    if request.method == 'POST':
        nombre_curso_input = request.form.get('nombre_curso')
        nombre_semestre_input = request.form.get('semestre')
        estado_portafolio = "Activo"  # Estado por defecto para nuevos portafolios

        if not nombre_curso_input or not nombre_semestre_input:
            flash('El nombre del curso y el semestre son requeridos.', 'warning')
        else:
            success = CrearPortafolioCompleto(nombre_curso_input, nombre_semestre_input, estado_portafolio)
            if success:
                flash('Portafolio creado exitosamente.', 'success')
            else:
                flash('Error al crear el portafolio. Verifique los datos o si ya existe una combinación similar.', 'danger')
        return redirect(url_for('usuario.crear_portafolio_vista'))

    # Método GET: Mostrar página con portafolios existentes y formulario de creación
    portafolios_existentes = ListarPortafoliosConDetalles()
    return render_template('CrearPortafolio.html', portafolios=portafolios_existentes)
    
# Asignar portafolio
@usuario.route('/asignarPortafolio', methods=['GET', 'POST'])
def AsignarPortafolioVista():
    if request.method == 'POST':
        id_portafolio = request.form['idPortafolio']
        id_usuario = request.form['idUsuario']
        rol_portafolio = request.form.get('rolPortafolio', 'Responsable')
        AsignarPortafolio(id_portafolio, id_usuario, rol_portafolio)
        return redirect(url_for('usuario.AsignarPortafolioVista'))

    portafolios = ObtenerPortafolios()
    usuarios = ObtenerUsuariosAsignables()
    asignaciones = ObtenerAsignacionesPortafolio()

    # Crear diccionario de listas por portafolio
    asignaciones_dict = {}
    for p_id, nombre, rol in asignaciones:
        asignaciones_dict.setdefault(p_id, []).append({'nombre': nombre, 'rol': rol})

    return render_template(
        'asignar_portafolio.html',
        portafolios=portafolios,
        usuarios=usuarios,
        asignaciones_dict=asignaciones_dict
    )


# Asignar trabajos a Evaluadores
@usuario.route('/asignarTrabajos', methods=['GET', 'POST'])
def AsignarTrabajosVista():
    if request.method == 'POST':
        trabajo_id = request.form.get('materialId')
        evaluador_id = request.form.get('evaluadorId')

        if trabajo_id and evaluador_id:
            exito = AsignarTrabajoAEvaluador(trabajo_id, evaluador_id)

            if exito:
                correo, nombre = ObtenerCorreoEvaluador(evaluador_id)

                if correo:
                    # Obtener nombre del archivo del trabajo
                    conexion = conectar_sql_server()
                    cursor = conexion.cursor()
                    cursor.execute("SELECT NombreArchivo FROM MaterialEnseñanza WHERE IdMaterial = ?", (trabajo_id,))
                    fila = cursor.fetchone()
                    archivo = fila[0] if fila else "un trabajo"
                    cursor.close()
                    conexion.close()

                    enviar_notificacion_asignacion(correo, nombre, archivo)
            
            return redirect(url_for('usuario.AsignarTrabajosVista'))


    materiales = ObtenerMateriales()
    evaluadores = ObtenerEvaluadores()
    asignados = ObtenerMaterialAsignado()

    return render_template(
        'asignar_trabajo.html',
        materiales=materiales,
        evaluadores=evaluadores,
        asignados=asignados
    )

# Devolver evaluación del documento al docente
@usuario.route('/DevolverEvaluacion', methods=['GET', 'POST'])
def DevolverEvaluacion():
    id_evaluador = session.get('idUsuario')

    if request.method == 'POST':
        id_observacion = request.form.get('documento')
        estado = request.form.get('estado')
        observacion = request.form.get('observaciones') if estado == 'Desaprobado' else None

        # Llamas a tu función para actualizar el documento evaluado
        ActualizarEvaluacion(id_observacion, estado, observacion)

        # Obtener datos del docente
        datos_docente = ObtenerCorreoDocentePorObservacion(id_observacion)
        if datos_docente:
            correo_docente, nombre_docente, nombre_archivo = datos_docente
            enviar_notificacion_evaluacion(
                destinatario=correo_docente,
                nombre_docente=nombre_docente,
                nombre_archivo=nombre_archivo,
                estado=estado
            )
        return redirect(url_for('usuario.DevolverEvaluacion'))

    documentos = ObtenerDocumentoEvaluador(id_evaluador)
    return render_template('evaluar_documento.html', documentos=documentos)

# Ver portafolios
@usuario.route('/portafolios', methods=['GET', 'POST'])
def ver_portafolios():
    semestres = obtener_semestres()
    portafolios = []
    id_semestre = None
    if request.method == 'POST':
        id_semestre = request.form.get('semestre')
        portafolios = obtener_portafolios_por_semestre(id_semestre)
    else:
        portafolios = obtener_portafolios_por_semestre()
    return render_template('PortafoliosPorSemestre.html', semestres=semestres, portafolios=portafolios, id_semestre=id_semestre)


# Detalle Portafolio
@usuario.route('/DetallePortafolio', methods=['GET', 'POST'])
def DetallePortafolio():
    if request.method == 'POST':
        id_portafolio = request.form.get('id_portafolio')  
    else:
        id_portafolio = request.args.get('id_portafolio')
    if not id_portafolio:
        return "ID de portafolio no proporcionado", 400
    archivos = obtener_archivos_portafolio(id_portafolio)
    # 🔧 ESTA LÍNEA ES LA MODIFICADA (antes no pasabas id_portafolio)
    return render_template('DetallePortafolio.html', archivos=archivos, id_portafolio=id_portafolio)


# Cambiar estado del portafolio (Completo/Incompleto)
@usuario.route('/marcar_estado_portafolio', methods=['GET', 'POST'])
def marcar_estado_portafolio():
    if request.method == 'POST':
        if 'idUsuario' not in session:
            return redirect(url_for('usuario.login'))  # o la ruta de login

        modificado_por = session['idUsuario']
        ids_portafolios = request.form.getlist('portafolios_ids')

        for id_portafolio in ids_portafolios:
            nuevo_estado = request.form.get(f'estado_{id_portafolio}')
            if not nuevo_estado:
                continue
            resultado = MarcarEstadoPortafolio(id_portafolio, nuevo_estado, modificado_por)

        return redirect(url_for('usuario.redirigir_por_rol'))  # Redirección exitosa

    portafolios = obtener_portafolios_con_faltantes()
    return render_template('marcarportafolio.html', portafolios=portafolios)

def ActualizarEstadoPortafolio(id_portafolio, nuevo_estado):
    conexion = conectar_sql_server()
    cursor = conexion.cursor()
    cursor.execute("UPDATE Portafolio SET Estado = ? WHERE IdPortafolio = ?", (nuevo_estado, id_portafolio))
    conexion.commit()
    cursor.close()
    conexion.close()

# Subir material con ID del portafolio
@usuario.route('/subir_material/<int:id_portafolio>', methods=['GET', 'POST'])
def SubirMaterialVistaConID(id_portafolio):
    mensaje_exito = None

    if request.method == 'POST':
        tipo = request.form['tipo']
        archivo = request.files.get('archivo')

        if not archivo or archivo.filename == '':
            mensaje_exito = 'Debe seleccionar un archivo.'
        elif not archivo.filename.endswith('.pdf'):
            mensaje_exito = 'Solo se permiten archivos PDF.'
        else:
            guardar_material_ensenanza(id_portafolio, tipo, archivo)
            mensaje_exito = 'Archivo subido correctamente.'

    return render_template('subir_material.html', id_portafolio=id_portafolio, mensaje_exito=mensaje_exito)

# Visualizar documentos sin necesidad de descarga
@usuario.route('/ver_archivo/<path:ruta_relativa>')
def ver_archivo(ruta_relativa):
    # Divide la ruta para obtener carpeta y archivo
    ruta_absoluta = os.path.join(current_app.root_path, ruta_relativa)
    
    if not os.path.isfile(ruta_absoluta):
        abort(404)

    # Separa la carpeta base y el nombre del archivo
    carpeta, nombre_archivo = os.path.split(ruta_absoluta)

    return send_from_directory(carpeta, nombre_archivo, as_attachment=False)


# Eliminar material
@usuario.route('/eliminar_material', methods=['POST'])
def eliminar_material():
    id_portafolio = request.form['id_portafolio']
    nombre_archivo = request.form['nombre_archivo']
    tipo_material = request.form['tipo_material']
    id_usuario = session.get('idUsuario')  # Asegúrate de que esté presente en sesión

    if id_usuario is None:
        flash('Sesión expirada o no válida. Por favor, inicia sesión nuevamente.', 'warning')
        return redirect(url_for('usuario.Inicio'))

    exito = eliminar_material_U(id_portafolio, nombre_archivo, tipo_material, id_usuario)

    if exito:
        flash('Archivo eliminado correctamente.', 'success')
    else:
        flash('Hubo un error al eliminar el archivo.', 'danger')

    return redirect(url_for('usuario.DetallePortafolio', id_portafolio=id_portafolio))

# Ver silabos
@usuario.route('/silabos', methods=['GET', 'POST'])
def gestionar_silabos():
    return render_template('ver_silabos.html')

# Detalle silabo
@usuario.route('/silabos/<tipo_silabo>', methods=['GET'])
def ver_detalle_silabos(tipo_silabo):
    silabos = obtener_silabos_por_tipo(tipo_silabo)
    print(silabos)
    return render_template('detalle_silabos.html', tipo_silabo=tipo_silabo, silabos=silabos)

# Subir silabo
@usuario.route('/subir_silabo/<tipo_silabo>', methods=['GET', 'POST'])
def subir_silabo(tipo_silabo):
    mensaje_exito = None

    # Obtener todos los portafolios (id, nombre del curso)
    portafolios = obtener_lista_portafolios()  # [(id, nombre_curso), ...]

    if request.method == 'POST':
        id_portafolio = int(request.form['id_portafolio'])
        archivo = request.files.get('archivo')

        if not archivo or archivo.filename == '':
            mensaje_exito = 'Debe seleccionar un archivo.'
        elif not archivo.filename.endswith('.pdf'):
            mensaje_exito = 'Solo se permiten archivos PDF.'
        else:
            guardar_silabo(id_portafolio, tipo_silabo, archivo)
            mensaje_exito = 'Archivo subido correctamente.'

    return render_template('subir_silabo.html', tipo_silabo=tipo_silabo, portafolios=portafolios, mensaje_exito=mensaje_exito)

