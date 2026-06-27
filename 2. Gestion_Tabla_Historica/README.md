# Diseno y Gestion de la Tabla Historica

Carpeta creada para la actividad del Integrante 2: disenar y gestionar la tabla historica de auditoria en SQL Server.

## Objetivo

Contar con una tabla que almacene el historial completo de cambios realizados en la base de datos, registrando usuario, fecha y hora, tipo de operacion, valores anteriores y valores nuevos.

## Relacion con el trabajo del Integrante 1

El Integrante 1 desarrollo los triggers de auditoria para las tablas criticas `Clientes` y `Reservas` en la carpeta:

`1. Implementacion_de_Auditorias`

Esta actividad complementa ese trabajo gestionando la tabla historica `dbo.AuditoriaCambios`, agregando reglas de integridad, indices, diccionario de datos, pruebas y consultas de evidencia.

## Archivos

1. `1_creacion_tabla_historica.sql`
   - Crea o completa la tabla historica `dbo.AuditoriaCambios`.
   - Agrega Primary Key, CHECK constraints, DEFAULT constraints e indices.

2. `2_integracion_triggers_auditoria.sql`
   - Verifica que los triggers de `Clientes` y `Reservas` existan.
   - Verifica que los triggers registren cambios en `dbo.AuditoriaCambios`.

3. `3_diccionario_datos_tabla_historica.md`
   - Explica cada campo de la tabla historica.
   - Describe reglas de integridad, indices e integracion con triggers.

4. `4_pruebas_almacenamiento_registros.sql`
   - Ejecuta pruebas de INSERT, UPDATE y DELETE en `Clientes` y `Reservas`.
   - Permite validar que se almacenen registros historicos.

5. `5_evidencias_registros_generados.sql`
   - Contiene consultas para tomar capturas de evidencias.
   - Muestra totales, resumen por tabla/operacion y detalle JSON.

## Orden de ejecucion

1. Ejecutar primero la base de datos y tablas principales del proyecto.
2. Ejecutar los scripts del Integrante 1 para crear triggers de auditoria.
3. Ejecutar `1_creacion_tabla_historica.sql`.
4. Ejecutar `2_integracion_triggers_auditoria.sql`.
5. Ejecutar `4_pruebas_almacenamiento_registros.sql`.
6. Ejecutar `5_evidencias_registros_generados.sql` para tomar capturas.

## Resultado esperado

La tabla `dbo.AuditoriaCambios` queda preparada como tabla historica central, con constraints e indices, y recibe automaticamente los registros generados por los triggers cuando se hacen operaciones `INSERT`, `UPDATE` y `DELETE` en tablas criticas.
