# Implementacion de la Base de Datos en SQL Server

Carpeta creada para la actividad del Integrante 2: implementacion de la base de datos en SQL Server para el proyecto de reservas hoteleras.

## Archivos

- `01_creacion_base_datos.sql`: script principal para crear la base de datos `HotelDB` y todas las tablas del modelo.
- `02_consultas_evidencia.sql`: consultas para generar evidencias de ejecucion en SQL Server.
- `03_diagrama_entidad_relacion.md`: documento con el diagrama entidad-relacion en formato Mermaid.
- `03_diagrama_entidad_relacion.png`: imagen del diagrama entidad-relacion.

## Tablas implementadas

- Hoteles
- Clientes
- CanalesReserva
- Habitaciones
- EstadosReserva
- FechasLlegada
- Reservas

## Relacion del modelo

La tabla `Reservas` es la tabla central del modelo. Cada reserva se relaciona mediante claves foraneas con:

- `Hoteles`
- `Clientes`
- `CanalesReserva`
- `Habitaciones`
- `EstadosReserva`
- `FechasLlegada`

## Que cumple el script

- Creacion de la base de datos `HotelDB`.
- Creacion de todas las tablas del modelo diseñado.
- Implementacion de Primary Keys.
- Implementacion de Foreign Keys.
- Implementacion de restricciones de integridad con `NOT NULL`, `UNIQUE`, `CHECK` y `DEFAULT`.
- Uso de tipos de datos adecuados para SQL Server.
- Creacion de indices en claves foraneas para mejorar consultas.

## Orden de ejecucion

1. Abrir SQL Server Management Studio o Azure Data Studio.
2. Ejecutar `01_creacion_base_datos.sql`.
3. Ejecutar `02_consultas_evidencia.sql`.
4. Tomar capturas de los resultados para entregar como evidencias de ejecucion.

## Resultado esperado

Al ejecutar el script, la base de datos `HotelDB` queda creada con las tablas normalizadas, sus llaves primarias, llaves foraneas, restricciones y tipos de datos necesarios para representar el modelo entidad-relacion del proyecto.
