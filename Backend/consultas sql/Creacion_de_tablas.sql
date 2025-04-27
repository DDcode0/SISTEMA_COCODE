
--CREACION DE LAS TABLAS



CREATE TABLE Personas (
    ID_Persona INT PRIMARY KEY IDENTITY(1,1), -- Clave primaria con autoincremento
    DPI VARCHAR(13) NOT NULL UNIQUE,         -- Documento �nico obligatorio
    Nombre VARCHAR(100) NOT NULL,            -- Nombre completo obligatorio
    Direccion VARCHAR(200) NULL,             -- Direcci�n (puede ser opcional)
    Telefono VARCHAR(15) NULL,               -- Tel�fono (opcional)
    Email VARCHAR(100) NULL,                 -- Correo electr�nico (opcional)
    Rol VARCHAR(50) NULL,                    -- Rol dentro de la comunidad (Presidente, Secretario, Tesorero, Miembro)
    Estado BIT NOT NULL                      -- Estado (activo/inactivo)
);


CREATE TABLE Derechos (
    ID_Derecho INT PRIMARY KEY IDENTITY(1,1), -- Clave primaria autoincremental
    Nombre VARCHAR(50) NOT NULL              -- Nombre del derecho (obligatorio)
);

CREATE TABLE Persona_Derecho (
    ID_Persona INT NOT NULL,              -- ID de la persona, no puede ser nulo
    ID_Derecho INT NOT NULL,              -- ID del derecho, no puede ser nulo
    Fecha_Inicio DATE NOT NULL,           -- Fecha obligatoria del inicio del derecho
    Fecha_Fin DATE NULL,                  -- Fecha opcional de revocaci�n del derecho
    PRIMARY KEY (ID_Persona, ID_Derecho), -- Clave primaria compuesta por ambas columnas
    FOREIGN KEY (ID_Persona) REFERENCES Personas(ID_Persona), -- Relaci�n con Personas
    FOREIGN KEY (ID_Derecho) REFERENCES Derechos(ID_Derecho)  -- Relaci�n con Derechos
);

USE COCODE_Gestion;
CREATE TABLE Cuotas (
    ID_Cuota INT PRIMARY KEY IDENTITY(1,1),  -- Clave primaria autoincremental
    Descripcion VARCHAR(100) NOT NULL,       -- Descripci�n de la cuota
    Monto DECIMAL(10,2) NOT NULL,            -- Monto de la cuota
    Fecha_Limite DATE NOT NULL               -- Fecha l�mite para el pago
);

CREATE TABLE Pagos (
    ID_Pago INT PRIMARY KEY IDENTITY(1,1),   -- Clave primaria autoincremental
    ID_Persona INT NOT NULL,                 -- Clave for�nea hacia Personas
    ID_Cuota INT NOT NULL,                   -- Clave for�nea hacia Cuotas
    Fecha_Pago DATE NOT NULL,                -- Fecha del pago
    Monto_Pagado DECIMAL(10,2) NOT NULL,     -- Monto pagado
    Estado VARCHAR(50) NOT NULL,             -- Estado del pago (pendiente, completado)
    FOREIGN KEY (ID_Persona) REFERENCES Personas(ID_Persona), -- Relaci�n con Personas
    FOREIGN KEY (ID_Cuota) REFERENCES Cuotas(ID_Cuota)        -- Relaci�n con Cuotas
);

CREATE TABLE Ingresos (
    ID_Ingreso INT PRIMARY KEY IDENTITY(1,1),  -- Clave primaria autoincremental
    Fecha DATE NOT NULL,                       -- Fecha del ingreso
    Monto DECIMAL(10,2) NOT NULL,              -- Monto recibido
    Fuente VARCHAR(100) NULL,                  -- Descripci�n de la fuente
    Observaciones TEXT NULL                    -- Notas adicionales opcionales
);

CREATE TABLE Egresos (
    ID_Egreso INT PRIMARY KEY IDENTITY(1,1),   -- Clave primaria autoincremental
    Fecha DATE NOT NULL,                       -- Fecha del egreso
    Monto DECIMAL(10,2) NOT NULL,              -- Monto gastado
    Descripcion TEXT NOT NULL                  -- Detalles sobre el gasto
);



USE COCODE_Gestion;

SELECT * FROM Derechos;

ALTER TABLE Personas
ALTER COLUMN Estado VARCHAR(10) NOT NULL;

UPDATE Personas
SET Estado = 'Activo'
WHERE Estado = '1';

UPDATE Personas
SET Estado = 'Inactivo'
WHERE Estado = '0';

ALTER TABLE Persona_Derecho
ADD CONSTRAINT UC_Persona_Derecho UNIQUE (ID_Persona, ID_Derecho);


-- Derechos: Nombre único
ALTER TABLE Derechos
ADD CONSTRAINT UC_Nombre_Derecho UNIQUE (Nombre);

-- Cuotas: Descripción única
ALTER TABLE Cuotas
ADD CONSTRAINT UC_Descripcion_Cuota UNIQUE (Descripcion);

-- Pagos: Combinación única de ID_Persona + ID_Cuota
ALTER TABLE Pagos
ADD CONSTRAINT UC_Pagos UNIQUE (ID_Persona, ID_Cuota);

-- Ingresos: Combinación única de Fecha + Fuente
ALTER TABLE Ingresos
ADD CONSTRAINT UC_Ingresos UNIQUE (Fecha, Fuente);

-- Egresos: Combinación única de Fecha + Descripción
ALTER TABLE Egresos
ADD CONSTRAINT UC_Egresos UNIQUE (Fecha, Descripcion);

-- Persona_Derecho: Combinación única de ID_Persona + ID_Derecho
ALTER TABLE Persona_Derecho
ADD CONSTRAINT UC_Persona_Derecho UNIQUE (ID_Persona, ID_Derecho);



SELECT ID_Persona, ID_Derecho, COUNT(*) as cantidad
FROM Persona_Derecho
GROUP BY ID_Persona, ID_Derecho
HAVING COUNT(*) > 1;






