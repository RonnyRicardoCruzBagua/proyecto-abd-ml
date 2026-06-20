/*
    Proyecto: Hotel Booking Demand
    Integrante 4: Evidencias de consultas optimizadas
    Probar las vistas creadas, validar que tengan datos correctos
    y medir el rendimiento de las consultas usando estadísticas de SQL Server.
*/

USE HotelDB;
GO

/* =========================================================
   Activar estadísticas de rendimiento
   Esto permite ver lecturas y tiempo de ejecución.
   ========================================================= */

SET STATISTICS IO ON;
SET STATISTICS TIME ON;
GO


/* =========================================================
   Evidencia 1: Consulta de la vista de predicción
   Muestra las columnas principales para Machine Learning supervisado.
   ========================================================= */

SELECT TOP 20
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


/* =========================================================
   Evidencia 2: Total de registros en vista de predicción
   Debe mostrar 119390 registros.
   ========================================================= */

SELECT COUNT(*) AS total_registros_prediccion
FROM dbo.vw_prediccion_cancelacion;
GO


/* =========================================================
   Evidencia 3: Cancelaciones por tipo de hotel
   Permite ver cuántas reservas fueron canceladas o no
   según el tipo de hotel.
   ========================================================= */

SELECT
    hotel,
    is_canceled,
    COUNT(*) AS total_reservas
FROM dbo.vw_prediccion_cancelacion
GROUP BY hotel, is_canceled
ORDER BY hotel, is_canceled;
GO


/* =========================================================
   Evidencia 4: Cancelaciones por tipo de cliente
   Permite analizar si algunos tipos de cliente cancelan más.
   ========================================================= */

SELECT
    customer_type,
    is_canceled,
    COUNT(*) AS total_reservas
FROM dbo.vw_prediccion_cancelacion
GROUP BY customer_type, is_canceled
ORDER BY customer_type, is_canceled;
GO


/* =========================================================
   Evidencia 5: Promedio de lead_time según cancelación
   Sirve para analizar si las reservas con más anticipación
   tienden a cancelarse más.
   ========================================================= */

SELECT
    is_canceled,
    AVG(CAST(lead_time AS FLOAT)) AS promedio_lead_time,
    MIN(lead_time) AS minimo_lead_time,
    MAX(lead_time) AS maximo_lead_time
FROM dbo.vw_prediccion_cancelacion
GROUP BY is_canceled
ORDER BY is_canceled;
GO


/* =========================================================
   Evidencia 6: Consulta de la vista de segmentación
   Muestra las columnas principales para K-Means.
   ========================================================= */

SELECT TOP 20
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


/* =========================================================
   Evidencia 7: Total de registros en vista de segmentación
   Debe mostrar 119390 registros.
   ========================================================= */

SELECT COUNT(*) AS total_registros_segmentacion
FROM dbo.vw_segmentacion_clientes;
GO


/* =========================================================
   Evidencia 8: Promedios de variables usadas para clustering
   Sirve para revisar el comportamiento general de las variables
   que después usará K-Means.
   ========================================================= */

SELECT
    AVG(CAST(lead_time AS FLOAT)) AS promedio_anticipacion,
    AVG(CAST(total_noches AS FLOAT)) AS promedio_noches,
    AVG(CAST(adults AS FLOAT)) AS promedio_adultos,
    AVG(CAST(children AS FLOAT)) AS promedio_ninos,
    AVG(CAST(adr AS FLOAT)) AS promedio_tarifa,
    AVG(CAST(booking_changes AS FLOAT)) AS promedio_cambios,
    AVG(CAST(total_of_special_requests AS FLOAT)) AS promedio_solicitudes,
    AVG(CAST(previous_cancellations AS FLOAT)) AS promedio_cancelaciones_previas
FROM dbo.vw_segmentacion_clientes;
GO


/* =========================================================
   Evidencia 9: Reservas con mayor anticipación
   Esta consulta puede aprovechar el índice sobre lead_time.
   ========================================================= */

SELECT TOP 20
    id_reserva,
    hotel,
    lead_time,
    customer_type,
    market_segment,
    is_canceled
FROM dbo.vw_prediccion_cancelacion
ORDER BY lead_time DESC;
GO


/* =========================================================
   Evidencia 10: Reservas con tarifa promedio más alta
   Esta consulta puede aprovechar el índice sobre adr.
   ========================================================= */

SELECT TOP 20
    id_reserva,
    hotel,
    adr,
    lead_time,
    customer_type,
    is_canceled
FROM dbo.vw_prediccion_cancelacion
ORDER BY adr DESC;
GO


/* =========================================================
   Desactivar estadísticas de rendimiento
   ========================================================= */

SET STATISTICS IO OFF;
SET STATISTICS TIME OFF;
GO