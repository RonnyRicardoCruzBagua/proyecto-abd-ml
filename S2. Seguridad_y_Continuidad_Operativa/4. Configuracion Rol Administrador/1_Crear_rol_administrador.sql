USE HotelDB;
GO

IF NOT EXISTS (
    SELECT 1
    FROM sys.database_principals
    WHERE name = 'RolAdministrador'
)
BEGIN
    CREATE ROLE RolAdministrador;
END;
GO

PRINT 'RolAdministrador creado correctamente';
GO