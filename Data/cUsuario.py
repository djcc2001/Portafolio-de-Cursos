from Data.conexion import conectar_sql_server

# Funcion para validar usuario en iniciar sesion
def ConsultaUsuarioPorCorreo(correo, contrasenia):
    conexion = conectar_sql_server()
    try:
        cursor = conexion.cursor()
        consulta = """
            SELECT IdUsuario, NombreCompleto, CorreoElectronico, Contrasenia, IdRol
            FROM Usuario
            WHERE CorreoElectronico = ? AND Contrasenia = ?
        """
        cursor.execute(consulta, (correo, contrasenia))
        usuario = cursor.fetchone()
        return usuario
    except Exception as e:
        print("Error al consultar usuario por correo:", e)
        return None
    finally:
        if conexion:
            cursor.close()
            conexion.close()

# Funciones propias para la gestion de usuario

# Gestionar Roles
def ConsultaRoles():
    # conectar a la BD
    conexion = conectar_sql_server()

    try:
        cursor = conexion.cursor()
        consulta = "SELECT * FROM Rol"
        cursor.execute(consulta)
        # Obtener el resultado
        datos = cursor.fetchall()
        return datos
    except Exception as e:
        print("Error al consultar:", e)
        return None
    finally:
        # Cerrar cursor y conexión
        cursor.close()
        # cerrar conexion a la BD
        conexion.close()

def ConsultaUsuarioRoles():
    # conectar a la BD
    conexion = conectar_sql_server()

    try:
        cursor = conexion.cursor()
        consulta = "SELECT u.IdUsuario, u.NombreCompleto, u.CorreoElectronico, r.NombreRol FROM Usuario u INNER JOIN Rol r ON u.IdRol=r.IdRol"
        cursor.execute(consulta)
        # Obtener el resultado
        datos = cursor.fetchall()
        return datos
    except Exception as e:
        print("Error al consultar:", e)
        return None
    finally:
        # Cerrar cursor y conexión
        cursor.close()
        # cerrar conexion a la BD
        conexion.close()

def ConsultaActualizarRol(idUsuario, idRol):
    # conectar a la BD
    conexion = conectar_sql_server()

    try:
        cursor = conexion.cursor()
        consulta = "UPDATE Usuario SET IdRol = ? WHERE IdUsuario = ?"
        cursor.execute(consulta, (idRol, idUsuario))
        conexion.commit()
        return True
    except Exception as e:
        print("Error al consultar:", e)
        return None
    finally:
        # Cerrar cursor y conexión
        cursor.close()
        # cerrar conexion a la BD
        conexion.close()


def ConsultaActualizarRol(idUsuario, idRol):
    # conectar a la BD
    conexion = conectar_sql_server()

    try:
        cursor = conexion.cursor()
        consulta = "UPDATE Usuario SET IdRol = ? WHERE IdUsuario = ?"
        cursor.execute(consulta, (idRol, idUsuario))
        conexion.commit()
        return True
    except Exception as e:
        print("Error al consultar:", e)
        return None
    finally:
        # Cerrar cursor y conexión
        cursor.close()
        # cerrar conexion a la BD
        conexion.close()

def ConsultaUsuarioPorId(idUsuario):
    conexion = conectar_sql_server()
    try:
        cursor = conexion.cursor()
        # Asegúrate que los campos coincidan con los que esperas en EditarUsuario.html
        # (IdUsuario, NombreCompleto, CorreoElectronico, Contrasenia, IdRol)
        consulta = "SELECT IdUsuario, NombreCompleto, CorreoElectronico, Contrasenia, IdRol FROM Usuario WHERE IdUsuario = ?"
        cursor.execute(consulta, (idUsuario,))
        datos = cursor.fetchone()
        return datos
    except Exception as e:
        print("Error al consultar usuario por ID:", e)
        return None
    finally:
        if conexion:
            cursor.close()
            conexion.close()

def ActualizarUsuario(idUsuario, nombreCompleto, correo, contrasenia, idRol):
    conexion = conectar_sql_server()
    try:
        cursor = conexion.cursor()

        # Si la contraseña está en blanco, se obtiene la actual de la base de datos
        if not contrasenia.strip():
            cursor.execute("SELECT Contrasenia FROM Usuario WHERE IdUsuario = ?", (idUsuario,))
            contrasenia_actual = cursor.fetchone()
            if contrasenia_actual:
                contrasenia = contrasenia_actual[0]
            else:
                print("Usuario no encontrado")
                return False

        consulta = """
            UPDATE Usuario 
            SET NombreCompleto = ?, CorreoElectronico = ?, Contrasenia = ?, IdRol = ?
            WHERE IdUsuario = ?
        """
        cursor.execute(consulta, (nombreCompleto, correo, contrasenia, idRol, idUsuario))
        conexion.commit()
        return True
    except Exception as e:
        print("Error al actualizar usuario:", e)
        return False
    finally:
        if conexion:
            cursor.close()
            conexion.close()

# Eliminar usuario
def ConsultaUsuariosFiltrados(filtro_nombre):
    conexion = conectar_sql_server()
    try:
        cursor = conexion.cursor()
        consulta = """
            SELECT u.IdUsuario, u.NombreCompleto, u.CorreoElectronico, r.NombreRol 
            FROM Usuario u
            INNER JOIN Rol r ON u.IdRol = r.IdRol
            WHERE u.NombreCompleto LIKE ?
        """
        cursor.execute(consulta, ('%' + filtro_nombre + '%',))
        return cursor.fetchall()
    except Exception as e:
        print("Error al filtrar usuarios:", e)
        return []
    finally:
        cursor.close()
        conexion.close()

# Verificar si existe el correo
def verificar_correo(email):
    conexion = conectar_sql_server()
    cursor = conexion.cursor()
    cursor.execute("SELECT COUNT(*) FROM Usuario WHERE CorreoElectronico = ?", (email,))
    existe = cursor.fetchone()[0] > 0
    conexion.close()
    return existe

# Actualizar la contraseña en la base de datos
def actualizar_contraseña(email, nueva):
    conexion = conectar_sql_server()
    cursor = conexion.cursor()
    cursor.execute("UPDATE Usuario SET Contrasenia = ? WHERE CorreoElectronico = ?", (nueva, email))
    conexion.commit()
    conexion.close()
