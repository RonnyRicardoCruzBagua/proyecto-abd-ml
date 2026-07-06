# 5. Evaluacion, Metricas y Persistencia de Resultados

## Objetivo
Desarrollar la etapa final del proyecto Hotel Booking Demand, integrando la evaluacion de modelos supervisados, resultados de clustering y persistencia de resultados en formato JSON y MongoDB.

## Modelos supervisados evaluados
- Regresion Logistica
- Random Forest

Random Forest fue seleccionado como mejor modelo porque obtuvo mayores valores en accuracy, precision, recall y F1-score.

## Clustering
Se utilizo K-Means para segmentar las reservas. Se evaluaron valores de k entre 2 y 8 usando inercia y coeficiente de silueta. El valor optimo fue k = 2.

## Archivos generados
- scripts/metricas_evaluacion.py
- scripts/exportar_resultados_json.py
- json/resultados_modelos_supervisados.json
- json/resultados_clustering.json
- json/resultados_finales_proyecto.json
- mongodb/insertar_resultados_mongodb.py
- mongodb/consultar_resultados_mongodb.py
- evidencias/evidencia_mongodb.md

## Ejecucion sugerida
1. Ejecutar `python scripts/metricas_evaluacion.py`
2. Revisar los archivos JSON generados en la carpeta `json/`
3. Iniciar MongoDB local
4. Ejecutar `python mongodb/insertar_resultados_mongodb.py`
5. Ejecutar `python mongodb/consultar_resultados_mongodb.py`

