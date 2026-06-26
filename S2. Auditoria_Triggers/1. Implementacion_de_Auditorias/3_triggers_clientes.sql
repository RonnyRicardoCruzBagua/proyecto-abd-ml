/*
    Archivo: 3_triggers_clientes.sql

    Creamos triggers de auditoría para la tabla Clientes.
    Se registran automáticamente operaciones INSERT, UPDATE y DELETE
    en la tabla dbo.AuditoriaCambios.
*/

USE HotelDB;
GO

/* =========================================================
   Trigger 1: Auditoria de INSERT en Clientes
   ========================================================= */

CREATE OR ALTER TRIGGER dbo.trg_Clientes_Auditoria_Insert
ON dbo.Clientes
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
        'Clientes',
        'INSERT',
        i.id_cliente,
        NULL,
        (
            SELECT i.*
            FOR JSON PATH, WITHOUT_ARRAY_WRAPPER
        ),
        'Se insertó un nuevo cliente en la tabla Clientes.'
    FROM inserted i;
END;
GO

/* =========================================================
   Trigger 2: Auditoria de UPDATE en Clientes
   ========================================================= */

CREATE OR ALTER TRIGGER dbo.trg_Clientes_Auditoria_Update
ON dbo.Clientes
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
        'Clientes',
        'UPDATE',
        i.id_cliente,
        (
            SELECT d.*
            FOR JSON PATH, WITHOUT_ARRAY_WRAPPER
        ),
        (
            SELECT i.*
            FOR JSON PATH, WITHOUT_ARRAY_WRAPPER
        ),
        'Se actualizó un cliente en la tabla Clientes.'
    FROM inserted i
    INNER JOIN deleted d
        ON i.id_cliente = d.id_cliente;
END;
GO

/* =========================================================
   Trigger 3: Auditoria de DELETE en Clientes
   ========================================================= */

CREATE OR ALTER TRIGGER dbo.trg_Clientes_Auditoria_Delete
ON dbo.Clientes
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
        'Clientes',
        'DELETE',
        d.id_cliente,
        (
            SELECT d.*
            FOR JSON PATH, WITHOUT_ARRAY_WRAPPER
        ),
        NULL,
        'Se eliminó un cliente en la tabla Clientes.'
    FROM deleted d;
END;
GO

/* =========================================================
   Validacion: Verificar triggers creados en Clientes
   ========================================================= */

SELECT 
    name AS nombre_trigger,
    OBJECT_NAME(parent_id) AS tabla_asociada,
    create_date,
    modify_date
FROM sys.triggers
WHERE OBJECT_NAME(parent_id) = 'Clientes'
ORDER BY name;
GO



