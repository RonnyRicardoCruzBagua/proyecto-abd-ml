USE HotelDB;
GO

EXECUTE AS USER = 'usuario_administrador';

-- Acceso a tablas

SELECT TOP 10 *
FROM dbo.Clientes;

SELECT TOP 10 *
FROM dbo.Reservas;

SELECT TOP 10 *
FROM dbo.Hoteles;

SELECT TOP 10 *
FROM dbo.Habitaciones;

-- Acceso a vista

SELECT TOP 10 *
FROM dbo.vw_resumen_reservas;

REVERT;
GO