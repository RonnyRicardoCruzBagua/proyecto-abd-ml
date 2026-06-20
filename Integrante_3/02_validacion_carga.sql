USE HotelDB;
GO

-- Verificar datos cargados
SELECT COUNT(*) AS total_reservas FROM Reservas;

SELECT COUNT(*) AS total_clientes FROM Clientes;
SELECT COUNT(*) AS total_hoteles FROM Hoteles;
SELECT COUNT(*) AS total_canales FROM CanalesReserva;
SELECT COUNT(*) AS total_habitaciones FROM Habitaciones;
SELECT COUNT(*) AS total_estados FROM EstadosReserva;
SELECT COUNT(*) AS total_fechas FROM FechasLlegada;

-- Visualización rápida
SELECT TOP 10 * FROM Reservas;
