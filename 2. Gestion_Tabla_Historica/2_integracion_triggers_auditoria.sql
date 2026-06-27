/*
    Proyecto: Hotel Booking Demand
    Integrante 2: Diseno y Gestion de la Tabla Historica
    Archivo: 2_integracion_triggers_auditoria.sql

    Objetivo:
    Verificar que la tabla historica dbo.AuditoriaCambios este integrada
    con los triggers desarrollados para las tablas criticas Clientes y Reservas.
*/

USE HotelDB;
GO

IF OBJECT_ID('dbo.AuditoriaCambios', 'U') IS NULL
BEGIN
    THROW 50001, 'No existe dbo.AuditoriaCambios. Ejecute primero 1_creacion_tabla_historica.sql.', 1;
END;
GO

DECLARE @TriggersEsperados TABLE (
    nombre_trigger SYSNAME NOT NULL,
    tabla_auditada SYSNAME NOT NULL
);

INSERT INTO @TriggersEsperados (nombre_trigger, tabla_auditada)
VALUES
    ('trg_Clientes_Auditoria_Insert', 'Clientes'),
    ('trg_Clientes_Auditoria_Update', 'Clientes'),
    ('trg_Clientes_Auditoria_Delete', 'Clientes'),
    ('trg_Reservas_Auditoria_Insert', 'Reservas'),
    ('trg_Reservas_Auditoria_Update', 'Reservas'),
    ('trg_Reservas_Auditoria_Delete', 'Reservas');

SELECT
    e.tabla_auditada,
    e.nombre_trigger,
    CASE
        WHEN t.object_id IS NULL THEN 'NO CREADO'
        WHEN t.is_disabled = 1 THEN 'DESHABILITADO'
        ELSE 'ACTIVO'
    END AS estado_trigger,
    t.create_date,
    t.modify_date
FROM @TriggersEsperados e
LEFT JOIN sys.triggers t
    ON t.name = e.nombre_trigger
ORDER BY e.tabla_auditada, e.nombre_trigger;

SELECT
    OBJECT_NAME(d.referencing_id) AS trigger_origen,
    OBJECT_NAME(tr.parent_id) AS tabla_auditada,
    d.referenced_schema_name,
    d.referenced_entity_name AS tabla_historica_referenciada
FROM sys.sql_expression_dependencies d
INNER JOIN sys.triggers tr
    ON d.referencing_id = tr.object_id
WHERE d.referenced_entity_name = 'AuditoriaCambios'
ORDER BY tabla_auditada, trigger_origen;

IF EXISTS (
    SELECT 1
    FROM @TriggersEsperados e
    LEFT JOIN sys.triggers t
        ON t.name = e.nombre_trigger
    WHERE t.object_id IS NULL OR t.is_disabled = 1
)
BEGIN
    PRINT 'Advertencia: uno o mas triggers esperados no existen o estan deshabilitados. Revise los scripts del Integrante 1.';
END
ELSE
BEGIN
    PRINT 'Integracion verificada: los triggers esperados estan activos y registran cambios en dbo.AuditoriaCambios.';
END;
GO
