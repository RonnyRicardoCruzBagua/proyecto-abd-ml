USE HotelDB;
GO

IF NOT EXISTS (
    SELECT *
    FROM sys.database_principals
    WHERE name = 'usuario_analitico'
)
BEGIN
    CREATE USER usuario_analitico
    WITHOUT LOGIN;
END;
GO

ALTER ROLE RolAnalitico

ADD MEMBER usuario_analitico;
GO

PRINT 'Usuario agregado al RolAnalitico';
GO

--PERMISOS GRANT
USE HotelDB;
GO

GRANT SELECT ON dbo.Clientes TO RolAnalitico;
GRANT SELECT ON dbo.Reservas TO RolAnalitico;
GRANT SELECT ON dbo.Hoteles TO RolAnalitico;

GO

--PERMISOS TABLA HISTORICA

GRANT SELECT ON dbo.AuditoriaCambios TO RolAnalitico;
GO

--PERMISOS VISTAS ANALITICAS
GRANT SELECT ON dbo.vw_prediccion_cancelacion TO RolAnalitico;
GO