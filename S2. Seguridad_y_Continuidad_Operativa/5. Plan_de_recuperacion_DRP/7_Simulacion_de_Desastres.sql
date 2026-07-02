-- 1. Verificar los registros

SELECT COUNT(*)
FROM Reservas;

-- 2. Simular el desastre

-- Antes de hacer esto se recomienda hacer un backup completo ante cualquier perdida importante

-- Esta es la mas eficiente
DELETE FROM Reservas; -- Puede usarse de ejemplo

-- Se puede usar tambien para el ejemplo, pero solo se debe de elegir uno
DROP TABLE Reservas; -- Puede usarse de ejemplo

-- 3. Verificar las perdidas

SELECT COUNT(*)
FROM Reservas;

-- 4. Ejecutar la restauracion de la base de datos

RESTORE DATABASE HotelDB
FROM DISK='C:\Backups\HotelDB_Full.bak'
WITH REPLACE;

-- 5. Validar la recuperacion

SELECT COUNT(*)
FROM Reservas;

-- 6. Validacion posterior a la recuperacion

SELECT COUNT(*) FROM Hoteles;
SELECT COUNT(*) FROM Clientes;
SELECT COUNT(*) FROM Reservas;
SELECT COUNT(*) FROM AuditoriaCambios;

-- Validar las auditorias

SELECT TOP 20 *
FROM AuditoriaCambios
ORDER BY fecha_evento DESC;

-- Validar los triggers

SELECT name
FROM sys.triggers;