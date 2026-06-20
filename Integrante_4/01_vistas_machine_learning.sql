/*
    Proyecto: Hotel Booking Demand
    Integrante 4: Vistas para Machine Learning
    Crear vistas que permitan consumir los datos desde Python
    para modelos supervisados y no supervisados.
*/

USE HotelDB;
GO

/* =========================================================
   Vista 1: Predicción de cancelación de reservas
   Esta vista será usada para modelos supervisados:
   Regresión Logística, Árbol de Decisión y Random Forest.
   ========================================================= */

CREATE OR ALTER VIEW dbo.vw_prediccion_cancelacion AS
SELECT
    r.id_reserva,

    -- Información del hotel
    h.nombre AS hotel,

    -- Información de fecha de llegada
    f.arrival_date_year,
    f.arrival_date_month,
    f.arrival_date_week_number,
    f.arrival_date_day_of_month,
    f.fecha_llegada,

    -- Información de la reserva
    r.lead_time,
    r.stays_in_weekend_nights,
    r.stays_in_week_nights,
    (r.stays_in_weekend_nights + r.stays_in_week_nights) AS total_noches,
    r.adults,
    ISNULL(r.children, 0) AS children,
    r.babies,
    r.adr,
    r.booking_changes,
    r.total_of_special_requests,

    -- Información del cliente
    c.country,
    c.customer_type,
    c.is_repeated_guest,
    c.previous_cancellations,
    c.previous_bookings_not_canceled,

    -- Información del canal de reserva
    cr.market_segment,
    cr.distribution_channel,

    -- Información de habitación
    ha.reserved_room_type,
    ha.assigned_room_type,

    -- Variable objetivo
    e.is_canceled

FROM dbo.Reservas r
INNER JOIN dbo.Hoteles h
    ON r.id_hotel = h.id_hotel
INNER JOIN dbo.Clientes c
    ON r.id_cliente = c.id_cliente
INNER JOIN dbo.CanalesReserva cr
    ON r.id_canal = cr.id_canal
INNER JOIN dbo.Habitaciones ha
    ON r.id_habitacion = ha.id_habitacion
INNER JOIN dbo.EstadosReserva e
    ON r.id_estado = e.id_estado
INNER JOIN dbo.FechasLlegada f
    ON r.id_fecha = f.id_fecha;
GO


/* =========================================================
   Vista 2: Segmentación de clientes/reservas
   Esta vista será usada para K-Means.
   ========================================================= */

CREATE OR ALTER VIEW dbo.vw_segmentacion_clientes AS
SELECT
    r.id_reserva,

    -- Variables numéricas para clustering
    r.lead_time,
    r.stays_in_weekend_nights,
    r.stays_in_week_nights,
    (r.stays_in_weekend_nights + r.stays_in_week_nights) AS total_noches,
    r.adults,
    ISNULL(r.children, 0) AS children,
    r.babies,
    r.adr,
    r.booking_changes,
    r.total_of_special_requests,

    -- Historial del cliente
    c.is_repeated_guest,
    c.previous_cancellations,
    c.previous_bookings_not_canceled,

    -- Se incluye para analizar después qué clusters cancelan más
    e.is_canceled

FROM dbo.Reservas r
INNER JOIN dbo.Clientes c
    ON r.id_cliente = c.id_cliente
INNER JOIN dbo.EstadosReserva e
    ON r.id_estado = e.id_estado;
GO

/* =========================================================
   Pruebas de las vistas creadas
   ========================================================= */

-- Evidencia 1: Vista de predicción con columnas principales
SELECT TOP 10
    id_reserva,
    hotel,
    lead_time,
    adults,
    children,
    adr,
    country,
    market_segment,
    customer_type,
    is_canceled
FROM dbo.vw_prediccion_cancelacion
ORDER BY id_reserva;
GO

-- Evidencia 2: Vista de segmentación con columnas principales
SELECT TOP 10
    id_reserva,
    lead_time,
    total_noches,
    adults,
    children,
    adr,
    booking_changes,
    total_of_special_requests,
    previous_cancellations,
    is_canceled
FROM dbo.vw_segmentacion_clientes
ORDER BY id_reserva;
GO

-- Evidencia 3: Total de registros en la vista de predicción
SELECT COUNT(*) AS total_prediccion
FROM dbo.vw_prediccion_cancelacion;
GO

-- Evidencia 4: Total de registros en la vista de segmentación
SELECT COUNT(*) AS total_segmentacion
FROM dbo.vw_segmentacion_clientes;
GO




