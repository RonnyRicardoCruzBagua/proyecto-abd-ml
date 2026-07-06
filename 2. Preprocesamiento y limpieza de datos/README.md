# PREPROCESAMIENTO, LIMPIEZA Y PREPARACIÓN DE DATOS

## Integrante

**Victoria  Moyon **

---

# Descripción General

Esta etapa corresponde al proceso de preprocesamiento de datos del proyecto de analítica predictiva sobre la cancelación de reservas hoteleras, utilizando el dataset **Hotel Booking Demand**.

El objetivo principal fue mejorar la calidad de la información mediante técnicas de limpieza, transformación y escalamiento de datos para garantizar que el conjunto de datos esté preparado para las fases posteriores de entrenamiento, validación y despliegue de modelos de Machine Learning.

Durante esta actividad se realizó un análisis exhaustivo de la calidad de los datos, identificando problemas relacionados con valores faltantes, registros duplicados y variables categóricas que requerían transformación.

---

# Objetivos de la Actividad

## Objetivo General

Preparar y optimizar el conjunto de datos para su utilización en modelos de Machine Learning mediante técnicas de preprocesamiento.

## Objetivos Específicos

- Analizar la estructura general del dataset.
- Identificar valores nulos y registros duplicados.
- Aplicar técnicas de limpieza de datos.
- Eliminar atributos con alta proporción de valores faltantes.
- Transformar variables categóricas a representación numérica.
- Escalar variables numéricas mediante técnicas de normalización.
- Generar un dataset final listo para el entrenamiento de modelos predictivos.

---

# Estructura de Archivos

## 1_carga_dataset.ipynb

### Descripción

Se realizó la carga inicial del conjunto de datos y una exploración preliminar para conocer sus características generales.

### Actividades Realizadas

- Importación de librerías necesarias.
- Lectura del archivo hotel_bookings.csv.
- Verificación de dimensiones del dataset.
- Visualización de registros iniciales.
- Análisis de tipos de datos.
- Estadísticas descriptivas generales.

### Resultados Obtenidos

- Registros iniciales: 119390
- Columnas iniciales: 32

---

## 2_identificacion_nulos_duplicados.ipynb

### Descripción

Se efectuó un análisis de calidad de datos para detectar posibles inconsistencias dentro del conjunto de datos.

### Actividades Realizadas

- Detección de valores faltantes.
- Cálculo de porcentaje de datos nulos.
- Identificación de registros duplicados.
- Perfilado de atributos.
- Generación de métricas de calidad de datos.

### Valores Nulos Identificados

| Variable | Valores Nulos |
|----------|---------------|
| children | 4 |
| country | 488 |
| agent | 16340 |
| company | 112593 |

### Registros Duplicados

Registros duplicados encontrados:

31994 registros

### Conclusión

El análisis permitió identificar variables que requerían tratamiento especial antes de continuar con el modelado.

---

## 3_limpieza_datos.ipynb

### Descripción

Se aplicaron diferentes técnicas de limpieza sobre las variables afectadas por problemas de calidad.

### Actividades Realizadas

#### Tratamiento de Valores Faltantes

Se aplicó imputación de datos utilizando técnicas estadísticas apropiadas para cada variable.

##### Variable children

Método utilizado:

- Mediana

Razón:

La mediana reduce el impacto de valores atípicos.

##### Variable country

Método utilizado:

- Moda

Razón:

Representa la categoría más frecuente dentro del conjunto de datos.

##### Variable agent

Método utilizado:

- Sustitución por valor 0

Razón:

Representa la ausencia de información del agente asociado.

---

### Eliminación de Variables

#### Variable company

Esta variable presentaba más del 94% de valores faltantes.

Por esta razón se eliminó completamente del conjunto de datos para evitar introducir ruido durante las fases posteriores de análisis y entrenamiento.

---

### Eliminación de Registros Duplicados

Se eliminaron todos los registros duplicados encontrados en el dataset.

### Resultados

| Métrica | Valor |
|----------|---------|
| Registros Iniciales | 119390 |
| Registros Finales | 87370 |
| Columnas Iniciales | 32 |
| Columnas Finales | 31 |
| Valores Nulos Finales | 0 |
| Registros Duplicados Finales | 0 |

---

## 4_transformacion_variables.ipynb

### Descripción

Se realizó la transformación de variables categóricas mediante la técnica Label Encoding.

### Objetivo

Convertir variables de tipo texto a representaciones numéricas compatibles con algoritmos de Machine Learning.

### Variables Transformadas

- hotel
- arrival_date_month
- meal
- country
- market_segment
- distribution_channel
- reserved_room_type
- assigned_room_type
- deposit_type
- customer_type
- reservation_status
- reservation_status_date

### Técnica Utilizada

Label Encoding

### Resultado

Todas las variables categóricas fueron convertidas exitosamente a valores numéricos.

### Archivo Generado

```
7_dataset_transformado.csv
```

---

## 5_escalamiento_datos.ipynb

### Descripción

Se realizó el escalamiento de las variables numéricas mediante la técnica StandardScaler.

### Objetivo

Garantizar que todas las variables trabajen en una escala homogénea para evitar sesgos durante el entrenamiento de modelos de Machine Learning.

### Técnica Utilizada

StandardScaler

### Beneficios del Escalamiento

- Mejora la convergencia de algoritmos de entrenamiento.
- Reduce la influencia de variables con magnitudes mayores.
- Facilita la comparación entre características.
- Optimiza el rendimiento de modelos predictivos.

### Validación

Después del escalamiento se verificó que:

- Media cercana a 0.
- Desviación estándar cercana a 1.

### Resultado

Variables escaladas:

31

### Archivo Generado

```
8_dataset_preparado_ml.csv
```

---

# Archivos Generados Durante la Actividad

## 6_dataset_limpio.csv

Dataset libre de valores nulos y registros duplicados.

## 7_dataset_transformado.csv

Dataset con variables categóricas codificadas.

## 8_dataset_preparado_ml.csv

Dataset final preparado para algoritmos de Machine Learning.

---

# Flujo de Procesamiento Aplicado

1. Carga del dataset.
2. Exploración inicial.
3. Identificación de valores faltantes.
4. Identificación de registros duplicados.
5. Tratamiento de datos faltantes.
6. Eliminación de variables no útiles.
7. Eliminación de registros duplicados.
8. Transformación de variables categóricas.
9. Escalamiento de variables numéricas.
10. Validación de calidad de datos.
11. Generación del dataset final.

---

# Resultado Final

## Estado Inicial

- Registros: 119390
- Columnas: 32

## Estado Final

- Registros: 87370
- Columnas: 31
- Valores nulos: 0
- Duplicados: 0

---

# Entregable para la Siguiente Etapa

El archivo que deberá utilizarse en las siguientes fases del proyecto es:

```
8_dataset_preparado_ml.csv
```

Este archivo contiene los datos completamente limpios, transformados y escalados, encontrándose listo para los procesos de entrenamiento, validación y evaluación de modelos de Machine Learning.