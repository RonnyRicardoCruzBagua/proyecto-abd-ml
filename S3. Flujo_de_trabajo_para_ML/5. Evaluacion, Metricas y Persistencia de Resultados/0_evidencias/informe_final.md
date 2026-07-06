# Informe final - Evaluacion, Metricas y Persistencia de Resultados

## 1. Evaluacion de modelos supervisados
Se evaluaron dos modelos supervisados para predecir la variable objetivo `is_canceled`: Regresion Logistica y Random Forest.

### Resultados principales
- Regresion Logistica: accuracy 0.7757, precision 0.6691, recall 0.3648 y F1-score 0.4722.
- Random Forest: accuracy 0.8524, precision 0.7737, recall 0.6545 y F1-score 0.7091.

Random Forest fue el mejor modelo porque obtuvo mejores resultados en todas las metricas. Ademas, detecto mejor las reservas canceladas, lo cual es importante para el objetivo del proyecto.

## 2. Matrices de confusion
La matriz de confusion de Regresion Logistica muestra que el modelo clasifica correctamente muchas reservas no canceladas, pero falla en una cantidad importante de reservas canceladas. Random Forest reduce los falsos negativos y mejora la deteccion de cancelaciones.

## 3. Evaluacion de K-Means
Se aplico K-Means para identificar segmentos de reservas. Se evaluaron valores de k desde 2 hasta 8 utilizando inercia y coeficiente de silueta. El mejor valor fue k = 2.

## 4. Perfil de clusters
- Cluster 0: 18,830 registros, 21.55% del total y 13.89% de cancelacion. Predomina Resort Hotel, segmento Direct y canal Direct.
- Cluster 1: 68,540 registros, 78.45% del total y 31.24% de cancelacion. Predomina City Hotel, segmento Online TA y canal TA/TO.

## 5. Persistencia de resultados
Los resultados se exportaron en formato JSON para permitir su almacenamiento flexible en MongoDB. Los documentos generados contienen metricas, matrices de confusion, metricas de clustering, perfiles de clusters y conclusion final.

## 6. Conclusion
La etapa final permite almacenar, consultar y analizar los resultados obtenidos durante el proceso de Machine Learning. Random Forest se recomienda como modelo final de prediccion y K-Means aporta una segmentacion util para comprender patrones de comportamiento en las reservas hoteleras.
