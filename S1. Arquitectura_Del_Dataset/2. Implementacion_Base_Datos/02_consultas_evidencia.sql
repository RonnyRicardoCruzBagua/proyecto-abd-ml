/*
    Consultas para evidencias de ejecucion en SQL Server.
    Ejecutar despues de 01_creacion_base_datos.sql.
*/

USE HotelDB;
GO

-- 1. Evidencia de tablas creadas
SELECT
    TABLE_SCHEMA,
    TABLE_NAME
FROM INFORMATION_SCHEMA.TABLES
WHERE TABLE_TYPE = 'BASE TABLE'
ORDER BY TABLE_NAME;
GO

-- 2. Evidencia de columnas y tipos de datos
SELECT
    TABLE_NAME,
    COLUMN_NAME,
    DATA_TYPE,
    CHARACTER_MAXIMUM_LENGTH,
    IS_NULLABLE
FROM INFORMATION_SCHEMA.COLUMNS
ORDER BY TABLE_NAME, ORDINAL_POSITION;
GO

-- 3. Evidencia de primary keys y unique constraints
SELECT
    tc.TABLE_NAME,
    tc.CONSTRAINT_NAME,
    tc.CONSTRAINT_TYPE,
    kcu.COLUMN_NAME
FROM INFORMATION_SCHEMA.TABLE_CONSTRAINTS tc
LEFT JOIN INFORMATION_SCHEMA.KEY_COLUMN_USAGE kcu
    ON tc.CONSTRAINT_NAME = kcu.CONSTRAINT_NAME
WHERE tc.CONSTRAINT_TYPE IN ('PRIMARY KEY', 'UNIQUE')
ORDER BY tc.TABLE_NAME, tc.CONSTRAINT_TYPE, tc.CONSTRAINT_NAME;
GO

-- 4. Evidencia de foreign keys
SELECT
    fk.name AS foreign_key,
    OBJECT_NAME(fk.parent_object_id) AS tabla_origen,
    COL_NAME(fkc.parent_object_id, fkc.parent_column_id) AS columna_origen,
    OBJECT_NAME(fk.referenced_object_id) AS tabla_referenciada,
    COL_NAME(fkc.referenced_object_id, fkc.referenced_column_id) AS columna_referenciada
FROM sys.foreign_keys fk
INNER JOIN sys.foreign_key_columns fkc
    ON fk.object_id = fkc.constraint_object_id
ORDER BY tabla_origen, foreign_key;
GO

-- 5. Evidencia de check constraints y default constraints
SELECT
    OBJECT_NAME(parent_object_id) AS tabla,
    name AS constraint_name,
    type_desc,
    definition
FROM sys.check_constraints
UNION ALL
SELECT
    OBJECT_NAME(parent_object_id) AS tabla,
    name AS constraint_name,
    type_desc,
    definition
FROM sys.default_constraints
ORDER BY tabla, constraint_name;
GO

-- 6. Evidencia de indices creados
SELECT
    OBJECT_NAME(i.object_id) AS tabla,
    i.name AS indice,
    i.type_desc,
    i.is_unique
FROM sys.indexes i
WHERE OBJECT_NAME(i.object_id) IN (
    'Hoteles', 'Clientes', 'CanalesReserva', 'Habitaciones',
    'EstadosReserva', 'FechasLlegada', 'Reservas'
)
AND i.name IS NOT NULL
ORDER BY tabla, indice;
GO

--