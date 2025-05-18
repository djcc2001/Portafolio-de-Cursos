-- Crear la base de datos
use master 
go

Create DATABASE DBPortafolioCursos  -- Creates the Almacenes DataBase
on
  (NAME = DBPortafolioCursos,    -- Primary data file
  FILENAME = 'D:\db\DBPortafolioCursos.mdf',
  SIZE = 5MB,
  FILEGROWTH = 1MB
  )
  LOG ON
  (NAME = DBPortafolioCursos_Log,   -- Log file
  FILENAME = 'D:\db\DBPortafolioCursos.ldf',
  SIZE = 5MB,
  FILEGROWTH = 1MB
  )
go

USE DBPortafolioCursos;
GO

-- Tabla Rol
CREATE TABLE Rol (
    IdRol INT PRIMARY KEY,
    NombreRol VARCHAR(100)
);

-- Tabla Usuario
CREATE TABLE Usuario (
    IdUsuario INT PRIMARY KEY,
    NombreCompleto VARCHAR(200),
    CorreoElectronico VARCHAR(100),
    Contrasenia VARCHAR(200),
    IdRol INT,
    FOREIGN KEY (IdRol) REFERENCES Rol(IdRol)
);

-- Tabla Curso
CREATE TABLE Curso (
    IdCurso INT PRIMARY KEY,
    NombreCurso VARCHAR(100),
    CodigoCurso VARCHAR(50)
);

-- Tabla Semestre
CREATE TABLE Semestre (
    IdSemestre INT PRIMARY KEY,
    Nombre VARCHAR(50),
    FechaInicio DATE,
    FechaFin DATE
);

-- Tabla Portafolio
CREATE TABLE Portafolio (
    IdPortafolio INT PRIMARY KEY,
    IdCurso INT,
    IdSemestre INT,
    Estado VARCHAR(50),
    FOREIGN KEY (IdCurso) REFERENCES Curso(IdCurso),
    FOREIGN KEY (IdSemestre) REFERENCES Semestre(IdSemestre)
);

-- Tabla PortafolioUsuario
CREATE TABLE PortafolioUsuario (
    IdPortafolioUsuario INT PRIMARY KEY,
    IdPortafolio INT,
    IdUsuario INT,
    RolEnPortafolio VARCHAR(50),
    FOREIGN KEY (IdPortafolio) REFERENCES Portafolio(IdPortafolio),
    FOREIGN KEY (IdUsuario) REFERENCES Usuario(IdUsuario)
);

-- Tabla MaterialEnse�anza
CREATE TABLE MaterialEnse�anza (
    IdMaterial INT PRIMARY KEY,
    IdPortafolio INT,
    TipoMaterial VARCHAR(50),
    NombreArchivo VARCHAR(200),
    RutaArchivo VARCHAR(300),
    FechaSubida DATE,
    FOREIGN KEY (IdPortafolio) REFERENCES Portafolio(IdPortafolio)
);

-- Tabla Silabo
CREATE TABLE Silabo (
    IdSilabo INT PRIMARY KEY,
    IdPortafolio INT,
    TipoSilabo VARCHAR(50),
    NombreArchivo VARCHAR(200),
    RutaArchivo VARCHAR(300),
    FechaSubida DATE,
    FOREIGN KEY (IdPortafolio) REFERENCES Portafolio(IdPortafolio)
);

-- Tabla TrabajoEstudiantil
CREATE TABLE TrabajoEstudiantil (
    IdTrabajo INT PRIMARY KEY,
    IdPortafolio INT,
    Categoria VARCHAR(50),
    NombreArchivo VARCHAR(200),
    RutaArchivo VARCHAR(300),
    FechaSubida DATE,
    FOREIGN KEY (IdPortafolio) REFERENCES Portafolio(IdPortafolio)
);

-- Tabla Observacion
CREATE TABLE Observacion (
    IdObservacion INT PRIMARY KEY,
    IdTrabajo INT,
    IdEvaluador INT,
    Comentario TEXT,
    FechaObservacion DATE,
    FOREIGN KEY (IdTrabajo) REFERENCES TrabajoEstudiantil(IdTrabajo),
    FOREIGN KEY (IdEvaluador) REFERENCES Usuario(IdUsuario)
);

-- Tabla RegistroEliminacion
CREATE TABLE RegistroEliminacion (
    IdRegistro INT PRIMARY KEY,
    TipoDocumento VARCHAR(50),
    NombreArchivo VARCHAR(200),
    IdUsuario INT,
    FechaEliminacion DATE,
    FOREIGN KEY (IdUsuario) REFERENCES Usuario(IdUsuario)
);
