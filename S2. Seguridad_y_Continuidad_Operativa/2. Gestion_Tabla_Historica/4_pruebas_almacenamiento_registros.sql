/*
    Proyecto: Hotel Booking Demand
    Integrante 2: Diseno y Gestion de la Tabla Historica
    Archivo: 4_pruebas_almacenamiento_registros.sql

    Objetivo:
    Realizar pruebas de almacenamiento de registros historicos generados
    por los triggers de auditoria.
*/

USE HotelDB;
GO

IF OBJECT_ID('dbo.AuditoriaCambios', 'U') IS NULL
BEGIN
    THROW 50001, 'No existe dbo.AuditoriaCambios. Ejecute primero 1_creacion_tabla_historica.sql.', 1;
END;
GO

DECLARE @total_antes INT;
SELECT @total_antes = COUNT(*) FROM dbo.AuditoriaCambios;

PRINT CONCAT('Total de registros historicos antes de la prueba: ', @total_antes);
GO

/* =========================================================
   Prueba 1: Clientes - INSERT, UPDATE, DELETE
   ========================================================= */

DECLARE @id_cliente_test INT;

INSERT INTO dbo.Clientes (
    country,
    customer_type,
    is_repeated_guest,
    previous_cancellations,
    previous_bookings_not_canceled
)
VALUES ('EC', 'Transient', 0, 0, 0);

SET @id_cliente_test = SCOPE_IDENTITY();

UPDATE dbo.Clientes
SET previous_cancellations = previous_cancellations + 1
WHERE id_cliente = @id_cliente_test;

DELETE FROM dbo.Clientes
WHERE id_cliente = @id_cliente_test;
GO

/* =========================================================
   Prueba 2: Reservas - INSERT, UPDATE, DELETE
   ========================================================= */

DECLARE @id_reserva_test INT;
DECLARE @id_hotel INT;
DECLARE @id_cliente INT;
DECLARE @id_canal INT;
DECLARE @id_habitacion INT;
DECLARE @id_estado INT;
DECLARE @id_fecha INT;

SELECT TOP 1 @id_hotel = id_hotel FROM dbo.Hoteles ORDER BY id_hotel;
SELECT TOP 1 @id_cliente = id_cliente FROM dbo.Clientes ORDER BY id_cliente;
SELECT TOP 1 @id_canal = id_canal FROM dbo.CanalesReserva ORDER BY id_canal;
SELECT TOP 1 @id_habitacion = id_habitacion FROM dbo.Habitaciones ORDER BY id_habitacion;
SELECT TOP 1 @id_estado = id_estado FROM dbo.EstadosReserva ORDER BY id_estado;
SELECT TOP 1 @id_fecha = id_fecha FROM dbo.FechasLlegada ORDER BY id_fecha;

IF @id_hotel IS NULL OR @id_cliente IS NULL OR @id_canal IS NULL OR @id_habitacion IS NULL OR @id_estado IS NULL OR @id_fecha IS NULL
BEGIN
    THROW 50002, 'No existen datos base suficientes para probar Reservas. Cargue primero las tablas normalizadas.', 1;
END;

INSERT INTO dbo.Reservas (
    id_hotel,
    id_cliente,
    id_canal,
    id_habitacion,
    id_estado,
    id_fecha,
    lead_time,
    stays_in_weekend_nights,
    stays_in_week_nights,
    adults,
    children,
    babies,
    adr,
    booking_changes,
    total_of_special_requests
)
VALUES (
    @id_hotel,
    @id_cliente,
    @id_canal,
    @id_habitacion,
    @id_estado,
    @id_fecha,
    12,
    1,
    2,
    2,
    0,
    0,
    99.90,
    0,
    1
);

SET @id_reserva_test = SCOPE_IDENTITY();

UPDATE dbo.Reservas
SET adr = 120.50,
    booking_changes = booking_changes + 1,
    total_of_special_requests = total_of_special_requests + 1
WHERE id_reserva = @id_reserva_test;

DELETE FROM dbo.Reservas
WHERE id_reserva = @id_reserva_test;
GO

/* =========================================================
   Resultado de pruebas
   ========================================================= */

SELECT TOP 20
    id_auditoria,
    tabla_afectada,
    operacion,
    id_registro_afectado,
    fecha_evento,
    usuario_sql,
    descripcion
FROM dbo.AuditoriaCambios
ORDER BY id_auditoria DESC;
GO

SELECT
    tabla_afectada,
    operacion,
    COUNT(*) AS total_eventos
FROM dbo.AuditoriaCambios
GROUP BY tabla_afectada, operacion
ORDER BY tabla_afectada, operacion;
GO
