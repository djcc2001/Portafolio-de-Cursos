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

-- Tabal Silabo arreglos
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