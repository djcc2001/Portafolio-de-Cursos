from Data.conexion import conectar_sql_server

import os
from datetime import datetime
from werkzeug.utils import secure_filename
from .conexion import conectar_sql_server
import os

# Obtén la ruta absoluta del proyecto
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'public', 'materiales')
UPLOAD_FOLDER_SILABO = os.path.join(BASE_DIR, 'public', 'silabos')

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


# --- Funciones para Crear Portafolios ---

def _obtener_o_crear_curso(nombre_curso, conexion, cursor):
    try:
        cursor.execute("SELECT IdCurso FROM Curso WHERE NombreCurso = ?", (nombre_curso,))
        curso_existente = cursor.fetchone()
        if curso_existente:
            return curso_existente[0]
        else:
            cursor.execute("SELECT ISNULL(MAX(IdCurso), 0) + 1 FROM Curso")
            nuevo_id_curso = cursor.fetchone()[0]
            codigo_curso = nombre_curso.replace(" ", "").upper()[:20] # Código simple
            cursor.execute("INSERT INTO Curso (IdCurso, NombreCurso, CodigoCurso) VALUES (?, ?, ?)",
                           (nuevo_id_curso, nombre_curso, codigo_curso))
            return nuevo_id_curso
    except Exception as e:
        print(f"Error en _obtener_o_crear_curso: {e}")
        return None

def _obtener_o_crear_semestre(nombre_semestre, conexion, cursor):
    try:
        cursor.execute("SELECT IdSemestre FROM Semestre WHERE Nombre = ?", (nombre_semestre,))
        semestre_existente = cursor.fetchone()
        if semestre_existente:
            return semestre_existente[0]
        else:
            cursor.execute("SELECT ISNULL(MAX(IdSemestre), 0) + 1 FROM Semestre")
            nuevo_id_semestre = cursor.fetchone()[0]
            # Fechas por defecto o NULL si la BD lo permite
            cursor.execute("INSERT INTO Semestre (IdSemestre, Nombre, FechaInicio, FechaFin) VALUES (?, ?, NULL, NULL)",
                           (nuevo_id_semestre, nombre_semestre))
            return nuevo_id_semestre
    except Exception as e:
        print(f"Error en _obtener_o_crear_semestre: {e}")
        return None

def _crear_nuevo_portafolio_db(id_curso, id_semestre, estado, conexion, cursor):
    try:
        cursor.execute("SELECT IdPortafolio FROM Portafolio WHERE IdCurso = ? AND IdSemestre = ?", (id_curso, id_semestre))
        if cursor.fetchone():
            print("Portafolio ya existe para este curso y semestre.")
            return None # Indica que ya existe

        cursor.execute("SELECT ISNULL(MAX(IdPortafolio), 0) + 1 FROM Portafolio")
        nuevo_id_portafolio = cursor.fetchone()[0]
        cursor.execute("INSERT INTO Portafolio (IdPortafolio, IdCurso, IdSemestre, Estado) VALUES (?, ?, ?, ?)",
                       (nuevo_id_portafolio, id_curso, id_semestre, estado))
        return nuevo_id_portafolio
    except Exception as e:
        print(f"Error en _crear_nuevo_portafolio_db: {e}")
        return None

def CrearPortafolioCompleto(nombre_curso_input, nombre_semestre_input, estado_portafolio):
    conexion = conectar_sql_server()
    if not conexion: return False
    cursor = conexion.cursor()
    try:
        id_curso = _obtener_o_crear_curso(nombre_curso_input, conexion, cursor)
        if not id_curso:
            conexion.rollback()
            return False

        id_semestre = _obtener_o_crear_semestre(nombre_semestre_input, conexion, cursor)
        if not id_semestre:
            conexion.rollback()
            return False
        
        id_nuevo_portafolio = _crear_nuevo_portafolio_db(id_curso, id_semestre, estado_portafolio, conexion, cursor)
        if not id_nuevo_portafolio:
            conexion.rollback() # Podría ser porque ya existe o por error
            return False

        conexion.commit()
        return True
    except Exception as e:
        print(f"Error en CrearPortafolioCompleto: {e}")
        conexion.rollback()
        return False
    finally:
        cursor.close()
        conexion.close()

def ListarPortafoliosConDetalles():
    conexion = conectar_sql_server()
    if not conexion: return []
    cursor = conexion.cursor()
    try:
        query = """
            SELECT 
                P.IdPortafolio, 
                C.NombreCurso, 
                S.Nombre AS NombreSemestre,
                P.Estado,
                CONCAT('Portafolio_', P.IdPortafolio) AS NombreCalculadoPortafolio
            FROM Portafolio P
            JOIN Curso C ON P.IdCurso = C.IdCurso
            JOIN Semestre S ON P.IdSemestre = S.IdSemestre
            ORDER BY P.IdPortafolio DESC;
        """
        cursor.execute(query)
        portafolios_raw = cursor.fetchall()
        lista_portafolios = []
        for row in portafolios_raw:
            lista_portafolios.append({
                'id': row[0],
                'nombre_curso': row[1],
                'nombre_semestre': row[2],
                'estado': row[3],
                'nombre_calculado': row[4]
            })
        return lista_portafolios
    except Exception as e:
        print(f"Error en ListarPortafoliosConDetalles: {e}")
        return []
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

# Funcion para obtener semestres
def obtener_semestres():
    conexion = conectar_sql_server()
    with conexion.cursor() as cursor:
        cursor.execute("SELECT IdSemestre, Nombre FROM Semestre ORDER BY FechaInicio DESC")
        return cursor.fetchall()

# Funcion para obtener los portafolios por semestre
def obtener_portafolios_por_semestre(id_semestre=None, id_docente=None):
    conexion = conectar_sql_server()
    with conexion.cursor() as cursor:
        if id_semestre:
            cursor.execute("""
                DECLARE @IdUsuario INT = ?;      
                DECLARE @IdSemestre VARCHAR = ?; -- ID del semestre (reemplaza con el valor deseado)

                SELECT P.IdPortafolio, C.NombreCurso, S.Nombre AS Semestre, P.Estado
                FROM Portafolio P
                JOIN Curso C ON P.IdCurso = C.IdCurso
                JOIN Semestre S ON P.IdSemestre = S.IdSemestre
                LEFT JOIN PortafolioUsuario PU ON P.IdPortafolio = PU.IdPortafolio
                LEFT JOIN Usuario U ON PU.IdUsuario = U.IdUsuario
                LEFT JOIN Rol R ON U.IdRol = R.IdRol
                WHERE 
                    P.IdSemestre = @IdSemestre
                    AND (
                        -- Si es docente, mostrar solo sus portafolios
                        (
                            @IdUsuario IN (
                                SELECT U2.IdUsuario
                                FROM Usuario U2
                                JOIN Rol R2 ON U2.IdRol = R2.IdRol
                                WHERE R2.NombreRol = 'Docente'
                            )
                            AND PU.IdUsuario = @IdUsuario
                        )
                        OR
                        -- Si no es docente, mostrar todo
                        (
                            @IdUsuario NOT IN (
                                SELECT U2.IdUsuario
                                FROM Usuario U2
                                JOIN Rol R2 ON U2.IdRol = R2.IdRol
                                WHERE R2.NombreRol = 'Docente'
                            )
                        )
                    );

            """, (id_docente, id_semestre))
        else:
            cursor.execute("""
                DECLARE @IdUsuario INT = ?; 
                SELECT P.IdPortafolio, C.NombreCurso, S.Nombre AS Semestre, P.Estado
                FROM Portafolio P
                JOIN Curso C ON P.IdCurso = C.IdCurso
                JOIN Semestre S ON P.IdSemestre = S.IdSemestre
                LEFT JOIN PortafolioUsuario PU ON P.IdPortafolio = PU.IdPortafolio
                LEFT JOIN Usuario U ON PU.IdUsuario = U.IdUsuario
                LEFT JOIN Rol R ON U.IdRol = R.IdRol
                WHERE 
                    (
                        -- Si el usuario es docente, filtrar por sus portafolios
                        @IdUsuario IN (
                            SELECT U2.IdUsuario
                            FROM Usuario U2
                            JOIN Rol R2 ON U2.IdRol = R2.IdRol
                            WHERE R2.NombreRol = 'Docente'
                        )
                        AND PU.IdUsuario = @IdUsuario
                    )
                    OR
                    (
                        -- Si no es docente, mostrar todos
                        @IdUsuario NOT IN (
                            SELECT U2.IdUsuario
                            FROM Usuario U2
                            JOIN Rol R2 ON U2.IdRol = R2.IdRol
                            WHERE R2.NombreRol = 'Docente'
                        )
                    );
            """, (id_docente,))
        return cursor.fetchall()

# Funcion para obtener archivos de la tabla Portafolio por IdPortafolio
def obtener_archivos_portafolio(id_portafolio):
    conexion = conectar_sql_server()
    with conexion.cursor() as cursor:
        cursor.execute("""
            SELECT Id, Tipo, NombreArchivo, RutaArchivo, FechaSubida
            FROM (
                SELECT 1 AS Orden, IdSilabo AS Id, TipoSilabo AS Tipo, NombreArchivo, RutaArchivo, FechaSubida
                FROM Silabo
                WHERE IdPortafolio = ?

                UNION ALL

                SELECT 2 AS Orden, IdMaterial AS Id, TipoMaterial AS Tipo, NombreArchivo, RutaArchivo, FechaSubida
                FROM MaterialEnseñanza
                WHERE IdPortafolio = ?
            ) AS Combinado
            ORDER BY  Orden, CASE WHEN Orden = 2 THEN FechaSubida END DESC;
        """, (id_portafolio, id_portafolio))
        return cursor.fetchall()


# Cambiar el estado del portafolio (a Completo o Incompleto)
def MarcarEstadoPortafolio(id_portafolio, nuevo_estado, modificado_por=None):
    conexion = conectar_sql_server()
    try:
        cursor = conexion.cursor()

        cursor.execute("""
            SELECT COUNT(*) FROM (
                SELECT IdMaterial FROM MaterialEnseñanza WHERE IdPortafolio = ?
                UNION ALL
                SELECT IdSilabo FROM Silabo WHERE IdPortafolio = ?
                UNION ALL
                SELECT IdTrabajo FROM TrabajoEstudiantil WHERE IdPortafolio = ?
            ) AS ArchivosSubidos
        """, (id_portafolio, id_portafolio, id_portafolio))
        total_archivos = cursor.fetchone()[0]

        if nuevo_estado == 'Completo' and total_archivos == 0:
            return "FALTAN_DATOS"

        # Solo se actualiza el estado
        cursor.execute("""
            UPDATE Portafolio
            SET Estado = ?
            WHERE IdPortafolio = ?
        """, (nuevo_estado, id_portafolio))

        conexion.commit()
        return True
    except Exception as e:
        print(f"Error al cambiar estado del portafolio: {e}")
        return False
    finally:
        cursor.close()
        conexion.close()

def ActualizarEstadoPortafolio(id_portafolio, nuevo_estado):
    conexion = conectar_sql_server()
    cursor = conexion.cursor()
    cursor.execute("UPDATE Portafolio SET Estado = ? WHERE IdPortafolio = ?", (nuevo_estado, id_portafolio))
    conexion.commit()
    cursor.close()
    conexion.close()

def obtener_portafolios_con_faltantes():
    conexion = conectar_sql_server()
    cursor = conexion.cursor()
    cursor.execute("""
        SELECT 
            P.IdPortafolio,
            C.NombreCurso,
            S.Nombre AS NombreSemestre,
            P.Estado,
            ISNULL((
                SELECT STRING_AGG(f.NombreArchivo, ', ')
                FROM (
                    SELECT NombreArchivo FROM MaterialEnseñanza 
                    WHERE IdPortafolio = P.IdPortafolio AND FechaSubida IS NULL

                    UNION ALL

                    SELECT NombreArchivo FROM Silabo 
                    WHERE IdPortafolio = P.IdPortafolio AND FechaSubida IS NULL

                    UNION ALL

                    SELECT NombreArchivo FROM TrabajoEstudiantil 
                    WHERE IdPortafolio = P.IdPortafolio AND FechaSubida IS NULL
                ) AS f
            ), '') AS Faltantes
        FROM Portafolio P
        JOIN Curso C ON C.IdCurso = P.IdCurso
        JOIN Semestre S ON S.IdSemestre = P.IdSemestre
    """)
    datos = cursor.fetchall()

    lista = []
    for fila in datos:
        id_portafolio = fila[0]

        # Obtener archivos subidos para ese portafolio
        cursor.execute("""
            SELECT NombreArchivo FROM MaterialEnseñanza 
            WHERE IdPortafolio = ? AND FechaSubida IS NOT NULL
            UNION
            SELECT NombreArchivo FROM Silabo 
            WHERE IdPortafolio = ? AND FechaSubida IS NOT NULL
            UNION
            SELECT NombreArchivo FROM TrabajoEstudiantil 
            WHERE IdPortafolio = ? AND FechaSubida IS NOT NULL
        """, (id_portafolio, id_portafolio, id_portafolio))
        subidos = [r[0] for r in cursor.fetchall()]

        lista.append({
            'id': fila[0],
            'nombre': fila[1],
            'semestre': fila[2],
            'estado': fila[3],
            'faltantes': fila[4] if fila[4] else None,
            'subidos': subidos  # 🔥 Agregamos esto
        })

    cursor.close()
    conexion.close()
    return lista
# -- Subir material de enseñanza
def guardar_material_ensenanza(id_portafolio, tipo_material, archivo_storage):
    nombre_archivo = secure_filename(archivo_storage.filename)
    ruta_guardado = os.path.join(UPLOAD_FOLDER, nombre_archivo)

    # Crear la carpeta si no existe
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)

    archivo_storage.save(ruta_guardado)

    conexion = conectar_sql_server()
    with conexion.cursor() as cursor:
        cursor.execute("SELECT ISNULL(MAX(IdMaterial), 0) + 1 FROM MaterialEnseñanza")
        nuevo_id = cursor.fetchone()[0]

        cursor.execute("""
            INSERT INTO MaterialEnseñanza (IdMaterial, IdPortafolio, TipoMaterial, NombreArchivo, RutaArchivo, FechaSubida)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (nuevo_id, id_portafolio, tipo_material, nombre_archivo, ruta_guardado, datetime.now()))

        conexion.commit()


# eliminar usuario
def eliminar_material_U(id_portafolio, nombre_archivo, tipo_material, id_usuario):
    try:
        conn = conectar_sql_server()
        cursor = conn.cursor()
        
        print(f"DEBUG - Valores recibidos para eliminar:")
        print(f"Portafolio: {id_portafolio}")
        print(f"Archivo: '{nombre_archivo}'")
        print(f"Tipo: '{tipo_material}'")
        
        # Consulta con comparación exacta
        cursor.execute("""
            SELECT IdMaterial, RutaArchivo 
            FROM MaterialEnseñanza 
            WHERE IdPortafolio = ? 
            AND NombreArchivo = ?
            AND TipoMaterial = ?
        """, (id_portafolio, nombre_archivo, tipo_material))
        
        resultado = cursor.fetchone()
        
        if not resultado:
            print("\nERROR: No se encontró coincidencia exacta. Valores en BD:")
            cursor.execute("""
                SELECT TipoMaterial, NombreArchivo 
                FROM MaterialEnseñanza 
                WHERE IdPortafolio = ?
            """, (id_portafolio,))
            for row in cursor.fetchall():
                print(f"- Tipo: '{row[0]}', Archivo: '{row[1]}'")
            return False
        
        id_material, ruta_archivo = resultado
        
        # Eliminar observaciones relacionadas primero
        cursor.execute("DELETE FROM ObservacionMaterial WHERE IdMaterial = ?", (id_material,))
        
        # Eliminar el material principal
        cursor.execute("DELETE FROM MaterialEnseñanza WHERE IdMaterial = ?", (id_material,))
        
        # Obtener nuevo ID para RegistroEliminacion
        cursor.execute("SELECT ISNULL(MAX(IdRegistro), 0) + 1 FROM RegistroEliminacion")
        nuevo_id = cursor.fetchone()[0]
        
        # Registrar eliminación
        cursor.execute("""
            INSERT INTO RegistroEliminacion 
            (IdRegistro, TipoDocumento, NombreArchivo, IdUsuario, FechaEliminacion)
            VALUES (?, ?, ?, ?, ?)
        """, (nuevo_id, 'MaterialEnseñanza', nombre_archivo, id_usuario, datetime.now().date()))
        
        # Eliminar archivo físico
        if ruta_archivo and os.path.exists(ruta_archivo):
            try:
                os.remove(ruta_archivo)
                print(f"Archivo físico eliminado: {ruta_archivo}")
            except Exception as e:
                print(f"Error al eliminar archivo físico: {str(e)}")
        
        conn.commit()
        return True
        
    except Exception as e:
        print(f"Error durante eliminación: {str(e)}")
        conn.rollback()
        return False
    finally:
        if conn:
            conn.close()

# Funcion para obtener silabos por tipo (ICACIT o UNSAAC)
def obtener_silabos_por_tipo(tipo_silabo):
    conexion = conectar_sql_server()
    try:
        print(f"Consultando sílabos con tipo: '{tipo_silabo}'")  # DEPURACIÓN
        cursor = conexion.cursor()
        cursor.execute("""
            SELECT S.TipoSilabo, S.NombreArchivo, S.RutaArchivo, S.FechaSubida, S.IdSilabo
            FROM Silabo S
            WHERE S.TipoSilabo = ?
        """, (tipo_silabo,))
        resultados = cursor.fetchall()
        return resultados
    except Exception as e:
        print("Error al obtener sílabos:", e)
        return []
    finally:
        cursor.close()
        conexion.close()

# Funcion para guardar un silabo luego de ser subido
def guardar_silabo(id_portafolio, tipo_silabo, archivo_storage):
    nombre_archivo = secure_filename(archivo_storage.filename)
    ruta_guardado = os.path.join(UPLOAD_FOLDER_SILABO, nombre_archivo)

    # Crear la carpeta si no existe
    os.makedirs(UPLOAD_FOLDER_SILABO, exist_ok=True)

    archivo_storage.save(ruta_guardado)

    conexion = conectar_sql_server()
    with conexion.cursor() as cursor:
        cursor.execute("SELECT ISNULL(MAX(IdSilabo), 0) + 1 FROM Silabo")
        nuevo_id = cursor.fetchone()[0]

        cursor.execute("""
            INSERT INTO Silabo (IdPortafolio, TipoSilabo, NombreArchivo, RutaArchivo, FechaSubida)
            VALUES (?, ?, ?, ?, ?)
        """, (id_portafolio, tipo_silabo, nombre_archivo, ruta_guardado, datetime.now()))

        conexion.commit()

# Funcion para eliminar un silabo de la base de datos
from datetime import datetime

def eliminar_silabo_U(id_silabo, nombre_archivo, tipo_silabo, id_usuario):
    try:
        conn = conectar_sql_server()
        cursor = conn.cursor()

        # Buscar la ruta del sílabo
        cursor.execute("""
            SELECT RutaArchivo 
            FROM Silabo 
            WHERE IdSilabo = ?
        """, (id_silabo,))
        resultado = cursor.fetchone()
        if not resultado:
            print("No se encontró el sílabo.")
            return False

        ruta_archivo_relativa = resultado[0]
        if not os.path.isabs(ruta_archivo_relativa):
            ruta_archivo = os.path.join(BASE_DIR, ruta_archivo_relativa.replace('/', os.sep))
        else:
            ruta_archivo = ruta_archivo_relativa

        # Eliminar el registro de la base de datos
        cursor.execute("DELETE FROM Silabo WHERE IdSilabo = ?", (id_silabo,))

        # Registrar eliminación (opcional)
        cursor.execute("SELECT ISNULL(MAX(IdRegistro), 0) + 1 FROM RegistroEliminacion")
        nuevo_id = cursor.fetchone()[0]
        fecha_hoy = datetime.now().strftime('%Y-%m-%d')  # <-- CAMBIO AQUÍ

        cursor.execute("""
            INSERT INTO RegistroEliminacion (IdRegistro, TipoDocumento, NombreArchivo, IdUsuario, FechaEliminacion)
            VALUES (?, ?, ?, ?, ?)
        """, (nuevo_id, 'Silabo', nombre_archivo, id_usuario, fecha_hoy))

        # Eliminar archivo físico
        if ruta_archivo and os.path.exists(ruta_archivo):
            try:
                os.remove(ruta_archivo)
                print(f"Archivo eliminado: {ruta_archivo}")
            except Exception as e:
                print(f"Error al eliminar archivo físico: {str(e)}")

        conn.commit()
        return True

    except Exception as e:
        print(f"Error eliminando silabo: {str(e)}")
        if conn:
            conn.rollback()
        return False
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()
# ver trabajo estudiantil
def obtener_trabajos_estudiantiles(id_portafolio):
    conexion = conectar_sql_server()
    with conexion.cursor() as cursor:
        cursor.execute("""
            SELECT IdTrabajo, Categoria, NombreArchivo, RutaArchivo, FechaSubida
            FROM TrabajoEstudiantil
            WHERE IdPortafolio = ?
            ORDER BY FechaSubida DESC
        """, (id_portafolio,))
        return cursor.fetchall()


# eliminar trabajo estudiantil
from datetime import date
def eliminar_trabajo_estudiantil(id_trabajo, nombre_archivo, categoria, id_usuario, id_portafolio):
    try:
        conn = conectar_sql_server()
        cursor = conn.cursor()

        # Buscar ruta absoluta del archivo usando el ID del trabajo
        cursor.execute("""
            SELECT RutaArchivo FROM TrabajoEstudiantil
            WHERE IdTrabajo = ?
        """, (id_trabajo,))
        fila = cursor.fetchone()

        if not fila:
            return {'exito': False, 'error': 'Archivo no encontrado en la base de datos'}

        ruta_absoluta = fila[0]
        # Eliminar archivo físico si existe
        if ruta_absoluta and os.path.exists(ruta_absoluta):
            try:
                os.remove(ruta_absoluta)
            except Exception as e:
                print(f"Error al eliminar archivo físico: {str(e)}")

        # Eliminar registro de TrabajoEstudiantil
        cursor.execute("""
            DELETE FROM TrabajoEstudiantil
            WHERE IdTrabajo = ?
        """, (id_trabajo,))

        # Insertar en RegistroEliminacion
        cursor.execute("SELECT ISNULL(MAX(IdRegistro), 0) + 1 FROM RegistroEliminacion")
        nuevo_id = cursor.fetchone()[0]
        from datetime import date
        fecha_hoy = date.today().strftime('%Y-%m-%d')  # <-- Convertir a string

        cursor.execute("""
            INSERT INTO RegistroEliminacion 
            (IdRegistro, TipoDocumento, NombreArchivo, IdUsuario, FechaEliminacion)
            VALUES (?, ?, ?, ?, ?)
        """, (nuevo_id, 'TrabajoEstudiantil', nombre_archivo, id_usuario, fecha_hoy))

        conn.commit()
        return {'exito': True}
    except Exception as e:
        return {'exito': False, 'error': str(e)}
    finally:
        if conn:
            conn.close()

def listar_estudiantes():
    conexion = conectar_sql_server()
    try:
        cursor = conexion.cursor()
        cursor.execute("SELECT IdEstudiante, NombreCompleto FROM Estudiante")
        return cursor.fetchall()
    except Exception as e:
        print("Error al listar estudiantes:", e)
        return []
    finally:
        cursor.close()
        conexion.close()

def guardar_trabajo_estudiantil(id_portafolio, id_estudiante, categoria, archivo_storage):
    from werkzeug.utils import secure_filename
    nombre_archivo = secure_filename(archivo_storage.filename)
    if not nombre_archivo.lower().endswith('.pdf'):
        return {'exito': False, 'error': 'Solo se permiten archivos PDF'}
    if archivo_storage.content_length and archivo_storage.content_length > 5 * 1024 * 1024:
        return {'exito': False, 'error': 'El archivo supera los 5MB'}

    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    UPLOAD_FOLDER = os.path.join(BASE_DIR, 'public', 'trabajos_estudiantiles')
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    ruta_guardado = os.path.join(UPLOAD_FOLDER, nombre_archivo)
    archivo_storage.save(ruta_guardado)

    conexion = conectar_sql_server()
    try:
        cursor = conexion.cursor()
        cursor.execute("SELECT ISNULL(MAX(IdTrabajo), 0) + 1 FROM TrabajoEstudiantil")
        nuevo_id = cursor.fetchone()[0]
        cursor.execute("""
            INSERT INTO TrabajoEstudiantil (IdTrabajo, IdPortafolio, IdEstudiante, Categoria, NombreArchivo, RutaArchivo, FechaSubida)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (nuevo_id, id_portafolio, id_estudiante, categoria, nombre_archivo, ruta_guardado, datetime.now()))
        conexion.commit()
        return {'exito': True}
    except Exception as e:
        print("Error al guardar trabajo estudiantil:", e)
        return {'exito': False, 'error': str(e)}
    finally:
        cursor.close()
        conexion.close()

def obtener_siguiente_id_estudiante():
    conexion = conectar_sql_server()
    try:
        cursor = conexion.cursor()
        cursor.execute("SELECT ISNULL(MAX(IdEstudiante), 0) + 1 FROM Estudiante")
        nuevo_id = cursor.fetchone()[0]
        # Insertar el estudiante si no existe
        cursor.execute("INSERT INTO Estudiante (IdEstudiante, NombreCompleto) VALUES (?, ?)", (nuevo_id, f"Estudiante {nuevo_id}"))
        conexion.commit()
        return nuevo_id
    except Exception as e:
        print("Error al obtener/crear estudiante:", e)
        return 1
    finally:
        cursor.close()
        conexion.close()

def obtener_trabajos_estudiantiles_filtrado(id_portafolio, categoria=None, id_estudiante=None):
    conexion = conectar_sql_server()
    try:
        cursor = conexion.cursor()
        query = """
            SELECT T.IdTrabajo, T.IdEstudiante, T.Categoria, T.NombreArchivo, T.RutaArchivo, T.FechaSubida
            FROM TrabajoEstudiantil T
            WHERE T.IdPortafolio = ?
        """
        params = [id_portafolio]
        if categoria:
            query += " AND T.Categoria = ?"
            params.append(categoria)
        if id_estudiante:
            query += " AND T.IdEstudiante = ?"
            params.append(id_estudiante)
        query += " ORDER BY T.FechaSubida DESC"
        cursor.execute(query, tuple(params))
        resultados = cursor.fetchall()
        # Devuelve "Estudiante N" en vez de nombre real
        return [(r[0], f"Estudiante {r[1]}", r[2], r[3], r[4], r[5]) for r in resultados]
    except Exception as e:
        print("Error al obtener trabajos estudiantiles filtrados:", e)
        return []
    finally:
        cursor.close()
        conexion.close()