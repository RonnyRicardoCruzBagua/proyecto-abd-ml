# **Informe de resultados - Modelado No Supervisado (Clustering)**

## Objetivo

Implementar K-Means para identificar segmentos o patrones ocultos dentro de las reservas hoteleras del proyecto Hotel Booking Demand.

---

## Dataset utilizado

Se utilizo el archivo preparado por la etapa de preprocesamiento:

`PREPROCESAMIENTO_LIMPIEZA_DATOS/8_dataset_preparado_ml.csv`

Este dataset contiene 87,370 registros y 31 columnas transformadas y escaladas.

Para el modelado se excluyeron las variables `is_canceled`, `reservation_status` y `reservation_status_date`, porque representan resultados o estados posteriores de la reserva. El clustering se realizo con 28 variables explicativas.

---

## Algoritmo implementado

Se aplico K-Means con valores de `k` entre 2 y 8. Para cada valor se calcularon:

- Inercia, usada en el Metodo del Codo.
- Coeficiente de Silueta, usado para evaluar separacion y cohesion de los clusters.

---

## Numero optimo de clusters

El mejor valor segun el coeficiente de silueta fue:

**k = 2**

## Metricas obtenidas

| k | inercia | coeficiente_silueta |
| --- | --- | --- |
| 2 | 2261582.9946 | 0.1671 |
| 3 | 2119108.9505 | 0.1087 |
| 4 | 2024794.8570 | 0.1171 |
| 5 | 1934323.1726 | 0.1236 |
| 6 | 1857212.1169 | 0.1037 |
| 7 | 1788503.5086 | 0.0870 |
| 8 | 1716271.3007 | 0.0944 |

---

## Perfil general de clusters

| cluster | total_registros | porcentaje_cancelacion | lead_time_promedio | adr_promedio | noches_promedio | huespedes_promedio | solicitudes_promedio | cambios_promedio | cancelaciones_previas_promedio | porcentaje_registros |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0 | 18830 | 13.8900 | 44.7700 | 95.7000 | 2.8400 | 1.8000 | 0.4800 | 0.4300 | 0.0900 | 21.5500 |
| 1 | 68540 | 31.2400 | 89.5700 | 109.2700 | 3.8500 | 2.0900 | 0.7600 | 0.2300 | 0.0100 | 78.4500 |

## Interpretacion de patrones encontrados

- Cluster 0: 18830 registros (21.55%). Cancelacion promedio 13.89%, anticipacion 44.77 dias, ADR 95.7, noches 2.84. Predominan hotel Resort Hotel, segmento Direct y cliente Transient.
- Cluster 1: 68540 registros (78.45%). Cancelacion promedio 31.24%, anticipacion 89.57 dias, ADR 109.27, noches 3.85. Predominan hotel City Hotel, segmento Online TA y cliente Transient.

## Graficas generadas

- `graficas/01_metodo_codo.png`
- `graficas/02_coeficiente_silueta.png`
- `graficas/03_distribucion_clusters.png`
- `graficas/04_perfil_clusters.png`
- `graficas/05_clusters_pca.png`

---

## Conclusiones

El modelado no supervisado permitio segmentar las reservas hoteleras en grupos con diferencias en anticipacion de reserva, tarifa promedio, duracion de estadia, solicitudes especiales y comportamiento de cancelacion. Estos segmentos pueden apoyar estrategias de gestion hotelera, analisis de clientes y futuras acciones predictivas.
