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