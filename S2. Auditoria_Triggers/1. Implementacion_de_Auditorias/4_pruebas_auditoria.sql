/*
    Archivo: 4_pruebas_auditoria.sql

    Probamos que los triggers de auditoría funcionan correctamente
    en las tablas Clientes y Reservas.

    Las pruebas realizan operaciones INSERT, UPDATE y DELETE.
    Los cambios se registran automáticamente en dbo.AuditoriaCambios.
*/

USE HotelDB;
GO

/* =========================================================
   1. Verificar registros actuales de auditoria
   ========================================================= */

SELECT COUNT(*) AS total_auditoria_antes
FROM dbo.AuditoriaCambios;
GO


/* =========================================================
   2. Pruebas de auditoría en la tabla Clientes
   ========================================================= */

DECLARE @id_cliente_test INT;

-- INSERT de cliente de prueba
INSERT INTO dbo.Clientes (
    country,
    customer_type,
    is_repeated_guest,
    previous_cancellations,
    previous_bookings_not_canceled
)
VALUES (
    'EC',
    'Transient',
    0,
    0,
    0
);

SET @id_cliente_test = SCOPE_IDENTITY();

-- UPDATE del cliente de prueba
UPDATE dbo.Clientes
SET previous_cancellations = 1
WHERE id_cliente = @id_cliente_test;

-- DELETE del cliente de prueba
DELETE FROM dbo.Clientes
WHERE id_cliente = @id_cliente_test;


/* =========================================================
   3. Pruebas de auditoria en la tabla Reservas
   ========================================================= */

DECLARE @id_reserva_test INT;

DECLARE @id_hotel INT;
DECLARE @id_cliente INT;
DECLARE @id_canal INT;
DECLARE @id_habitacion INT;
DECLARE @id_estado INT;
DECLARE @id_fecha INT;

-- Tomar IDs existentes para crear una reserva de prueba valida
SELECT TOP 1 @id_hotel = id_hotel FROM dbo.Hoteles ORDER BY id_hotel;
SELECT TOP 1 @id_cliente = id_cliente FROM dbo.Clientes ORDER BY id_cliente;
SELECT TOP 1 @id_canal = id_canal FROM dbo.CanalesReserva ORDER BY id_canal;
SELECT TOP 1 @id_habitacion = id_habitacion FROM dbo.Habitaciones ORDER BY id_habitacion;
SELECT TOP 1 @id_estado = id_estado FROM dbo.EstadosReserva ORDER BY id_estado;
SELECT TOP 1 @id_fecha = id_fecha FROM dbo.FechasLlegada ORDER BY id_fecha;

-- INSERT de reserva de prueba
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
    10,
    1,
    2,
    2,
    0,
    0,
    80.00,
    0,
    1
);

SET @id_reserva_test = SCOPE_IDENTITY();

-- UPDATE de reserva de prueba
UPDATE dbo.Reservas
SET 
    adr = 95.50,
    booking_changes = 1,
    total_of_special_requests = 2
WHERE id_reserva = @id_reserva_test;

-- DELETE de reserva de prueba
DELETE FROM dbo.Reservas
WHERE id_reserva = @id_reserva_test;


/* =========================================================
   4. Ver registros generados en auditoria
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


/* =========================================================
   5. Resumen de auditoria por tabla y operacion
   ========================================================= */

SELECT
    tabla_afectada,
    operacion,
    COUNT(*) AS total_eventos
FROM dbo.AuditoriaCambios
GROUP BY tabla_afectada, operacion
ORDER BY tabla_afectada, operacion;


/* =========================================================
   6. Ver detalle JSON de los ultimos registros
   ========================================================= */

SELECT TOP 10
    id_auditoria,
    tabla_afectada,
    operacion,
    id_registro_afectado,
    datos_anteriores,
    datos_nuevos
FROM dbo.AuditoriaCambios
ORDER BY id_auditoria DESC;
GO




