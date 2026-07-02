DENY INSERT ON dbo.Clientes TO RolAnalitico;
DENY UPDATE ON dbo.Clientes TO RolAnalitico;
DENY DELETE ON dbo.Clientes TO RolAnalitico;

DENY INSERT ON dbo.Reservas TO RolAnalitico;
DENY UPDATE ON dbo.Reservas TO RolAnalitico;
DENY DELETE ON dbo.Reservas TO RolAnalitico;

DENY INSERT ON dbo.AuditoriaCambios TO RolAnalitico;
DENY UPDATE ON dbo.AuditoriaCambios TO RolAnalitico;
DENY DELETE ON dbo.AuditoriaCambios TO RolAnalitico;
GO


--VERIFICACIONES DE PERMISOS

SELECT
    dp.name AS Rol,
    o.name AS Objeto,
    p.permission_name,
    p.state_desc
FROM sys.database_permissions p
JOIN sys.objects o
    ON p.major_id = o.object_id
JOIN sys.database_principals dp
    ON p.grantee_principal_id = dp.principal_id
WHERE dp.name = 'RolAnalitico';
GO