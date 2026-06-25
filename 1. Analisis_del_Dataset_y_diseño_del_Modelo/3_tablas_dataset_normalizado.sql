-- Base de datos Normalizada para el proyecto de análisis del dataset y diseño del modelo
CREATE DATABASE HotelDB;
GO

USE HotelDB;
GO

-- Tablas del modelo

-- Hoteles
CREATE TABLE Hoteles (
    id_hotel INT IDENTITY PRIMARY KEY,
    nombre VARCHAR(50) UNIQUE
);

-- Clientes
CREATE TABLE Clientes (
    id_cliente INT IDENTITY PRIMARY KEY,
    country VARCHAR(50),
    customer_type VARCHAR(50),
    is_repeated_guest BIT,
    previous_cancellations INT,
    previous_bookings_not_canceled INT
);

-- Canales
CREATE TABLE CanalesReserva (
    id_canal INT IDENTITY PRIMARY KEY,
    market_segment VARCHAR(50),
    distribution_channel VARCHAR(50)
);

-- Habitaaciones
CREATE TABLE Habitaciones (
    id_habitacion INT IDENTITY PRIMARY KEY,
    reserved_room_type VARCHAR(10),
    assigned_room_type VARCHAR(10)
);

-- Estados
CREATE TABLE EstadosReserva (
    id_estado INT IDENTITY PRIMARY KEY,
    is_canceled BIT
);

-- Fechas
CREATE TABLE FechasLlegada (
    id_fecha INT IDENTITY PRIMARY KEY,
    arrival_date_year INT,
    arrival_date_month VARCHAR(20),
    arrival_date_week_number INT,
    arrival_date_day_of_month INT
);

-- Reservas
CREATE TABLE Reservas (
    id_reserva INT IDENTITY PRIMARY KEY,

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
    adr FLOAT,
    booking_changes INT,
    total_of_special_requests INT,

    FOREIGN KEY (id_hotel) REFERENCES Hoteles(id_hotel),
    FOREIGN KEY (id_cliente) REFERENCES Clientes(id_cliente),
    FOREIGN KEY (id_canal) REFERENCES CanalesReserva(id_canal),
    FOREIGN KEY (id_habitacion) REFERENCES Habitaciones(id_habitacion),
    FOREIGN KEY (id_estado) REFERENCES EstadosReserva(id_estado),
    FOREIGN KEY (id_fecha) REFERENCES FechasLlegada(id_fecha)
);