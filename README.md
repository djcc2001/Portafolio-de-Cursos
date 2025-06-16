# Portafolio de Cursos - Sistema de Gestión Académica

## Descripción

Este proyecto es un sistema de gestión de portafolios de cursos diseñado para facilitar la administración de material de enseñanza, la asignación de roles (Administrador, Docente, Evaluador), y el proceso de evaluación de trabajos. Permite a los administradores gestionar usuarios y portafolios, a los docentes subir material, y a los evaluadores revisar y comentar los trabajos asignados.

## Características Principales

*   **Gestión de Usuarios:**
    *   Creación, listado, edición y eliminación de usuarios.
    *   Asignación de roles (Administrador, Docente, Evaluador).
    *   Recuperación de contraseña mediante código enviado por correo electrónico.
*   **Gestión de Portafolios:**
    *   Creación de portafolios asociados a cursos y semestres.
    *   Asignación de docentes responsables y evaluadores a los portafolios.
*   **Gestión de Material de Enseñanza:**
    *   (Funcionalidad futura o en desarrollo: Subida de material por parte de docentes).
    *   Asignación de material de enseñanza a evaluadores específicos.
*   **Proceso de Evaluación:**
    *   Los evaluadores pueden revisar el material asignado.
    *   (Funcionalidad futura o en desarrollo: Registrar observaciones y estado de evaluación (Aprobado/Desaprobado)).
    *   Notificaciones por correo electrónico para asignaciones y resultados de evaluación.
*   **Interfaz Diferenciada por Roles:**
    *   Cada rol (Administrador, Docente, Evaluador) tiene acceso a diferentes funcionalidades y vistas.

## Tecnologías Utilizadas

*   **Backend:** Python con Flask
*   **Frontend:** HTML, CSS, JavaScript, Bootstrap
*   **Base de Datos:** Microsoft SQL Server (a través de `pyodbc`)
*   **Notificaciones:** `smtplib` para envío de correos electrónicos.

## Configuración del Entorno

1.  **Clonar el repositorio:**
    ```bash
    git clone <URL_DEL_REPOSITORIO>
    cd Portafolio-de-Cursos
    ```
2.  **Crear un entorno virtual (recomendado):**
    ```bash
    python -m venv venv
    venv\Scripts\activate  # En Windows
    # source venv/bin/activate  # En macOS/Linux
    ```
3.  **Instalar dependencias:**
    ```bash
    pip install -r Requerimientos.txt
    ```
4.  **Configurar la conexión a la base de datos:**
    *   Crea un archivo `Data/conexion.py`. Este archivo está ignorado por Git (`.gitignore`) y debe contener tu función `conectar_sql_server()` con las credenciales y detalles de conexión a tu instancia de SQL Server.
    *   Ejemplo de `Data/conexion.py`:
        ```python
        import pyodbc

        def conectar_sql_server():
            try:
                conexion = pyodbc.connect(
                    'DRIVER={SQL Server};'
                    'SERVER=TU_SERVIDOR;'
                    'DATABASE=TU_BASE_DE_DATOS;'
                    'UID=TU_USUARIO;'
                    'PWD=TU_CONTRASEÑA;'
                )
                print("Conexión exitosa a SQL Server")
                return conexion
            except Exception as e:
                print(f"Error al conectar a SQL Server: {e}")
                return None
        ```
5.  **Crear la base de datos y tablas:**
    *   Asegúrate de tener una base de datos creada en tu SQL Server.
    *   Utiliza los scripts SQL proporcionados (`Data/CrearDB.sql` y `Data/CambiosDB.sql`) para configurar el esquema de la base de datos.

## Cómo Ejecutar la Aplicación

Una vez configurado el entorno y la base de datos, puedes ejecutar la aplicación con:

```bash
python index.py
```

La aplicación estará disponible por defecto en `http://127.0.0.1:5000/`.

## Estructura del Proyecto

```
Portafolio-de-Cursos/
├── Business/               # Lógica de negocio y controladores
│   ├── controlador_usuarios.py
│   └── EmailSender.py
├── Data/                   # Acceso a datos y scripts SQL
│   ├── conexion.py         # (Debe crearse localmente)
│   ├── cUsuario.py
│   ├── CrearDB.sql
│   └── CambiosDB.sql
├── Presentacion/           # Plantillas HTML (vistas)
│   ├── base.html
│   ├── IniciarSesion.html
│   └── ... (otras plantillas)
├── static/                 # Archivos estáticos (CSS, JS, imágenes)
│   ├── css/
│   └── js/
├── .gitignore
├── index.py                # Punto de entrada de la aplicación
├── README.md
└── Requerimientos.txt      # Dependencias de Python
```

## Autores

*   OSCAR DAVID BARRIENTOS HUILLCA
*   DENIS JAIR CANCINAS CARDENAS
*   BRAYAN RODRIGO QUISPE CASTILLO
*   JOHAM ESAU QUISPE HUILLCA
*   RICHARD RODRIGUEZ HUAYLLA

---
