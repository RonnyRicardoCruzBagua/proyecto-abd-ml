/*
    Proyecto: Hotel Booking Demand
    Integrante 2: Diseno y Gestion de la Tabla Historica
    Archivo: 5_evidencias_registros_generados.sql

    Objetivo:
    Consultas para tomar evidencias de los registros historicos generados.
*/

USE HotelDB;
GO

SELECT COUNT(*) AS total_registros_historicos
FROM dbo.AuditoriaCambios;
GO

SELECT
    tabla_afectada,
    operacion,
    COUNT(*) AS total_eventos
FROM dbo.AuditoriaCambios
GROUP BY tabla_afectada, operacion
ORDER BY tabla_afectada, operacion;
GO

SELECT TOP 30
    id_auditoria,
    tabla_afectada,
    operacion,
    id_registro_afectado,
    fecha_evento,
    usuario_sql,
    descripcion
FROM dbo.AuditoriaCambios
ORDER BY fecha_evento DESC, id_auditoria DESC;
GO

SELECT TOP 10
    id_auditoria,
    tabla_afectada,
    operacion,
    datos_anteriores,
    datos_nuevos
FROM dbo.AuditoriaCambios
WHERE datos_anteriores IS NOT NULL
   OR datos_nuevos IS NOT NULL
ORDER BY id_auditoria DESC;
GO

SELECT
    i.name AS nombre_indice,
    i.type_desc,
    i.is_unique,
    OBJECT_NAME(i.object_id) AS tabla
FROM sys.indexes i
WHERE i.object_id = OBJECT_ID('dbo.AuditoriaCambios')
  AND i.name IS NOT NULL
ORDER BY i.name;
GO
