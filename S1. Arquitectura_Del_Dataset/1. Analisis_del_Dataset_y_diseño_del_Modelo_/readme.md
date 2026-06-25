# **Normalización**

La Base de datos ha sido normalizada

Se creó una segunda base:

    - HotelDB

Esta base contiene el modelo relacional normalizado.

**🧩 Modelo Entidad-Relación**

Se identificaron las siguientes entidades:

- 🏨 Hoteles
- 👤 Clientes
- 📡 Canales de Reserva
- 🛏️ Habitaciones
- 📅 Fechas de llegada
- ✔️ Estados de reserva
- 📋 Reservas (tabla principal)

La tabla Reservas actúa como entidad central conectando todas las demás.

**🔄 Proceso de Normalización**

Se aplicaron las siguientes formas normales:

**✅ Primera Forma Normal (1FN)**

- Se eliminaron atributos multivaluados
- Cada campo contiene un solo valor
- No hay repetición de grupos

    ✔ Resultado: Datos atómicos

**✅ Segunda Forma Normal (2FN)**

Se separaron dependencias parciales:

- Clientes en tabla independiente
- Hoteles en tabla independiente

    ✔ Resultado: Reducción de redundancia

**✅ Tercera Forma Normal (3FN)**

Se eliminaron dependencias transitivas:

- Canales separados
- Estados separados
- Fechas separadas

    ✔ Resultado: Modelo totalmente normalizado

**🗃️ Diseño de Tablas**

🔹 Hoteles

- Almacena el tipo de hotel

🔹 Clientes

- Contiene información del cliente y su historial

🔹 CanalesReserva
- Define el segmento y canal de la reserva

🔹 Habitaciones

- Tipos de habitaciones reservadas y asignadas

🔹 EstadosReserva

- Indica si la reserva fue cancelada

🔹 FechasLlegada

- Información temporal de la llegada

🔹 Reservas

- Tabla principal que contiene la información de cada reserva

**🔑 Llaves**

🔹 Llaves Primarias

    Cada tabla contiene una clave primaria (IDENTITY)

🔹 Llaves Foráneas

    La tabla Reservas contiene:

- id_hotel → Hoteles
- id_cliente → Clientes
- id_canal → CanalesReserva
- id_habitacion → Habitaciones
- id_estado → EstadosReserva
- id_fecha → FechasLlegada

Esto garantiza la integridad referencial.

## Resultado esperado ✔️

El dataset o csv fue descompuesto en múltiples tablas relacionadas para cumplir con la normalización (1FN, 2FN y 3FN). Se definieron entidades como Hoteles, Clientes, Reservas, Habitaciones, Canales y Fechas. La tabla Reservas actúa como entidad central conectada mediante llaves foráneas, evitando redundancia y mejorando la integridad de los datos.

**Nota:** Realizar la conexion de vscode a sql-server.
