EXECUTE AS USER = 'usuario_analitico';

SELECT TOP 5 *
FROM dbo.Clientes;

SELECT TOP 5 *
FROM dbo.Reservas;

SELECT TOP 5 *
FROM dbo.AuditoriaCambios;

REVERT;
GO


--FALLA
EXECUTE AS USER = 'usuario_analitico';

UPDATE dbo.Clientes
SET previous_cancellations = 99
WHERE id_cliente = 1;

REVERT;
GO



--EVIDENCIAS
SELECT name
FROM sys.database_principals
WHERE type = 'R';

--CONSULTA DE PERMISOS
SELECT *
FROM sys.database_permissions;

SELECT TOP 5 * FROM Clientes;

EXECUTE AS USER = 'usuario_analitico';
GO

UPDATE dbo.Clientes
SET previous_cancellations = 99
WHERE id_cliente = 1;
GO

REVERT;
GO
