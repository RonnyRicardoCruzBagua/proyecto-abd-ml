USE HotelDB;
GO

-- Validar cantidad de registros por tabla normalizada
SELECT 'Hoteles' AS tabla, COUNT(*) AS total FROM dbo.Hoteles
UNION ALL
SELECT 'Clientes', COUNT(*) FROM dbo.Clientes
UNION ALL
SELECT 'CanalesReserva', COUNT(*) FROM dbo.CanalesReserva
UNION ALL
SELECT 'Habitaciones', COUNT(*) FROM dbo.Habitaciones
UNION ALL
SELECT 'EstadosReserva', COUNT(*) FROM dbo.EstadosReserva
UNION ALL
SELECT 'FechasLlegada', COUNT(*) FROM dbo.FechasLlegada
UNION ALL
SELECT 'Reservas', COUNT(*) FROM dbo.Reservas;
GO

-- Comparar registros originales vs registros normalizados
SELECT COUNT(*) AS total_raw
FROM HotelDB_RAW.dbo.hotel_raw;
GO

SELECT COUNT(*) AS total_reservas_normalizadas
FROM HotelDB.dbo.Reservas;
GO