from Data.conexion import conectar_sql_server

# Funciones propias para la gestion de usuario
# Iniciar Sesion


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
