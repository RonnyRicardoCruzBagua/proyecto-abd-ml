USE HotelDB;
GO

GRANT SELECT, INSERT, UPDATE, DELETE
ON dbo.Clientes
TO RolAdministrador;
GO

GRANT SELECT, INSERT, UPDATE, DELETE
ON dbo.Reservas
TO RolAdministrador;
GO

GRANT SELECT, INSERT, UPDATE, DELETE
ON dbo.Hoteles
TO RolAdministrador;
GO

GRANT SELECT, INSERT, UPDATE, DELETE
ON dbo.Habitaciones
TO RolAdministrador;
GO

GRANT SELECT, INSERT, UPDATE, DELETE
ON dbo.CanalesReserva
TO RolAdministrador;
GO

GRANT SELECT, INSERT, UPDATE, DELETE
ON dbo.EstadosReserva
TO RolAdministrador;
GO

GRANT SELECT, INSERT, UPDATE, DELETE
ON dbo.FechasLlegada
TO RolAdministrador;
GO

REVOKE DELETE
ON dbo.Clientes
FROM RolAdministrador;
GO