-- Datos normalizados para el análisis del dataset y diseño del modelo
SET NOCOUNT ON;

-- Limpiar tablas destino si se ejecutó el proceso antes
DELETE FROM HotelDB.dbo.Reservas;
DELETE FROM HotelDB.dbo.FechasLlegada;
DELETE FROM HotelDB.dbo.EstadosReserva;
DELETE FROM HotelDB.dbo.Habitaciones;
DELETE FROM HotelDB.dbo.Clientes;
DELETE FROM HotelDB.dbo.CanalesReserva;
DELETE FROM HotelDB.dbo.Hoteles;

-- Hoteles
INSERT INTO HotelDB.dbo.Hoteles (nombre)
SELECT DISTINCT hotel
FROM HotelDB_RAW.dbo.hotel_raw;

-- Canales
INSERT INTO HotelDB.dbo.CanalesReserva (market_segment, distribution_channel)
SELECT DISTINCT market_segment, distribution_channel
FROM HotelDB_RAW.dbo.hotel_raw;

-- Clientes
INSERT INTO HotelDB.dbo.Clientes (
    country, customer_type,
    is_repeated_guest,
    previous_cancellations,
    previous_bookings_not_canceled
)
SELECT DISTINCT
    country,
    customer_type,
    is_repeated_guest,
    previous_cancellations,
    previous_bookings_not_canceled
FROM HotelDB_RAW.dbo.hotel_raw;

-- Habitaciones
INSERT INTO HotelDB.dbo.Habitaciones (reserved_room_type, assigned_room_type)
SELECT DISTINCT reserved_room_type, assigned_room_type
FROM HotelDB_RAW.dbo.hotel_raw;

-- Estados
INSERT INTO HotelDB.dbo.EstadosReserva (is_canceled)
SELECT DISTINCT is_canceled
FROM HotelDB_RAW.dbo.hotel_raw;

-- Fechas
INSERT INTO HotelDB.dbo.FechasLlegada (
    arrival_date_year,
    arrival_date_month,
    arrival_date_week_number,
    arrival_date_day_of_month
)
SELECT DISTINCT
    arrival_date_year,
    arrival_date_month,
    arrival_date_week_number,
    arrival_date_day_of_month
FROM HotelDB_RAW.dbo.hotel_raw;

/*  (Este bloque se hizo comentario para evitar errores de duplicados al ejecutar varias veces el proceso)
-- Crear índices únicos para evitar filas duplicadas en las dimensiones
IF NOT EXISTS (SELECT 1 FROM sys.indexes WHERE name = 'UQ_Hoteles_nombre' AND object_id = OBJECT_ID('HotelDB.dbo.Hoteles'))
    CREATE UNIQUE INDEX UQ_Hoteles_nombre ON HotelDB.dbo.Hoteles(nombre);

IF NOT EXISTS (SELECT 1 FROM sys.indexes WHERE name = 'UQ_CanalesReserva_segment_dist' AND object_id = OBJECT_ID('HotelDB.dbo.CanalesReserva'))
    CREATE UNIQUE INDEX UQ_CanalesReserva_segment_dist ON HotelDB.dbo.CanalesReserva(market_segment, distribution_channel);

IF NOT EXISTS (SELECT 1 FROM sys.indexes WHERE name = 'UQ_Clientes_combo' AND object_id = OBJECT_ID('HotelDB.dbo.Clientes'))
    CREATE UNIQUE INDEX UQ_Clientes_combo ON HotelDB.dbo.Clientes(country, customer_type, is_repeated_guest, previous_cancellations, previous_bookings_not_canceled);

IF NOT EXISTS (SELECT 1 FROM sys.indexes WHERE name = 'UQ_Habitaciones_combo' AND object_id = OBJECT_ID('HotelDB.dbo.Habitaciones'))
    CREATE UNIQUE INDEX UQ_Habitaciones_combo ON HotelDB.dbo.Habitaciones(reserved_room_type, assigned_room_type);

IF NOT EXISTS (SELECT 1 FROM sys.indexes WHERE name = 'UQ_EstadosReserva_canceled' AND object_id = OBJECT_ID('HotelDB.dbo.EstadosReserva'))
    CREATE UNIQUE INDEX UQ_EstadosReserva_canceled ON HotelDB.dbo.EstadosReserva(is_canceled);

IF NOT EXISTS (SELECT 1 FROM sys.indexes WHERE name = 'UQ_FechasLlegada_combo' AND object_id = OBJECT_ID('HotelDB.dbo.FechasLlegada'))
    CREATE UNIQUE INDEX UQ_FechasLlegada_combo ON HotelDB.dbo.FechasLlegada(arrival_date_year, arrival_date_month, arrival_date_week_number, arrival_date_day_of_month);
*/

-- Reservas
INSERT INTO HotelDB.dbo.Reservas (
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
SELECT 
    h.id_hotel,
    c.id_cliente,
    cr.id_canal,
    ha.id_habitacion,
    e.id_estado,
    f.id_fecha,
    r.lead_time,
    r.stays_in_weekend_nights,
    r.stays_in_week_nights,
    r.adults,
    r.children,
    r.babies,
    r.adr,
    r.booking_changes,
    r.total_of_special_requests
FROM HotelDB_RAW.dbo.hotel_raw r
JOIN HotelDB.dbo.Hoteles h 
    ON r.hotel = h.nombre
JOIN HotelDB.dbo.Clientes c 
    ON r.country = c.country 
    AND r.customer_type = c.customer_type
    AND r.is_repeated_guest = c.is_repeated_guest
    AND r.previous_cancellations = c.previous_cancellations
    AND r.previous_bookings_not_canceled = c.previous_bookings_not_canceled
JOIN HotelDB.dbo.CanalesReserva cr 
    ON r.market_segment = cr.market_segment
    AND r.distribution_channel = cr.distribution_channel
JOIN HotelDB.dbo.Habitaciones ha 
    ON r.reserved_room_type = ha.reserved_room_type
    AND r.assigned_room_type = ha.assigned_room_type
JOIN HotelDB.dbo.EstadosReserva e 
    ON r.is_canceled = e.is_canceled
JOIN HotelDB.dbo.FechasLlegada f 
    ON r.arrival_date_year = f.arrival_date_year
    AND r.arrival_date_month = f.arrival_date_month
    AND r.arrival_date_week_number = f.arrival_date_week_number
    AND r.arrival_date_day_of_month = f.arrival_date_day_of_month;


