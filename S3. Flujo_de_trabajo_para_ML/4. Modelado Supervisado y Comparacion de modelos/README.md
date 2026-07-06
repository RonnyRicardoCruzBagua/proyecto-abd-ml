# Modelado Supervisado y Comparación de Modelos

## Proyecto

**Hotel Booking Demand**

## Tema

**Predicción de cancelación de reservas hoteleras y segmentación de clientes mediante Machine Learning y persistencia híbrida SQL Server + MongoDB**

---

## Descripción general

En esta parte del proyecto se realizó el modelado supervisado para predecir si una reserva hotelera será cancelada o no.

La variable objetivo utilizada fue:

``` is_canceled ```

Donde:
1. **0 = reserva no cancelada**
2. **1 = reserva cancelada**

---
**Archivos utilizados**

Se usaron los archivos generados en la etapa de preprocesamiento:
1. **PREPROCESAMIENTO_LIMPIEZA_DATOS/8_dataset_preparado_ml.csv**
2. **PREPROCESAMIENTO_LIMPIEZA_DATOS/7_dataset_transformado.csv**

El archivo ```8_dataset_preparado_ml.csv``` se utilizó para las variables de entrada X, ya que contiene los datos preparados para Machine Learning, la variable objetivo ```is_canceled``` se tomó desde ```7_dataset_transformado.csv```, porque en ese archivo conserva sus valores correctos:

1. **0 = no cancelada**
2. **1 = cancelada**

Esto fue necesario porque en el dataset preparado la variable ```is_canceled``` estaba escalada.

---
**División de datos**

Los datos fueron divididos en:

1. **80% entrenamiento**
2. **20% prueba**

Se utilizó:

- random_state = 42

También se aplicó ```stratify=y``` para mantener una proporción similar de reservas canceladas y no canceladas tanto en entrenamiento como en prueba.

---
**Modelos entrenados**

Se entrenaron dos modelos supervisados:

- Regresión Logística
- Random Forest

Ambos modelos fueron evaluados usando las métricas:

- Accuracy
- Precision
- Recall
- F1-score

### Resultados obtenidos

| Modelo | Accuracy | Precision | Recall | F1-score |
| :--- | :---: | :---: | :---: | :---: |
| **Regresión Logística** | 0.7757 | 0.6691 | 0.3648 | 0.4722 |
| **Random Forest** | 0.8523 | 0.7737 | 0.6545 | 0.7091 |

---
**Mejor modelo**

El mejor modelo fue:
1. **Random Forest**

Random Forest obtuvo mejor rendimiento general que Regresión Logística, además, tuvo mejor capacidad para detectar reservas canceladas, ya que obtuvo mejores valores en ```Recall``` y ```F1-score```.

---
**Resultados generados**

Dentro de la carpeta resultados se generaron los siguientes archivos:
1. **metricas_modelos_supervisados.csv**
2. **matriz_confusion_regresion_logistica.png**
3. **matriz_confusion_random_forest.png**
4. **comparacion_modelos_supervisados.png**

---
**Interpretación breve**

La Regresión Logística tuvo un buen rendimiento general, pero detectó menos reservas canceladas.
Random Forest logró mejores resultados en todas las métricas principales, especialmente al identificar reservas canceladas, por esta razón, Random Forest se considera el modelo con mejor capacidad predictiva para este problema.

---
**Conclusión**

En esta etapa se entrenaron y compararon dos modelos supervisados para predecir cancelaciones hoteleras.
El modelo Random Forest fue seleccionado como el mejor modelo debido a que obtuvo mayor Accuracy, Precision, Recall y F1-score.
Esto indica que Random Forest es más adecuado para apoyar la predicción de cancelaciones de reservas dentro del proyecto



