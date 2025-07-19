CREATE TABLE ObservacionMaterial (
    IdObservacion INT PRIMARY KEY,
    IdMaterial INT,
    IdEvaluador INT,
    Comentario TEXT,
    FechaObservacion DATE,
	FechaAsignacion DATETIME,
    FOREIGN KEY (IdMaterial) REFERENCES MaterialEnseñanza(IdMaterial),
    FOREIGN KEY (IdEvaluador) REFERENCES Usuario(IdUsuario)
);

-- Tabla Silabo arreglos
DROP TABLE Silabo;

CREATE TABLE Silabo (
    IdSilabo INT IDENTITY(1,1) PRIMARY KEY,
    IdPortafolio INT,
    TipoSilabo VARCHAR(50),
    NombreArchivo VARCHAR(200),
    RutaArchivo VARCHAR(300),
    FechaSubida DATE,
    FOREIGN KEY (IdPortafolio) REFERENCES Portafolio(IdPortafolio)
);

-- Tabla necesaria para crear la copia de seguridad
CREATE TABLE BackupRegistro (
    IdBackup INT PRIMARY KEY,
    NombreArchivo VARCHAR(200),
    RutaArchivo VARCHAR(300),
    FechaBackup DATETIME,
    TamañoMB FLOAT,
    IdUsuario INT,
    FOREIGN KEY (IdUsuario) REFERENCES Usuario(IdUsuario)
);
