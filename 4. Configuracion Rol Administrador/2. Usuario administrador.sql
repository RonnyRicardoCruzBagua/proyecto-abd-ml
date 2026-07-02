USE HotelDB;
GO

IF NOT EXISTS (
    SELECT 1
    FROM sys.database_principals
    WHERE name = 'usuario_administrador'
)
BEGIN
    CREATE USER usuario_administrador
    WITHOUT LOGIN;
END;
GO

ALTER ROLE RolAdministrador
ADD MEMBER usuario_administrador;
GO

PRINT 'Usuario agregado al RolAdministrador';
GO