/*
    Proyecto: Hotel Booking Demand
    Integrante 4: Índices para optimización de consultas
    Crear índices que mejoren el rendimiento de las consultas usadas
    por las vistas de Machine Learning:
    - vw_prediccion_cancelacion
    - vw_segmentacion_clientes
*/

USE HotelDB;
GO

/* =========================================================
   Nota:
   Las Primary Keys ya funcionan como índices clustered.
   En este script se crean índices non-clustered adicionales
   para mejorar consultas, joins y análisis.
   ========================================================= */


/* =========================================================
   Índices sobre llaves foráneas de la tabla Reservas
   Estas columnas se usan en los JOIN de las vistas.
   ========================================================= */

IF NOT EXISTS (
    SELECT 1 FROM sys.indexes
    WHERE name = 'IX_Reservas_id_hotel_ML'
    AND object_id = OBJECT_ID('dbo.Reservas')
)
BEGIN
    CREATE NONCLUSTERED INDEX IX_Reservas_id_hotel_ML
    ON dbo.Reservas(id_hotel);
END;
GO

IF NOT EXISTS (
    SELECT 1 FROM sys.indexes
    WHERE name = 'IX_Reservas_id_cliente_ML'
    AND object_id = OBJECT_ID('dbo.Reservas')
)
BEGIN
    CREATE NONCLUSTERED INDEX IX_Reservas_id_cliente_ML
    ON dbo.Reservas(id_cliente);
END;
GO

IF NOT EXISTS (
    SELECT 1 FROM sys.indexes
    WHERE name = 'IX_Reservas_id_canal_ML'
    AND object_id = OBJECT_ID('dbo.Reservas')
)
BEGIN
    CREATE NONCLUSTERED INDEX IX_Reservas_id_canal_ML
    ON dbo.Reservas(id_canal);
END;
GO

IF NOT EXISTS (
    SELECT 1 FROM sys.indexes
    WHERE name = 'IX_Reservas_id_habitacion_ML'
    AND object_id = OBJECT_ID('dbo.Reservas')
)
BEGIN
    CREATE NONCLUSTERED INDEX IX_Reservas_id_habitacion_ML
    ON dbo.Reservas(id_habitacion);
END;
GO

IF NOT EXISTS (
    SELECT 1 FROM sys.indexes
    WHERE name = 'IX_Reservas_id_estado_ML'
    AND object_id = OBJECT_ID('dbo.Reservas')
)
BEGIN
    CREATE NONCLUSTERED INDEX IX_Reservas_id_estado_ML
    ON dbo.Reservas(id_estado);
END;
GO

IF NOT EXISTS (
    SELECT 1 FROM sys.indexes
    WHERE name = 'IX_Reservas_id_fecha_ML'
    AND object_id = OBJECT_ID('dbo.Reservas')
)
BEGIN
    CREATE NONCLUSTERED INDEX IX_Reservas_id_fecha_ML
    ON dbo.Reservas(id_fecha);
END;
GO


/* =========================================================
   Índices sobre variables importantes para Machine Learning
   ========================================================= */

IF NOT EXISTS (
    SELECT 1 FROM sys.indexes
    WHERE name = 'IX_Reservas_lead_time_ML'
    AND object_id = OBJECT_ID('dbo.Reservas')
)
BEGIN
    CREATE NONCLUSTERED INDEX IX_Reservas_lead_time_ML
    ON dbo.Reservas(lead_time);
END;
GO

IF NOT EXISTS (
    SELECT 1 FROM sys.indexes
    WHERE name = 'IX_Reservas_adr_ML'
    AND object_id = OBJECT_ID('dbo.Reservas')
)
BEGIN
    CREATE NONCLUSTERED INDEX IX_Reservas_adr_ML
    ON dbo.Reservas(adr);
END;
GO

IF NOT EXISTS (
    SELECT 1 FROM sys.indexes
    WHERE name = 'IX_Reservas_booking_changes_ML'
    AND object_id = OBJECT_ID('dbo.Reservas')
)
BEGIN
    CREATE NONCLUSTERED INDEX IX_Reservas_booking_changes_ML
    ON dbo.Reservas(booking_changes);
END;
GO

IF NOT EXISTS (
    SELECT 1 FROM sys.indexes
    WHERE name = 'IX_Reservas_special_requests_ML'
    AND object_id = OBJECT_ID('dbo.Reservas')
)
BEGIN
    CREATE NONCLUSTERED INDEX IX_Reservas_special_requests_ML
    ON dbo.Reservas(total_of_special_requests);
END;
GO


/* =========================================================
   Índice compuesto para clustering
   Ayuda en consultas con variables numéricas usadas por K-Means.
   ========================================================= */

IF NOT EXISTS (
    SELECT 1 FROM sys.indexes
    WHERE name = 'IX_Reservas_Clustering_ML'
    AND object_id = OBJECT_ID('dbo.Reservas')
)
BEGIN
    CREATE NONCLUSTERED INDEX IX_Reservas_Clustering_ML
    ON dbo.Reservas (
        lead_time,
        adr,
        adults,
        children,
        booking_changes,
        total_of_special_requests
    );
END;
GO


/* =========================================================
   Índice para historial del cliente
   Estas variables ayudan a predecir cancelaciones.
   ========================================================= */

IF NOT EXISTS (
    SELECT 1 FROM sys.indexes
    WHERE name = 'IX_Clientes_historial_ML'
    AND object_id = OBJECT_ID('dbo.Clientes')
)
BEGIN
    CREATE NONCLUSTERED INDEX IX_Clientes_historial_ML
    ON dbo.Clientes (
        previous_cancellations,
        previous_bookings_not_canceled,
        is_repeated_guest
    );
END;
GO


/* =========================================================
   Evidencia: mostrar índices creados
   ========================================================= */

SELECT
    OBJECT_NAME(i.object_id) AS tabla,
    i.name AS indice,
    i.type_desc,
    i.is_unique
FROM sys.indexes i
WHERE OBJECT_NAME(i.object_id) IN (
    'Reservas',
    'Clientes',
    'Hoteles',
    'CanalesReserva',
    'Habitaciones',
    'EstadosReserva',
    'FechasLlegada'
)
AND i.name IS NOT NULL
ORDER BY tabla, indice;
GO