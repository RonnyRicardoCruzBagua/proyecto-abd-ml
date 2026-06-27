# Diccionario de datos - Tabla historica de auditoria

Tabla: `dbo.AuditoriaCambios`
Base de datos: `HotelDB`

Esta tabla almacena el historial de cambios realizados en tablas criticas del proyecto. Los registros son generados automaticamente por triggers despues de operaciones `INSERT`, `UPDATE` y `DELETE`.

| Campo | Tipo de dato | Nulo | Descripcion | Regla / Uso |
|---|---:|:---:|---|---|
| `id_auditoria` | `INT IDENTITY(1,1)` | No | Identificador unico del evento historico. | Primary Key. |
| `tabla_afectada` | `VARCHAR(100)` | No | Nombre de la tabla donde ocurrio el cambio. | Ejemplo: `Clientes`, `Reservas`. |
| `operacion` | `VARCHAR(20)` | No | Tipo de operacion realizada. | `INSERT`, `UPDATE` o `DELETE`. |
| `id_registro_afectado` | `INT` | Si | Identificador del registro afectado en la tabla origen. | Permite rastrear el registro modificado. |
| `fecha_evento` | `DATETIME2(0)` | No | Fecha y hora en que se genero el evento. | Valor por defecto: `SYSDATETIME()`. |
| `usuario_sql` | `VARCHAR(100)` | No | Usuario de SQL Server que realizo la operacion. | Valor por defecto: `SUSER_SNAME()`. |
| `datos_anteriores` | `NVARCHAR(MAX)` | Si | Valores anteriores del registro. | Se usa en `UPDATE` y `DELETE`. Se guarda en JSON. |
| `datos_nuevos` | `NVARCHAR(MAX)` | Si | Valores nuevos del registro. | Se usa en `INSERT` y `UPDATE`. Se guarda en JSON. |
| `descripcion` | `VARCHAR(300)` | Si | Texto breve que explica el evento registrado. | Facilita la lectura de evidencias. |

## Reglas de integridad

- `PK_AuditoriaCambios`: clave primaria de la tabla historica.
- `CK_AuditoriaCambios_operacion`: limita la operacion a `INSERT`, `UPDATE` o `DELETE`.
- `CK_AuditoriaCambios_tabla_afectada`: evita nombres de tabla vacios.
- `DF_AuditoriaCambios_fecha_evento`: registra automaticamente fecha y hora.
- `DF_AuditoriaCambios_usuario_sql`: registra automaticamente el usuario SQL.

## Indices

- `IX_AuditoriaCambios_tabla_operacion_fecha`: facilita consultas por tabla, operacion y fecha.
- `IX_AuditoriaCambios_registro_afectado`: facilita rastrear el historial de un registro especifico.

## Integracion con triggers

La tabla recibe registros desde los triggers creados para:

- `Clientes`: insercion, actualizacion y eliminacion.
- `Reservas`: insercion, actualizacion y eliminacion.

