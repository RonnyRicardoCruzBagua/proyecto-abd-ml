# Diagrama Entidad-Relacion

Este diagrama representa el modelo relacional usado para la implementacion de la base de datos `HotelDB` en SQL Server.

La tabla central es `Reservas`, que se conecta con las tablas de dimension del modelo: `Hoteles`, `Clientes`, `CanalesReserva`, `Habitaciones`, `EstadosReserva` y `FechasLlegada`.

```mermaid
erDiagram
    HOTELES ||--o{ RESERVAS : tiene
    CLIENTES ||--o{ RESERVAS : realiza
    CANALES_RESERVA ||--o{ RESERVAS : registra
    HABITACIONES ||--o{ RESERVAS : asigna
    ESTADOS_RESERVA ||--o{ RESERVAS : clasifica
    FECHAS_LLEGADA ||--o{ RESERVAS : programa

    HOTELES {
        INT id_hotel PK
        VARCHAR nombre UK
    }

    CLIENTES {
        INT id_cliente PK
        VARCHAR country
        VARCHAR customer_type
        BIT is_repeated_guest
        INT previous_cancellations
        INT previous_bookings_not_canceled
    }

    CANALES_RESERVA {
        INT id_canal PK
        VARCHAR market_segment UK
        VARCHAR distribution_channel UK
    }

    HABITACIONES {
        INT id_habitacion PK
        VARCHAR reserved_room_type UK
        VARCHAR assigned_room_type UK
    }

    ESTADOS_RESERVA {
        INT id_estado PK
        BIT is_canceled UK
    }

    FECHAS_LLEGADA {
        INT id_fecha PK
        SMALLINT arrival_date_year UK
        VARCHAR arrival_date_month UK
        TINYINT arrival_date_week_number UK
        TINYINT arrival_date_day_of_month UK
        DATE fecha_llegada
    }

    RESERVAS {
        INT id_reserva PK
        INT id_hotel FK
        INT id_cliente FK
        INT id_canal FK
        INT id_habitacion FK
        INT id_estado FK
        INT id_fecha FK
        INT lead_time
        TINYINT stays_in_weekend_nights
        TINYINT stays_in_week_nights
        TINYINT adults
        TINYINT children
        TINYINT babies
        DECIMAL adr
        SMALLINT booking_changes
        TINYINT total_of_special_requests
        DATETIME2 fecha_creacion
    }
```

## Cardinalidades

- Un hotel puede tener muchas reservas.
- Un cliente puede estar relacionado con muchas reservas.
- Un canal de reserva puede aparecer en muchas reservas.
- Una combinacion de habitacion reservada/asignada puede aparecer en muchas reservas.
- Un estado de reserva puede clasificar muchas reservas.
- Una fecha de llegada puede estar asociada a muchas reservas.
- Cada reserva pertenece a un solo registro de cada tabla relacionada.
