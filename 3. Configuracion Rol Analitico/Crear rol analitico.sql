USE HotelDB;
GO

IF NOT EXISTS (
    SELECT *
    FROM sys.database_principals
    WHERE name = 'RolAnalitico'
)
BEGIN
    CREATE ROLE RolAnalitico;
END;
GO

PRINT 'RolAnalitico creado correctamente';
GO