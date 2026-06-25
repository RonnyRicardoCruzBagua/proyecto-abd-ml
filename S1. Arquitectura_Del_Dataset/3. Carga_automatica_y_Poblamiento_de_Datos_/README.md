# Carga Automática y Poblamiento de Datos

## Descripción General

En este componente del proyecto se desarrolló un proceso ETL (Extract, Transform, Load) utilizando Python, con el objetivo de cargar automáticamente el dataset de reservas hoteleras hacia SQL Server.

Se transformó un archivo CSV en una base de datos relacional normalizada, garantizando integridad de datos y evitando inserciones manuales.

---

## Actividades realizadas

- Limpieza del dataset  
- Implementación del proceso ETL  
- Carga automática de datos desde Python hacia SQL Server  
- Validación de los registros cargados  

---

## Herramientas utilizadas

- Pandas  
- pyodbc  
- SQL Server  

---

## Proceso ETL

### Extracción

Se carga el dataset desde CSV:

```python
df = pd.read_csv(ruta)
```

---

### Transformación

Se limpian y preparan los datos:

```python
clientes = df[[
    'country', 'customer_type', 'is_repeated_guest',
    'previous_cancellations', 'previous_bookings_not_canceled'
]].drop_duplicates()
```

---

### Carga

Se insertan los datos en SQL Server mediante conexión con pyodbc:

```python
conn = pyodbc.connect(
    'DRIVER={ODBC Driver 17 for SQL Server};'
    'SERVER=localhost;'
    'DATABASE=HotelDB;'
    'Trusted_Connection=yes;'
)
```

Inserción de datos:

```python
cursor.execute("""
INSERT INTO Clientes (...)
VALUES (?, ?, ?, ?, ?)
""", ...)
```
``

---

### Relación entre tablas (claves foráneas)

Para mantener la integridad referencial:

```python
map_clientes = {(row.country, row.customer_type): row.id_cliente}
```

---

## Creación de la base de datos

Script SQL utilizado:

```sql
CREATE DATABASE HotelDB;
GO

USE HotelDB;
```

Creación de la tabla principal:

```sql
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
```

---

## Validación de datos

```sql
SELECT COUNT(*) FROM Reservas;
SELECT COUNT(*) FROM Clientes;
SELECT TOP 10 * FROM Reservas;
```

---

## Resultados obtenidos

- Inserción correcta del dataset completo  
- Base de datos poblada automáticamente  
- Datos organizados y listos para Machine Learning  

---

## Conclusión

Se implementó un proceso ETL completo que automatiza la carga de datos hacia SQL Server, garantizando integridad, eficiencia y preparación para análisis avanzado.

Este proceso permite que los datos estén listos para su uso en modelos de Machine Learning dentro del proyecto.
