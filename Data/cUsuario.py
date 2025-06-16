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
def EliminarUsuario(idUsuario):
    conexion = conectar_sql_server()
    try:
        cursor = conexion.cursor()
        cursor.execute("DELETE FROM Usuario WHERE IdUsuario = ?", (idUsuario,))
        conexion.commit()
        return True
    except Exception as e:
        print(f"Error al eliminar usuario: {e}")
        return False
    finally:
        if conexion:
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

# Asignar portafolios a docentes y evaluadores
# Obtener portafolios con semestre
def ObtenerPortafolios():
    conexion = conectar_sql_server()
    try:
        cursor = conexion.cursor()
        consulta = """
            SELECT P.IdPortafolio, CONCAT('Portafolio_', P.IdPortafolio), S.Nombre 
            FROM Portafolio P
            JOIN Semestre S ON P.IdSemestre = S.IdSemestre
        """
        cursor.execute(consulta)
        return cursor.fetchall()
    except Exception as e:
        print("Error al obtener portafolios:", e)
        return []
    finally:
        cursor.close()
        conexion.close()

# Obtener usuarios docentes o evaluadores
def ObtenerUsuariosAsignables():
    conexion = conectar_sql_server()
    try:
        cursor = conexion.cursor()
        cursor.execute("""
            SELECT IdUsuario, NombreCompleto, CorreoElectronico
            FROM Usuario
            WHERE IdRol IN (1, 3)
        """)
        return cursor.fetchall()
    except Exception as e:
        print("Error al obtener usuarios asignables:", e)
        return []
    finally:
        cursor.close()
        conexion.close()

# Obtener usuarios docentes o evaluadores (agregamos IdRol)
def ObtenerUsuariosAsignables():
    conexion = conectar_sql_server()
    try:
        cursor = conexion.cursor()
        cursor.execute("""
            SELECT IdUsuario, NombreCompleto, CorreoElectronico, IdRol
            FROM Usuario
            WHERE IdRol IN (1, 3)
        """)
        return cursor.fetchall()
    except Exception as e:
        print("Error al obtener usuarios asignables:", e)
        return []
    finally:
        cursor.close()
        conexion.close()

# Obtener asignaciones actuales (ahora también rol)
def ObtenerAsignacionesPortafolio():
    conexion = conectar_sql_server()
    try:
        cursor = conexion.cursor()
        cursor.execute("""
            SELECT PU.IdPortafolio, U.NombreCompleto, PU.RolEnPortafolio
            FROM PortafolioUsuario PU
            JOIN Usuario U ON PU.IdUsuario = U.IdUsuario
        """)
        return cursor.fetchall()
    except Exception as e:
        print("Error al obtener asignaciones:", e)
        return []
    finally:
        cursor.close()
        conexion.close()

# Insertar asignación, pero solo si no existe ya para ese portafolio y rol
def AsignarPortafolio(id_portafolio, id_usuario, rol_portafolio="Responsable"):
    conexion = conectar_sql_server()
    try:
        cursor = conexion.cursor()

        if rol_portafolio == "Responsable":
            cursor.execute("""
                SELECT COUNT(*) FROM PortafolioUsuario
                WHERE IdPortafolio = ? AND RolEnPortafolio = 'Responsable'
            """, (id_portafolio,))
            if cursor.fetchone()[0] > 0:
                return False  # Ya hay responsable

        cursor.execute("""
            SELECT COUNT(*) FROM PortafolioUsuario
            WHERE IdPortafolio = ? AND IdUsuario = ? AND RolEnPortafolio = ?
        """, (id_portafolio, id_usuario, rol_portafolio))
        if cursor.fetchone()[0] > 0:
            return False  # Ya existe esta asignación

        cursor.execute("SELECT ISNULL(MAX(IdPortafolioUsuario), 0) + 1 FROM PortafolioUsuario")
        nuevo_id = cursor.fetchone()[0]

        cursor.execute("""
            INSERT INTO PortafolioUsuario (IdPortafolioUsuario, IdPortafolio, IdUsuario, RolEnPortafolio)
            VALUES (?, ?, ?, ?)
        """, (nuevo_id, id_portafolio, id_usuario, rol_portafolio))
        conexion.commit()
        return True
    except Exception as e:
        print("Error al asignar portafolio:", e)
        return False
    finally:
        cursor.close()
        conexion.close()

# --- Asignar Trabajos a evaluador
def ObtenerMateriales():
    conexion = conectar_sql_server()
    try:
        cursor = conexion.cursor()
        cursor.execute("""
            SELECT ME.IdMaterial, ME.TipoMaterial, ME.NombreArchivo, ME.FechaSubida
            FROM MaterialEnseñanza ME
            LEFT JOIN ObservacionMaterial OM ON ME.IdMaterial = OM.IdMaterial
            WHERE OM.IdMaterial IS NULL
        """)
        return cursor.fetchall()
    except Exception as e:
        print("Error al obtener trabajos:", e)
        return []
    finally:
        cursor.close()
        conexion.close()

def ObtenerEvaluadores():
    conexion = conectar_sql_server()
    try:
        cursor = conexion.cursor()
        cursor.execute("""
            SELECT IdUsuario, NombreCompleto, CorreoElectronico
            FROM Usuario
            WHERE IdRol = 3
        """)
        return cursor.fetchall()
    except Exception as e:
        print("Error al obtener evaluadores:", e)
        return []
    finally:
        cursor.close()
        conexion.close()

def ObtenerMaterialAsignado():
    conexion = conectar_sql_server()
    try:
        cursor = conexion.cursor()
        cursor.execute("""
            SELECT ME.FechaSubida, ME.NombreArchivo, ME.TipoMaterial, U.NombreCompleto, CONVERT(VARCHAR(19), OM.FechaAsignacion, 120) AS FechaAsignacion  
            FROM ObservacionMaterial OM 
            INNER JOIN MaterialEnseñanza ME ON OM.IdMaterial=ME.IdMaterial 
            INNER JOIN Usuario U ON OM.IdEvaluador=U.IdUsuario
        """)
        return cursor.fetchall()
    except Exception as e:
        print("Error al obtener evaluadores:", e)
        return []
    finally:
        cursor.close()
        conexion.close()

def AsignarTrabajoAEvaluador(IdMaterial, IdEvaluador):
    conexion = conectar_sql_server()
    try:
        cursor = conexion.cursor()
        # Obtener el nuevo IdObservacion (suponiendo que no es autoincremental)
        cursor.execute("SELECT ISNULL(MAX(IdObservacion), 0) + 1 FROM ObservacionMaterial")
        Id = cursor.fetchone()[0]

        consulta = """
            INSERT INTO ObservacionMaterial (IdObservacion, IdMaterial, IdEvaluador, FechaAsignacion)
            VALUES (?, ?, ?, GETDATE())
        """
        cursor.execute(consulta, (Id, IdMaterial, IdEvaluador))
        conexion.commit() 
        return True  # Éxito
    except Exception as e:
        print("Error al asignar:", e)
        return False  # Falló
    finally:
        cursor.close()
        conexion.close()

def ObtenerCorreoEvaluador(idEvaluador):
    conexion = conectar_sql_server()
    try:
        cursor = conexion.cursor()
        consulta = """
            SELECT CorreoElectronico, NombreCompleto
            FROM Usuario
            WHERE IdUsuario = ?
        """
        cursor.execute(consulta, (idEvaluador,))
        fila = cursor.fetchone()
        if fila:
            return fila[0], fila[1]  # (correo, nombre)
        else:
            return None, None
    except Exception as e:
        print("Error al obtener correo del evaluador:", e)
        return None, None
    finally:
        cursor.close()
        conexion.close()


# --- Devoler evaluacion de documentos
def ObtenerDocumentoEvaluador(idEvaluador):
    conexion = conectar_sql_server()
    try:
        cursor = conexion.cursor()
        consulta = """
            SELECT OM.IdObservacion, ME.NombreArchivo 
            FROM ObservacionMaterial OM 
            INNER JOIN MaterialEnseñanza ME ON OM.IdMaterial = ME.IdMaterial 
            WHERE OM.IdEvaluador = ? AND OM.Comentario IS NULL
        """
        cursor.execute(consulta, (idEvaluador,))
        resultados = cursor.fetchall()
        return resultados
    except Exception as e:
        print("Error al obtener documentos del evaluador:", e)
        return []
    finally:
        cursor.close()
        conexion.close()

def ActualizarEvaluacion(id_observacion, estado, observacion):
    conexion = conectar_sql_server()
    try:
        cursor = conexion.cursor()

        if estado == "Aprobado":
            consulta = """
                UPDATE ObservacionMaterial
                SET Comentario = '', FechaObservacion = GETDATE()
                WHERE IdObservacion = ?
            """
            cursor.execute(consulta, (id_observacion,))
        elif estado == "Desaprobado":
            consulta = """
                UPDATE ObservacionMaterial
                SET Comentario = ?, FechaObservacion = GETDATE()
                WHERE IdObservacion = ?
            """
            cursor.execute(consulta, (observacion, id_observacion))

        conexion.commit()
    except Exception as e:
        print("Error al actualizar evaluación:", e)
    finally:
        cursor.close()
        conexion.close()

def ObtenerCorreoDocentePorObservacion(id_observacion):
    conexion = conectar_sql_server()
    try:
        cursor = conexion.cursor()
        consulta = """
            SELECT U.CorreoElectronico, U.NombreCompleto, ME.NombreArchivo
            FROM ObservacionMaterial OM
            INNER JOIN MaterialEnseñanza ME ON OM.IdMaterial = ME.IdMaterial
            INNER JOIN Portafolio P ON ME.IdPortafolio = P.IdPortafolio
            INNER JOIN PortafolioUsuario PU ON P.IdPortafolio = PU.IdPortafolio
            INNER JOIN Usuario U ON PU.IdUsuario = U.IdUsuario
            WHERE OM.IdObservacion = ?
        """
        cursor.execute(consulta, (id_observacion,))
        resultado = cursor.fetchone()
        return resultado  # correo, nombre docente, nombre archivo
    except Exception as e:
        print("Error al obtener datos del docente:", e)
        return None
    finally:
        cursor.close()
        conexion.close()


