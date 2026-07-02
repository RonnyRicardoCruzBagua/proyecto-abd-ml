Configuración del Rol Analítico
Objetivo
Crear un rol de SQL Server llamado RolAnalitico que tenga acceso únicamente a consultas y visualización de información, sin permitir modificaciones en los datos.
La idea es que usuarios analíticos puedan:
✅ Consultar vistas
✅ Ejecutar SELECT sobre información analítica
✅ Generar reportes
Pero NO puedan:
❌ INSERT
❌ UPDATE
❌ DELETE
❌ ALTER TABLE

Lo que realizo fue lo siguiente

Fue implementar el rol de seguridad RolAnalitico utilizando el modelo basado en roles de SQL Server.
Se creó un rol con permisos exclusivos de lectura sobre las tablas, la vista analítica y la tabla de auditoría del proyecto. Además, 
se aplicaron sentencias GRANT para permitir consultas y sentencias DENY para impedir modificaciones. Finalmente,
se realizaron pruebas para verificar que el usuario puede consultar información pero no alterar los datos.
