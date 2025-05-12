-- 01_relas_avanzadas.sql

USE COCODE_Gestion;
GO

-- 1) Tabla intermedia Derecho_Cuota
IF OBJECT_ID('dbo.Derecho_Cuota', 'U') IS NULL
BEGIN
  CREATE TABLE dbo.Derecho_Cuota (
    ID_Derecho INT NOT NULL
      CONSTRAINT FK_DC_Derecho FOREIGN KEY REFERENCES Derechos(ID_Derecho),
    ID_Cuota   INT NOT NULL
      CONSTRAINT FK_DC_Cuota   FOREIGN KEY REFERENCES Cuotas(ID_Cuota),
    CONSTRAINT PK_Derecho_Cuota PRIMARY KEY (ID_Derecho, ID_Cuota)
  );
END;
GO

-- 2) Tabla intermedia Persona_Cuota
IF OBJECT_ID('dbo.Persona_Cuota', 'U') IS NULL
BEGIN
  CREATE TABLE dbo.Persona_Cuota (
    ID_Persona INT NOT NULL
      CONSTRAINT FK_PC_Persona FOREIGN KEY REFERENCES Personas(ID_Persona),
    ID_Cuota   INT NOT NULL
      CONSTRAINT FK_PC_Cuota   FOREIGN KEY REFERENCES Cuotas(ID_Cuota),
    Fecha_Asig DATE    NOT NULL,
    Estado     VARCHAR(20) NOT NULL DEFAULT('Pendiente'),
    CONSTRAINT PK_Persona_Cuota PRIMARY KEY (ID_Persona, ID_Cuota)
  );
END;
GO

-- 3) Alterar Pagos para referenciar Persona_Cuota
ALTER TABLE dbo.Pagos
  ADD CONSTRAINT FK_Pago_Persona_Cuota
      FOREIGN KEY (ID_Persona, ID_Cuota)
      REFERENCES dbo.Persona_Cuota(ID_Persona, ID_Cuota);
GO

-- 4) (Opcional) Alterar Ingresos para referenciar Pago
ALTER TABLE dbo.Ingresos
  ADD ID_Pago INT NULL;
GO

ALTER TABLE dbo.Ingresos
  ADD CONSTRAINT FK_Ingreso_Pago
      FOREIGN KEY (ID_Pago) REFERENCES dbo.Pagos(ID_Pago);
GO
