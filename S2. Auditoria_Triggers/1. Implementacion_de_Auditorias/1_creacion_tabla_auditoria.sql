/*
    Proyecto: Hotel Booking Demand
    Integrante: Auditoría mediante Triggers
    Archivo: 1_creacion_tabla_auditoria.sql

    Creamos una tabla central de auditoría para registrar automáticamente
    operaciones INSERT, UPDATE y DELETE realizadas en tablas críticas.
*/

USE HotelDB;
GO

/* =========================================================
   Crear tabla de auditoría
   ========================================================= */

IF OBJECT_ID('dbo.AuditoriaCambios', 'U') IS NOT NULL
BEGIN
    DROP TABLE dbo.AuditoriaCambios;
END;
GO

CREATE TABLE dbo.AuditoriaCambios (
    id_auditoria INT IDENTITY(1,1) PRIMARY KEY,

    tabla_afectada VARCHAR(100) NOT NULL,
    operacion VARCHAR(20) NOT NULL,

    id_registro_afectado INT NULL,

    fecha_evento DATETIME2(0) NOT NULL DEFAULT SYSDATETIME(),
    usuario_sql VARCHAR(100) NOT NULL DEFAULT SUSER_SNAME(),

    datos_anteriores NVARCHAR(MAX) NULL,
    datos_nuevos NVARCHAR(MAX) NULL,

    descripcion VARCHAR(300) NULL
);
GO

/* =========================================================
   Validación de creación de tabla
   ========================================================= */

SELECT 
    COLUMN_NAME,
    DATA_TYPE,
    IS_NULLABLE
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_NAME = 'AuditoriaCambios'
ORDER BY ORDINAL_POSITION;
GO

/* =========================================================
   Verificar que la tabla esté vacía al inicio
   ========================================================= */

SELECT COUNT(*) AS total_registros_auditoria
FROM dbo.AuditoriaCambios;
GO



