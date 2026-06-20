-- ========================================
-- CONEXIÓN Y CONFIGURACIÓN DE BASE DE DATOS
-- ========================================

-- Crear base de datos si no existe
IF DB_ID('HotelDB_RAW') IS NULL
BEGIN
    CREATE DATABASE HotelDB_RAW;
    PRINT 'Base de datos HotelDB_RAW creada exitosamente.';
END;
GO

-- Usar la base de datos
USE HotelDB_RAW;
GO

-- Crear tabla temporal con todos los campos como VARCHAR para carga segura
IF OBJECT_ID('dbo.hotel_raw_temp', 'U') IS NOT NULL
    DROP TABLE dbo.hotel_raw_temp;

CREATE TABLE dbo.hotel_raw_temp (
    hotel VARCHAR(50),
    is_canceled VARCHAR(50),
    lead_time VARCHAR(50),
    arrival_date_year VARCHAR(50),
    arrival_date_month VARCHAR(50),
    arrival_date_week_number VARCHAR(50),
    arrival_date_day_of_month VARCHAR(50),
    stays_in_weekend_nights VARCHAR(50),
    stays_in_week_nights VARCHAR(50),
    adults VARCHAR(50),
    children VARCHAR(50),
    babies VARCHAR(50),
    meal VARCHAR(50),
    country VARCHAR(50),
    market_segment VARCHAR(50),
    distribution_channel VARCHAR(50),
    is_repeated_guest VARCHAR(50),
    previous_cancellations VARCHAR(50),
    previous_bookings_not_canceled VARCHAR(50),
    reserved_room_type VARCHAR(50),
    assigned_room_type VARCHAR(50),
    booking_changes VARCHAR(50),
    deposit_type VARCHAR(50),
    agent VARCHAR(50),
    company VARCHAR(50),
    days_in_waiting_list VARCHAR(50),
    customer_type VARCHAR(50),
    adr VARCHAR(50),
    required_car_parking_spaces VARCHAR(50),
    total_of_special_requests VARCHAR(50),
    reservation_status VARCHAR(50),
    reservation_status_date VARCHAR(50)
);
PRINT 'Tabla temporal creada para carga segura.';
GO

-- Cargar datos desde el CSV a la tabla temporal (El URL debe cambiarse por la ruta local del archivo CSV)
BULK INSERT dbo.hotel_raw_temp
FROM 'C:\1_UNACH\1_Issac_Unach\1_AUTONOMOS UNACH\Semestre_4\ABD\Proyecto\Codigo_Proyecto\proyecto-abd-ml\database\hotel_bookings.csv'
WITH (
    FIRSTROW = 2,
    FIELDTERMINATOR = ',',
    ROWTERMINATOR = '0x0A',
    TABLOCK,
    CODEPAGE = '65001'
);
PRINT 'Datos cargados en tabla temporal.';
GO

-- Crear tabla final con tipos de datos correctos
IF OBJECT_ID('dbo.hotel_raw', 'U') IS NOT NULL
    DROP TABLE dbo.hotel_raw;

CREATE TABLE dbo.hotel_raw (
    hotel VARCHAR(50),
    is_canceled INT,
    lead_time INT,
    arrival_date_year INT,
    arrival_date_month VARCHAR(20),
    arrival_date_week_number INT,
    arrival_date_day_of_month INT,
    stays_in_weekend_nights INT,
    stays_in_week_nights INT,
    adults INT,
    children FLOAT,
    babies INT,
    meal VARCHAR(20),
    country VARCHAR(10),
    market_segment VARCHAR(50),
    distribution_channel VARCHAR(50),
    is_repeated_guest INT,
    previous_cancellations INT,
    previous_bookings_not_canceled INT,
    reserved_room_type VARCHAR(5),
    assigned_room_type VARCHAR(5),
    booking_changes INT,
    deposit_type VARCHAR(50),
    agent VARCHAR(50),
    company VARCHAR(50),
    days_in_waiting_list INT,
    customer_type VARCHAR(50),
    adr FLOAT,
    required_car_parking_spaces INT,
    total_of_special_requests INT,
    reservation_status VARCHAR(50),
    reservation_status_date DATE
);
PRINT 'Tabla hotel_raw creada con tipos de datos correctos.';
GO

-- Convertir y transferir datos desde tabla temporal a tabla final
INSERT INTO dbo.hotel_raw
SELECT 
    hotel,
    TRY_CAST(NULLIF(is_canceled, 'NULL') AS INT),
    TRY_CAST(NULLIF(lead_time, 'NULL') AS INT),
    TRY_CAST(NULLIF(arrival_date_year, 'NULL') AS INT),
    arrival_date_month,
    TRY_CAST(NULLIF(arrival_date_week_number, 'NULL') AS INT),
    TRY_CAST(NULLIF(arrival_date_day_of_month, 'NULL') AS INT),
    TRY_CAST(NULLIF(stays_in_weekend_nights, 'NULL') AS INT),
    TRY_CAST(NULLIF(stays_in_week_nights, 'NULL') AS INT),
    TRY_CAST(NULLIF(adults, 'NULL') AS INT),
    TRY_CAST(NULLIF(children, 'NULL') AS FLOAT),
    TRY_CAST(NULLIF(babies, 'NULL') AS INT),
    meal,
    country,
    market_segment,
    distribution_channel,
    TRY_CAST(NULLIF(is_repeated_guest, 'NULL') AS INT),
    TRY_CAST(NULLIF(previous_cancellations, 'NULL') AS INT),
    TRY_CAST(NULLIF(previous_bookings_not_canceled, 'NULL') AS INT),
    reserved_room_type,
    assigned_room_type,
    TRY_CAST(NULLIF(booking_changes, 'NULL') AS INT),
    deposit_type,
    NULLIF(agent, 'NULL'),
    NULLIF(company, 'NULL'),
    TRY_CAST(NULLIF(days_in_waiting_list, 'NULL') AS INT),
    customer_type,
    TRY_CAST(NULLIF(adr, 'NULL') AS FLOAT),
    TRY_CAST(NULLIF(required_car_parking_spaces, 'NULL') AS INT),
    TRY_CAST(NULLIF(total_of_special_requests, 'NULL') AS INT),
    reservation_status,
    TRY_CAST(NULLIF(reservation_status_date, 'NULL') AS DATE)
FROM dbo.hotel_raw_temp;

PRINT 'Datos convertidos y transferidos correctamente.';
GO

-- Eliminar tabla temporal
DROP TABLE dbo.hotel_raw_temp;
PRINT 'Tabla temporal eliminada.';
GO

-- Validar la carga de datos
PRINT '';
PRINT '========== VALIDACIÓN FINAL ==========';
PRINT '';

DECLARE @TotalRegistros INT = (SELECT COUNT(*) FROM hotel_raw);
PRINT CONCAT('✓ Total de registros cargados: ', @TotalRegistros);
PRINT '';
PRINT 'Primeros 5 registros:';
SELECT TOP 5 * FROM hotel_raw;
PRINT '';
PRINT 'Estructura de la tabla:';
SELECT COLUMN_NAME, DATA_TYPE, IS_NULLABLE FROM INFORMATION_SCHEMA.COLUMNS 
WHERE TABLE_NAME = 'hotel_raw' ORDER BY ORDINAL_POSITION;
