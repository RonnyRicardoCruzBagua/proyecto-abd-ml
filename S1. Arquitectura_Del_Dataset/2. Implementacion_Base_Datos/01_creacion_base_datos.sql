/*
    Universidad Nacional de Chimborazo
    Proyecto: Hotel Booking Demand
    Integrante 2: Implementacion de la Base de Datos en SQL Server

    Actividades cubiertas:
    - Crear la base de datos.
    - Crear todas las tablas del modelo diseñado.
    - Implementar Primary Keys.
    - Implementar Foreign Keys.
    - Implementar Constraints.
    - Usar tipos de datos adecuados.

    Modelo:
    Hoteles, Reservas, Clientes, Habitaciones, CanalesReserva,
    EstadosReserva y FechasLlegada.
*/

IF DB_ID(N'HotelDB') IS NULL
BEGIN
    CREATE DATABASE HotelDB;
END;
GO

USE HotelDB;
GO

/*
    Se eliminan las tablas en orden inverso a sus dependencias para permitir
    ejecutar nuevamente el script durante pruebas.
*/
IF OBJECT_ID(N'dbo.Reservas', N'U') IS NOT NULL DROP TABLE dbo.Reservas;
IF OBJECT_ID(N'dbo.FechasLlegada', N'U') IS NOT NULL DROP TABLE dbo.FechasLlegada;
IF OBJECT_ID(N'dbo.EstadosReserva', N'U') IS NOT NULL DROP TABLE dbo.EstadosReserva;
IF OBJECT_ID(N'dbo.Habitaciones', N'U') IS NOT NULL DROP TABLE dbo.Habitaciones;
IF OBJECT_ID(N'dbo.Clientes', N'U') IS NOT NULL DROP TABLE dbo.Clientes;
IF OBJECT_ID(N'dbo.CanalesReserva', N'U') IS NOT NULL DROP TABLE dbo.CanalesReserva;
IF OBJECT_ID(N'dbo.Hoteles', N'U') IS NOT NULL DROP TABLE dbo.Hoteles;
GO

CREATE TABLE dbo.Hoteles (
    id_hotel INT IDENTITY(1,1) NOT NULL,
    nombre VARCHAR(50) NOT NULL,
    CONSTRAINT PK_Hoteles PRIMARY KEY (id_hotel),
    CONSTRAINT UQ_Hoteles_nombre UNIQUE (nombre),
    CONSTRAINT CK_Hoteles_nombre CHECK (LTRIM(RTRIM(nombre)) <> '')
);
GO

CREATE TABLE dbo.Clientes (
    id_cliente INT IDENTITY(1,1) NOT NULL,
    country VARCHAR(10) NULL,
    customer_type VARCHAR(50) NOT NULL,
    is_repeated_guest BIT NOT NULL CONSTRAINT DF_Clientes_is_repeated_guest DEFAULT (0),
    previous_cancellations INT NOT NULL CONSTRAINT DF_Clientes_previous_cancellations DEFAULT (0),
    previous_bookings_not_canceled INT NOT NULL CONSTRAINT DF_Clientes_previous_bookings_not_canceled DEFAULT (0),
    CONSTRAINT PK_Clientes PRIMARY KEY (id_cliente),
    CONSTRAINT CK_Clientes_customer_type CHECK (customer_type IN ('Transient', 'Contract', 'Transient-Party', 'Group')),
    CONSTRAINT CK_Clientes_is_repeated_guest CHECK (is_repeated_guest IN (0, 1)),
    CONSTRAINT CK_Clientes_previous_cancellations CHECK (previous_cancellations >= 0),
    CONSTRAINT CK_Clientes_previous_bookings_not_canceled CHECK (previous_bookings_not_canceled >= 0)
);
GO

CREATE TABLE dbo.CanalesReserva (
    id_canal INT IDENTITY(1,1) NOT NULL,
    market_segment VARCHAR(50) NOT NULL,
    distribution_channel VARCHAR(50) NOT NULL,
    CONSTRAINT PK_CanalesReserva PRIMARY KEY (id_canal),
    CONSTRAINT UQ_CanalesReserva_segmento_canal UNIQUE (market_segment, distribution_channel),
    CONSTRAINT CK_CanalesReserva_market_segment CHECK (LTRIM(RTRIM(market_segment)) <> ''),
    CONSTRAINT CK_CanalesReserva_distribution_channel CHECK (LTRIM(RTRIM(distribution_channel)) <> '')
);
GO

CREATE TABLE dbo.Habitaciones (
    id_habitacion INT IDENTITY(1,1) NOT NULL,
    reserved_room_type VARCHAR(10) NOT NULL,
    assigned_room_type VARCHAR(10) NOT NULL,
    CONSTRAINT PK_Habitaciones PRIMARY KEY (id_habitacion),
    CONSTRAINT UQ_Habitaciones_tipos UNIQUE (reserved_room_type, assigned_room_type),
    CONSTRAINT CK_Habitaciones_reserved_room_type CHECK (LTRIM(RTRIM(reserved_room_type)) <> ''),
    CONSTRAINT CK_Habitaciones_assigned_room_type CHECK (LTRIM(RTRIM(assigned_room_type)) <> '')
);
GO

CREATE TABLE dbo.EstadosReserva (
    id_estado INT IDENTITY(1,1) NOT NULL,
    is_canceled BIT NOT NULL,
    CONSTRAINT PK_EstadosReserva PRIMARY KEY (id_estado),
    CONSTRAINT UQ_EstadosReserva_is_canceled UNIQUE (is_canceled),
    CONSTRAINT CK_EstadosReserva_is_canceled CHECK (is_canceled IN (0, 1))
);
GO

CREATE TABLE dbo.FechasLlegada (
    id_fecha INT IDENTITY(1,1) NOT NULL,
    arrival_date_year SMALLINT NOT NULL,
    arrival_date_month VARCHAR(20) NOT NULL,
    arrival_date_week_number TINYINT NOT NULL,
    arrival_date_day_of_month TINYINT NOT NULL,
    fecha_llegada AS TRY_CONVERT(
        DATE,
        CONCAT(
            arrival_date_year, '-',
            CASE arrival_date_month
                WHEN 'January' THEN '01'
                WHEN 'February' THEN '02'
                WHEN 'March' THEN '03'
                WHEN 'April' THEN '04'
                WHEN 'May' THEN '05'
                WHEN 'June' THEN '06'
                WHEN 'July' THEN '07'
                WHEN 'August' THEN '08'
                WHEN 'September' THEN '09'
                WHEN 'October' THEN '10'
                WHEN 'November' THEN '11'
                WHEN 'December' THEN '12'
            END,
            '-', RIGHT('00' + CAST(arrival_date_day_of_month AS VARCHAR(2)), 2)
        )
    ),
    CONSTRAINT PK_FechasLlegada PRIMARY KEY (id_fecha),
    CONSTRAINT UQ_FechasLlegada_fecha UNIQUE (arrival_date_year, arrival_date_month, arrival_date_week_number, arrival_date_day_of_month),
    CONSTRAINT CK_FechasLlegada_year CHECK (arrival_date_year BETWEEN 2000 AND 2100),
    CONSTRAINT CK_FechasLlegada_month CHECK (arrival_date_month IN ('January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December')),
    CONSTRAINT CK_FechasLlegada_week CHECK (arrival_date_week_number BETWEEN 1 AND 53),
    CONSTRAINT CK_FechasLlegada_day CHECK (arrival_date_day_of_month BETWEEN 1 AND 31)
);
GO

CREATE TABLE dbo.Reservas (
    id_reserva INT IDENTITY(1,1) NOT NULL,
    id_hotel INT NOT NULL,
    id_cliente INT NOT NULL,
    id_canal INT NOT NULL,
    id_habitacion INT NOT NULL,
    id_estado INT NOT NULL,
    id_fecha INT NOT NULL,
    lead_time INT NOT NULL,
    stays_in_weekend_nights TINYINT NOT NULL,
    stays_in_week_nights TINYINT NOT NULL,
    adults TINYINT NOT NULL,
    children TINYINT NULL,
    babies TINYINT NOT NULL CONSTRAINT DF_Reservas_babies DEFAULT (0),
    adr DECIMAL(10,2) NOT NULL,
    booking_changes SMALLINT NOT NULL CONSTRAINT DF_Reservas_booking_changes DEFAULT (0),
    total_of_special_requests TINYINT NOT NULL CONSTRAINT DF_Reservas_total_special_requests DEFAULT (0),
    fecha_creacion DATETIME2(0) NOT NULL CONSTRAINT DF_Reservas_fecha_creacion DEFAULT (SYSDATETIME()),
    CONSTRAINT PK_Reservas PRIMARY KEY (id_reserva),
    CONSTRAINT FK_Reservas_Hoteles FOREIGN KEY (id_hotel) REFERENCES dbo.Hoteles(id_hotel),
    CONSTRAINT FK_Reservas_Clientes FOREIGN KEY (id_cliente) REFERENCES dbo.Clientes(id_cliente),
    CONSTRAINT FK_Reservas_CanalesReserva FOREIGN KEY (id_canal) REFERENCES dbo.CanalesReserva(id_canal),
    CONSTRAINT FK_Reservas_Habitaciones FOREIGN KEY (id_habitacion) REFERENCES dbo.Habitaciones(id_habitacion),
    CONSTRAINT FK_Reservas_EstadosReserva FOREIGN KEY (id_estado) REFERENCES dbo.EstadosReserva(id_estado),
    CONSTRAINT FK_Reservas_FechasLlegada FOREIGN KEY (id_fecha) REFERENCES dbo.FechasLlegada(id_fecha),
    CONSTRAINT CK_Reservas_lead_time CHECK (lead_time >= 0),
    CONSTRAINT CK_Reservas_stays_weekend CHECK (stays_in_weekend_nights >= 0),
    CONSTRAINT CK_Reservas_stays_week CHECK (stays_in_week_nights >= 0),
    CONSTRAINT CK_Reservas_total_noches CHECK (stays_in_weekend_nights + stays_in_week_nights >= 0),
    CONSTRAINT CK_Reservas_adults CHECK (adults >= 0),
    CONSTRAINT CK_Reservas_children CHECK (children IS NULL OR children >= 0),
    CONSTRAINT CK_Reservas_babies CHECK (babies >= 0),
    CONSTRAINT CK_Reservas_adr CHECK (adr >= -100 AND adr <= 10000),
    CONSTRAINT CK_Reservas_booking_changes CHECK (booking_changes >= 0),
    CONSTRAINT CK_Reservas_total_special_requests CHECK (total_of_special_requests >= 0)
);
GO

CREATE INDEX IX_Reservas_id_hotel ON dbo.Reservas(id_hotel);
CREATE INDEX IX_Reservas_id_cliente ON dbo.Reservas(id_cliente);
CREATE INDEX IX_Reservas_id_canal ON dbo.Reservas(id_canal);
CREATE INDEX IX_Reservas_id_habitacion ON dbo.Reservas(id_habitacion);
CREATE INDEX IX_Reservas_id_estado ON dbo.Reservas(id_estado);
CREATE INDEX IX_Reservas_id_fecha ON dbo.Reservas(id_fecha);
GO

INSERT INTO dbo.EstadosReserva (is_canceled)
VALUES (0), (1);
GO

PRINT 'Base de datos HotelDB creada correctamente con tablas, PK, FK, constraints y tipos de datos adecuados.';
GO


