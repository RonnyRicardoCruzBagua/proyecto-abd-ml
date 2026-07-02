# Auditoría mediante Triggers

**Hotel Booking Demand**

### **Tema:** 

**Predicción de cancelación de reservas hoteleras y segmentación de clientes mediante Machine Learning y persistencia híbrida SQL Server + MongoDB**

---
**Descripción general**  

Esta parte del proyecto consiste en implementar auditoría dentro de SQL Server mediante triggers, la idea principal es que la base de datos pueda registrar automáticamente los cambios realizados en tablas importantes del sistema, es decir, si alguien inserta, modifica o elimina información en tablas críticas como `Reservas` o `Clientes`, el sistema guarda un historial del cambio realizado.

Esto permite tener mayor control, trazabilidad y seguridad sobre los datos.

---

## Archivos incluidos

```text
1_creacion_tabla_auditoria.sql
2_triggers_reservas.sql
3_triggers_clientes.sql
4_pruebas_auditoria.sql
README.md
```

---
### **1_creacion_tabla_auditoria.sql**

Este archivo crea la tabla principal de auditoría:
- AuditoriaCambios  

Esta tabla almacena información sobre los cambios realizados en la base de datos.

Campos principales de la tabla
- **id_auditoria:** identificador del registro de auditoría.
- **tabla_afectada:** nombre de la tabla donde ocurrió el cambio.
- **operacion:** tipo de operación realizada: INSERT, UPDATE o DELETE.
- **id_registro_afectado:** ID del registro modificado.
- **fecha_evento:** fecha y hora en que ocurrió el cambio.
- **usuario_sql:** usuario que ejecutó la operación.
- **datos_anteriores:** datos antes del cambio.
- **datos_nuevos:** datos después del cambio.
- **descripcion:** explicación breve del evento registrado.

Al ejecutar este archivo, la tabla de auditoría se crea vacía.

Resultado inicial esperado:

```total_registros_auditoria = 0```

### **2_triggers_reservas.sql**
Este archivo crea triggers para la tabla:

- Reservas

Se crearon tres triggers:
- trg_Reservas_Auditoria_Insert
- trg_Reservas_Auditoria_Update
- trg_Reservas_Auditoria_Delete

Estos triggers registran automáticamente cualquier cambio realizado en la tabla Reservas.
- Si se inserta una reserva, se guarda un evento INSERT.
- Si se modifica una reserva, se guarda un evento UPDATE.
- Si se elimina una reserva, se guarda un evento DELETE.

Cada evento queda registrado en la tabla:
- AuditoriaCambios

### **3_triggers_clientes.sql**

Este archivo crea triggers para la tabla:
- Clientes

Se crearon tres triggers:
- trg_Clientes_Auditoria_Insert
- trg_Clientes_Auditoria_Update
- trg_Clientes_Auditoria_Delete

Estos triggers registran automáticamente cualquier cambio realizado en la tabla Clientes.
- Si se inserta un cliente, se registra en la auditoría.
- Si se actualiza un cliente, se guardan los datos anteriores y nuevos.
- Si se elimina un cliente, se guarda el registro eliminado.

Esto permite controlar cambios en información importante del cliente, como país, tipo de cliente e historial de cancelaciones.

### **4_pruebas_auditoria.sql**

Este archivo sirve para comprobar que los triggers funcionan correctamente.

Se realizaron pruebas en las tablas:
- Clientes
- Reservas

**Operaciones probadas**

Para cada tabla se ejecutaron operaciones:
- INSERT
- UPDATE
- DELETE

Luego se consultó la tabla AuditoriaCambios para verificar que los cambios fueron registrados correctamente.

**Resultados obtenidos**
Al ejecutar las pruebas se registraron 6 eventos de auditoría:
1. Clientes INSERT  = 1
2. Clientes UPDATE  = 1
3. Clientes DELETE  = 1
4. Reservas INSERT  = 1
5. Reservas UPDATE  = 1
6. Reservas DELETE  = 1

Esto confirma que los triggers funcionan correctamente para las dos tablas críticas seleccionadas.

Si el archivo 4_pruebas_auditoria.sql se ejecuta más de una vez, se agregarán nuevos registros en la tabla AuditoriaCambios, por ejemplo, la primera ejecución genera 6 registros, si se ejecuta nuevamente, se agregarán otros 6 registros más, esto no es un error, ya que la función de la auditoría es guardar cada operación realizada.

**¿Por qué se auditan Reservas y Clientes?**
Se eligieron estas tablas porque son importantes para el proyecto:

**Reservas**

Contiene la información principal de las reservas hoteleras, como hotel, cliente, fecha, tarifa, número de personas, solicitudes especiales y estado de cancelación.

**Clientes**

Contiene información relacionada con el cliente, como país, tipo de cliente, si es cliente repetido y su historial de cancelaciones.
Auditar estas tablas ayuda a controlar cambios en datos que pueden afectar el análisis y los modelos de Machine Learning.













