
# Vistas e Índices para Machine Learning

## Proyecto

**Hotel Booking Demand**

## Tema

**Predicción de cancelación de reservas hoteleras y segmentación de clientes mediante Machine Learning y persistencia híbrida SQL Server + MongoDB**

---

## Descripción general

Mi parte del proyecto consiste en preparar los datos de SQL Server para que puedan ser utilizados posteriormente en Python y Machine Learning, para esto se validó la base normalizada, se crearon vistas para modelos supervisados y no supervisados, se implementaron índices para mejorar el rendimiento de las consultas y se generaron evidencias de ejecución.

---

## Archivos incluidos

```text
00_validacion_base.sql
01_vistas_machine_learning.sql
02_indices_optimizacion.sql
03_evidencias_consultas.sql
README.md
```

## 00_validacion_base.sql
Este archivo verifica que la base de datos normalizada, HotelDB esté correctamente creada y poblada, se revisa la cantidad de registros de las tablas principales:
- Hoteles
- Clientes
- CanalesReserva
- Habitaciones
- EstadosReserva
- FechasLlegada
- Reservas

También se compara la cantidad de registros entre la tabla original y la tabla normalizada.  
Resultado esperado:
1. **HotelDB_RAW.dbo.hotel_raw = 119390 registros**
2. **HotelDB.dbo.Reservas = 119390 registros**  

Esto confirma que la base normalizada conserva todos los registros del dataset original.

## 01_vistas_machine_learning.sql
Este archivo crea las vistas que serán usadas desde Python para Machine Learning, se crearon dos vistas principales:
###  **vw_prediccion_cancelacion**   
Esta vista se usará para modelos supervisados, es decir, para predecir si una reserva será cancelada o no.

La variable objetivo es:
- is_canceled

Donde:
1. **0 = reserva no cancelada**
2. **1 = reserva cancelada**

Algunas columnas importantes de esta vista son:

- hotel
- lead_time
- adults
- children
- adr
- country
- market_segment
- customer_type
- previous_cancellations
- is_canceled

Esta vista puede ser usada por modelos como:

- Regresión Logística
- Árbol de Decisión
- Random Forest


###  **vw_segmentacion_clientes**
Esta vista se usará para aprendizaje no supervisado con K-Means, sirve para agrupar reservas o clientes con características parecidas, algunas columnas importantes son:

- lead_time
- total_noches
- adults
- children
- adr
- booking_changes
- total_of_special_requests
- previous_cancellations

Esta vista puede ayudar a identificar grupos como:

- Reservas hechas con mucha anticipación.
- Reservas familiares.
- Clientes con historial de cancelaciones.
- Reservas con muchas solicitudes especiales.

Resultado esperado de ambas vistas:
1. **vw_prediccion_cancelacion = 119390 registros**
2. **vw_segmentacion_clientes = 119390 registros**

## 02_indices_optimizacion.sql
Este archivo crea índices para mejorar el rendimiento de las consultas, los índices ayudan a que SQL Server consulte los datos de forma más rápida, especialmente cuando se usan uniones entre tablas o columnas importantes para análisis, se consideraron dos tipos de índices:

**Índices clustered**

Estos ya se generan principalmente con las llaves primarias, por ejemplo:

- PK_Reservas
- PK_Clientes
- PK_Hoteles

**Índices non-clustered**

Se crearon índices adicionales para mejorar consultas importantes, algunos índices creados son:

- IX_Reservas_id_hotel_ML
- IX_Reservas_id_cliente_ML
- IX_Reservas_id_estado_ML
- IX_Reservas_lead_time_ML
- IX_Reservas_adr_ML
- IX_Reservas_Clustering_ML
- IX_Clientes_historial_ML

Estos índices apoyan consultas relacionadas con:

- Tipo de hotel.
- Cliente.
- Estado de cancelación.
- Anticipación de reserva.
- Tarifa promedio.
- Historial de cancelaciones.
- Variables usadas para clustering.

## 03_evidencias_consultas.sql
Este archivo contiene consultas para comprobar que las vistas funcionan correctamente y para evidenciar el rendimiento, se realizaron consultas como:

- Total de registros en las vistas.
- Cancelaciones por tipo de hotel.
- Cancelaciones por tipo de cliente.
- Promedio de lead_time según cancelación.
- Promedios de variables usadas para clustering.
- Reservas con mayor anticipación.
- Reservas con tarifa promedio más alta.

También se activaron estadísticas de SQL Server:
1. **SET STATISTICS IO ON;**
2. **SET STATISTICS TIME ON;**

Esto permite revisar:
- Tiempo de CPU.
- Tiempo total de ejecución.
- Lecturas lógicas.
- Lecturas físicas.

Estas evidencias sirven para demostrar que las consultas fueron ejecutadas correctamente y que se revisó su rendimiento.

**Resultados importantes**

Las vistas contienen todos los registros esperados:
1. **total_prediccion = 119390**
2. **total_segmentacion = 119390**

Además, se observó que las reservas canceladas tienen un promedio mayor de lead_time, lo que indica que la anticipación de la reserva puede ser una variable importante para predecir cancelaciones.

**Relación con Machine Learning:**
Las vistas creadas permiten que Python pueda consumir los datos de forma sencilla.

Para modelos supervisados:
1. SELECT * FROM dbo.vw_prediccion_cancelacion;

Para clustering con K-Means:
1. SELECT * FROM dbo.vw_segmentacion_clientes;

De esta manera, Python no necesita consultar muchas tablas por separado, sino que puede trabajar directamente con vistas preparadas.

En resumen mi parte fue preparar los datos desde SQL Server para Machine Learning, primero validé que la base normalizada tenga los 119390 registros del dataset original, luego creé dos vistas: una para predecir cancelaciones y otra para segmentar clientes o reservas, después implementé índices para mejorar el rendimiento de las consultas y finalmente ejecuté consultas de evidencia usando estadísticas de SQL Server.
