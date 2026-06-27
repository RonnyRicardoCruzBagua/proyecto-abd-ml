/*
    Archivo: 2_triggers_reservas.sql

    Creamos triggers de auditoría para la tabla Reservas.
    Se registran automáticamente operaciones INSERT, UPDATE y DELETE
    en la tabla dbo.AuditoriaCambios.
*/

USE HotelDB;
GO

/* =========================================================
   Trigger 1: Auditoria de INSERT en Reservas
   ========================================================= */

CREATE OR ALTER TRIGGER dbo.trg_Reservas_Auditoria_Insert
ON dbo.Reservas
AFTER INSERT
AS
BEGIN
    SET NOCOUNT ON;

    INSERT INTO dbo.AuditoriaCambios (
        tabla_afectada,
        operacion,
        id_registro_afectado,
        datos_anteriores,
        datos_nuevos,
        descripcion
    )
    SELECT
        'Reservas',
        'INSERT',
        i.id_reserva,
        NULL,
        (
            SELECT i.*
            FOR JSON PATH, WITHOUT_ARRAY_WRAPPER
        ),
        'Se insertó una nueva reserva en la tabla Reservas.'
    FROM inserted i;
END;
GO

/* =========================================================
   Trigger 2: Auditoria de UPDATE en Reservas
   ========================================================= */

CREATE OR ALTER TRIGGER dbo.trg_Reservas_Auditoria_Update
ON dbo.Reservas
AFTER UPDATE
AS
BEGIN
    SET NOCOUNT ON;

    INSERT INTO dbo.AuditoriaCambios (
        tabla_afectada,
        operacion,
        id_registro_afectado,
        datos_anteriores,
        datos_nuevos,
        descripcion
    )
    SELECT
        'Reservas',
        'UPDATE',
        i.id_reserva,
        (
            SELECT d.*
            FOR JSON PATH, WITHOUT_ARRAY_WRAPPER
        ),
        (
            SELECT i.*
            FOR JSON PATH, WITHOUT_ARRAY_WRAPPER
        ),
        'Se actualizó una reserva en la tabla Reservas.'
    FROM inserted i
    INNER JOIN deleted d
        ON i.id_reserva = d.id_reserva;
END;
GO

/* =========================================================
   Trigger 3: Auditoria de DELETE en Reservas
   ========================================================= */

CREATE OR ALTER TRIGGER dbo.trg_Reservas_Auditoria_Delete
ON dbo.Reservas
AFTER DELETE
AS
BEGIN
    SET NOCOUNT ON;

    INSERT INTO dbo.AuditoriaCambios (
        tabla_afectada,
        operacion,
        id_registro_afectado,
        datos_anteriores,
        datos_nuevos,
        descripcion
    )
    SELECT
        'Reservas',
        'DELETE',
        d.id_reserva,
        (
            SELECT d.*
            FOR JSON PATH, WITHOUT_ARRAY_WRAPPER
        ),
        NULL,
        'Se eliminó una reserva en la tabla Reservas.'
    FROM deleted d;
END;
GO

/* =========================================================
   Validación: Verificar triggers creados en Reservas
   ========================================================= */

SELECT 
    name AS nombre_trigger,
    OBJECT_NAME(parent_id) AS tabla_asociada,
    create_date,
    modify_date
FROM sys.triggers
WHERE OBJECT_NAME(parent_id) = 'Reservas'
ORDER BY name;
GO


