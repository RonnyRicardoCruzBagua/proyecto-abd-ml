# DOCUMENTO DRP

El presente Plan de Recuperación ante Desastres (DRP) tiene como objetivo garantizar la continuidad operativa de la base de datos HotelDB ante eventos críticos que comprometan la disponibilidad o integridad de la información.

La base de datos almacena información relacionada con reservas hoteleras, clientes, hoteles, habitaciones, canales de reserva, estados de reserva, fechas de llegada y registros históricos de auditoría.

---

### **Objetivo:**

Garantizar la recuperación total de la base de datos HotelDB mediante procedimientos documentados, verificables y ejecutables.

---

### **Alcance**

Aplica a la Base de datos HotelDB.

- Tabla Reservas.

- Tabla Clientes.

- Tabla Hoteles.

- Tabla Habitaciones.

- Tabla CanalesReserva.

- Tabla EstadosReserva.

- Tabla FechasLlegada.

- Tabla AuditoriaCambios.

- Triggers de auditoría.

---

## **Riesgos identificados**

| Riesgo | Probabilidad | Impacto |
| --- | --- | --- |
| Eliminación accidental de registros | Alta | Alto |
| Modificación incorrecta de datos | Alta | Alto |
| Eliminación de tablas críticas | Media | Crítico |
| Corrupción de base de datos | Baja | Crítico |
| Falla del servidor SQL Server | Baja | Crítico |
| Error administrativo | Alta | Alto |
| Ataque de malware o ransomware | Baja | Crítico |
| Fallo eléctrico | Media | Alto |

---

## **Política de Backups**

- **Full Backup**

Frecuencia:

> Semanal --> Domingo 00:00

- **Differential Backup**

Frecuencia:

> Diario a las 02:00 am

- **Transaction Log Backup**

Frecuencia:

> Cada hora

---

## **Objetos Críticos del Sistema**

Los siguientes objetos son considerados críticos para la recuperación:

**Nivel Crítico Alto**

1. **Reservas**

Contiene la información principal de las reservas hoteleras.

**Impacto ante pérdida:**

> Muy Alto

**Prioridad de recuperación:**

> Inmediata

2. **Clientes**

Contiene los datos asociados a los huéspedes y clientes.

**Impacto ante pérdida:**

> Alto

**Prioridad de recuperación:**

> Alta

3. **AuditoriaCambios**

Almacena el historial de modificaciones realizadas por los usuarios y procesos automáticos.

**Impacto ante pérdida:**

> Alto

**Prioridad de recuperación:**

> Alta

---

### **Nivel Crítico Medio**

- Hoteles

- Habitaciones

- CanalesReserva

- EstadosReserva

- FechasLlegada

---

##  **Estrategia de Recuperación**

La estrategia DRP se basa en la combinación de:

**1. Full Backup** 

Respaldo completo de toda la base de datos.

**Permite recuperar:**

- Estructura

- Datos

- Índices

- Restricciones

- Objetos almacenados

**2. Differential Backup**

Respaldo de los cambios realizados desde el último respaldo completo.

**Permite:**

- Reducir tiempos de recuperación.

- Reducir espacio de almacenamiento.


**3.Transaction Log Backup**

Respaldo del registro de transacciones.

**Permite:**

- Recuperación punto en el tiempo.

- Minimizar pérdida de información.

- Recuperación de operaciones recientes.

---

## **Objetivos de recuperación**

**RTO** --> Recovery Time Objective

> 2 Horas

Tiempo maximo para restaurar el servicio

**RPO** --> Recovery Point Objective

> 1 Hora

Maxima perdida aceptable de informacion.

---

## Procedimiento General de Recuperación

Ante un incidente crítico se deberá seguir el siguiente procedimiento:

1. Identificar el incidente y determinar el alcance del daño.
2. Aislar la base de datos afectada.
3. Restaurar el último Full Backup disponible.
4. Aplicar el último Differential Backup.
5. Aplicar los Transaction Log Backups disponibles.
6. Validar la integridad de la información recuperada.
7. Verificar la existencia de tablas, índices y restricciones.
8. Validar el funcionamiento de los triggers de auditoría.
9. Verificar los registros almacenados en la tabla AuditoriaCambios.
10. Habilitar nuevamente la operación normal de la base de datos.

---

## Resultado Esperado

Garantizar la recuperación total de la base de datos HotelDB ante una falla crítica utilizando procedimientos documentados, verificables y ejecutables, minimizando el tiempo de indisponibilidad y la pérdida de información.

