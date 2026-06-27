/*
    Proyecto: Hotel Booking Demand
    Integrante 2: Diseno y Gestion de la Tabla Historica
    Archivo: 1_creacion_tabla_historica.sql

    Objetivo:
    Crear o completar la tabla historica de auditoria dbo.AuditoriaCambios.
    Esta tabla almacena el historial completo de cambios generados por triggers.

    Nota:
    Este script no modifica los archivos del Integrante 1. Solo completa la
    gestion de la tabla historica en SQL Server si ya existe.
*/

USE HotelDB;
GO

IF OBJECT_ID('dbo.AuditoriaCambios', 'U') IS NULL
BEGIN
    CREATE TABLE dbo.AuditoriaCambios (
        id_auditoria INT IDENTITY(1,1) NOT NULL,
        tabla_afectada VARCHAR(100) NOT NULL,
        operacion VARCHAR(20) NOT NULL,
        id_registro_afectado INT NULL,
        fecha_evento DATETIME2(0) NOT NULL CONSTRAINT DF_AuditoriaCambios_fecha_evento DEFAULT SYSDATETIME(),
        usuario_sql VARCHAR(100) NOT NULL CONSTRAINT DF_AuditoriaCambios_usuario_sql DEFAULT SUSER_SNAME(),
        datos_anteriores NVARCHAR(MAX) NULL,
        datos_nuevos NVARCHAR(MAX) NULL,
        descripcion VARCHAR(300) NULL,
        CONSTRAINT PK_AuditoriaCambios PRIMARY KEY (id_auditoria),
        CONSTRAINT CK_AuditoriaCambios_operacion CHECK (operacion IN ('INSERT', 'UPDATE', 'DELETE')),
        CONSTRAINT CK_AuditoriaCambios_tabla_afectada CHECK (LTRIM(RTRIM(tabla_afectada)) <> '')
    );
END;
GO

IF NOT EXISTS (
    SELECT 1
    FROM sys.key_constraints
    WHERE parent_object_id = OBJECT_ID('dbo.AuditoriaCambios')
      AND type = 'PK'
)
BEGIN
    ALTER TABLE dbo.AuditoriaCambios
    ADD CONSTRAINT PK_AuditoriaCambios PRIMARY KEY (id_auditoria);
END;
GO

IF NOT EXISTS (
    SELECT 1 FROM sys.check_constraints
    WHERE name = 'CK_AuditoriaCambios_operacion'
      AND parent_object_id = OBJECT_ID('dbo.AuditoriaCambios')
)
BEGIN
    ALTER TABLE dbo.AuditoriaCambios
    ADD CONSTRAINT CK_AuditoriaCambios_operacion
    CHECK (operacion IN ('INSERT', 'UPDATE', 'DELETE'));
END;
GO

IF NOT EXISTS (
    SELECT 1 FROM sys.check_constraints
    WHERE name = 'CK_AuditoriaCambios_tabla_afectada'
      AND parent_object_id = OBJECT_ID('dbo.AuditoriaCambios')
)
BEGIN
    ALTER TABLE dbo.AuditoriaCambios
    ADD CONSTRAINT CK_AuditoriaCambios_tabla_afectada
    CHECK (LTRIM(RTRIM(tabla_afectada)) <> '');
END;
GO

IF NOT EXISTS (
    SELECT 1
    FROM sys.default_constraints dc
    INNER JOIN sys.columns c
        ON dc.parent_object_id = c.object_id
       AND dc.parent_column_id = c.column_id
    WHERE dc.parent_object_id = OBJECT_ID('dbo.AuditoriaCambios')
      AND c.name = 'fecha_evento'
)
BEGIN
    ALTER TABLE dbo.AuditoriaCambios
    ADD CONSTRAINT DF_AuditoriaCambios_fecha_evento
    DEFAULT SYSDATETIME() FOR fecha_evento;
END;
GO

IF NOT EXISTS (
    SELECT 1
    FROM sys.default_constraints dc
    INNER JOIN sys.columns c
        ON dc.parent_object_id = c.object_id
       AND dc.parent_column_id = c.column_id
    WHERE dc.parent_object_id = OBJECT_ID('dbo.AuditoriaCambios')
      AND c.name = 'usuario_sql'
)
BEGIN
    ALTER TABLE dbo.AuditoriaCambios
    ADD CONSTRAINT DF_AuditoriaCambios_usuario_sql
    DEFAULT SUSER_SNAME() FOR usuario_sql;
END;
GO

IF NOT EXISTS (
    SELECT 1 FROM sys.indexes
    WHERE name = 'IX_AuditoriaCambios_tabla_operacion_fecha'
      AND object_id = OBJECT_ID('dbo.AuditoriaCambios')
)
BEGIN
    CREATE INDEX IX_AuditoriaCambios_tabla_operacion_fecha
    ON dbo.AuditoriaCambios (tabla_afectada, operacion, fecha_evento DESC);
END;
GO

IF NOT EXISTS (
    SELECT 1 FROM sys.indexes
    WHERE name = 'IX_AuditoriaCambios_registro_afectado'
      AND object_id = OBJECT_ID('dbo.AuditoriaCambios')
)
BEGIN
    CREATE INDEX IX_AuditoriaCambios_registro_afectado
    ON dbo.AuditoriaCambios (tabla_afectada, id_registro_afectado, fecha_evento DESC);
END;
GO

SELECT
    c.COLUMN_NAME,
    c.DATA_TYPE,
    c.CHARACTER_MAXIMUM_LENGTH,
    c.IS_NULLABLE
FROM INFORMATION_SCHEMA.COLUMNS c
WHERE c.TABLE_SCHEMA = 'dbo'
  AND c.TABLE_NAME = 'AuditoriaCambios'
ORDER BY c.ORDINAL_POSITION;
GO

SELECT COUNT(*) AS total_registros_historicos
FROM dbo.AuditoriaCambios;
GO
