-- ===============================
-- CREAR BASE DE DATOS
-- ===============================
CREATE DATABASE HotelDB;
GO

-- ===============================
-- USAR BASE DE DATOS
-- ===============================
USE HotelDB;
GO

-- ===============================
-- CREAR TABLA HOTELES
-- ===============================
CREATE TABLE Hoteles (
    id_hotel INT IDENTITY(1,1) PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL
);
GO

-- ===============================
-- CONSULTAR DATOS
-- ===============================
SELECT * FROM Hoteles;
GO
SELECT * FROM Hoteles;

-- ===============================
-- CREAR TABLA CLIENTES
-- ===============================
CREATE TABLE Clientes (
    id_cliente INT IDENTITY(1,1) PRIMARY KEY,
    country VARCHAR(10),
    customer_type VARCHAR(50) NOT NULL,
    is_repeated_guest BIT NOT NULL,
    previous_cancellations INT NOT NULL,
    previous_bookings_not_canceled INT NOT NULL
);
GO
SELECT * FROM Clientes;

USE HotelDB;
GO

SELECT TOP 10 * FROM Clientes;

CREATE TABLE CanalesReserva (
    id_canal INT IDENTITY(1,1) PRIMARY KEY,
    market_segment VARCHAR(50) NOT NULL,
    distribution_channel VARCHAR(50) NOT NULL
);
GO
SELECT * FROM CanalesReserva;
SELECT TOP 10 * FROM CanalesReserva;

CREATE TABLE Habitaciones (
    id_habitacion INT IDENTITY(1,1) PRIMARY KEY,
    reserved_room_type VARCHAR(10) NOT NULL,
    assigned_room_type VARCHAR(10) NOT NULL
);
GO

SELECT * FROM Habitaciones;
SELECT TOP 10 * FROM Habitaciones;

CREATE TABLE EstadosReserva (
    id_estado INT IDENTITY(1,1) PRIMARY KEY,
    is_canceled BIT NOT NULL
);
GO
SELECT * FROM EstadosReserva;
SELECT * FROM EstadosReserva;

CREATE TABLE FechasLlegada (
    id_fecha INT IDENTITY(1,1) PRIMARY KEY,
    arrival_date_year INT NOT NULL,
    arrival_date_month VARCHAR(20) NOT NULL,
    arrival_date_week_number INT NOT NULL,
    arrival_date_day_of_month INT NOT NULL
);
GO

SELECT * FROM FechasLlegada;
SELECT TOP 10 * FROM FechasLlegada;


IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'Reservas')
BEGIN
    CREATE TABLE Reservas (
        id_reserva INT IDENTITY(1,1) PRIMARY KEY,
        id_hotel INT,
        id_cliente INT,
        id_canal INT,
        id_habitacion INT,
        id_estado INT,
        id_fecha INT,
        lead_time INT,
        stays_in_weekend_nights INT,
        stays_in_week_nights INT,
        adults INT,
        children INT,
        babies INT,
        adr DECIMAL(10,2)
    );
END
GO
SELECT COUNT(*) FROM Reservas;
SELECT COUNT(*) FROM Reservas;
