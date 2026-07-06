# Análisis de columnas — Hotel Booking Demand

## Objetivo
Explicar detalladamente qué columnas del dataset `hotel_bookings.csv` se usarán para el proyecto (predicción de cancelación y segmentación), qué significa cada una, cómo se transformarán y por qué se incluyen o descartan.

## Contexto del dataset
- Registros: ~119,390 filas.
- Columnas: 32 (cada fila = una reserva).
- Target principal: `is_canceled` (0 = no cancelada, 1 = cancelada).
- Tipos de hotel: `City Hotel`, `Resort Hotel`.

## Variable objetivo
- `is_canceled` — variable binaria que indica si la reserva fue cancelada. El modelo supervisado deberá predecir esta columna usando solo información disponible antes de que ocurra la cancelación.

## Columnas que usaremos para predecir (`X`) y por qué
Estas variables serán candidatas para modelos supervisados (Regresión Logística, Árboles, Random Forest):

- `hotel`: tipo de hotel (City / Resort). Puede mostrar diferencias de comportamiento.
- `lead_time`: días entre reserva y llegada. Reservas con alta anticipación tienen diferente riesgo.
- `arrival_date_month`: mes de llegada (estacionalidad).
- `arrival_date_week_number`: semana del año (patrones estacionales).
- `arrival_date_day_of_month`: día del mes (posibles efectos calendario).
- `stays_in_weekend_nights`: noches de fin de semana (tipo de viaje).
- `stays_in_week_nights`: noches de entre semana.
- `adults`, `children`, `babies`: composición del grupo, útil para detectar reservas familiares o de negocio.
- `meal`: tipo de régimen contratado (paquete/cliente).
- `country`: país de origen (agrupar países raros como "Other").
- `market_segment`: segmento de mercado (agencia, directo, corporate, etc.).
- `distribution_channel`: canal de distribución.
- `is_repeated_guest`: cliente repetido (menos propenso a cancelar).
- `previous_cancellations`: historial de cancelaciones previas (predictor fuerte).
- `previous_bookings_not_canceled`: historial de reservas no canceladas.
- `reserved_room_type`: tipo de habitación reservada (p. ej. por precio/preferencia).
- `booking_changes`: número de cambios en la reserva (incertidumbre).
- `deposit_type`: tipo de depósito (No Deposit, Refundable, Non Refund).
- `days_in_waiting_list`: días en lista de espera.
- `customer_type`: tipo de cliente (Transient, Contract, Group, etc.).
- `adr`: tarifa diaria promedio (precio relativo).
- `required_car_parking_spaces`: espacios de parking solicitados.
- `total_of_special_requests`: número de solicitudes especiales.

> Nota: algunas de estas columnas pueden necesitar transformaciones (one-hot, ordinal, agrupación de categorías, imputación de nulos).

## Columnas a revisar (decisión pendiente)
- `agent`: puede tener muchos nulos; transformar a `has_agent` (sí/no) si procede.
- `company`: muchos nulos; transformar a `has_company` (sí/no) o mantener según cobertura.
- `assigned_room_type`: puede conocerse después de la gestión; usar con cuidado o descartar para evitar fuga de información.
- `arrival_date_year`: útil para análisis de tendencia pero revisar si aporta a la predicción en producción.

## Columnas a descartar (evitan fuga de información)
Estas columnas contienen información posterior al resultado y pueden producir leakage si se usan en entrenamiento:

- `reservation_status` (ej.: Check-Out, Canceled, No-Show) — indica estado final.
- `reservation_status_date` — fecha del estado final.
- `assigned_room_type` — si se determina que la habitación asignada se conoce después del proceso, descartarla.

Frase justificativa corta: descartamos columnas que se conocen sólo después de que la reserva se resuelva, para asegurar predicciones realistas.

## Columnas para K-Means (clustering)
Para segmentación por comportamiento (no usar `is_canceled` como input):
- `lead_time`, `stays_in_weekend_nights`, `stays_in_week_nights`, `adults`, `children`, `babies`,
- `previous_cancellations`, `previous_bookings_not_canceled`, `booking_changes`, `adr`,
- `required_car_parking_spaces`, `total_of_special_requests`.

Después de crear clusters, comparar la distribución de `is_canceled` por cluster para interpretar qué grupos tienen mayor riesgo.

## Preprocesamiento recomendado
- Imputación: `children` -> 0 si nulo; otras numéricas con mediana o segmentadas por `hotel`.
- Categóricas: agrupar niveles raros (ej. `country` -> `Other`), one-hot encoding o target encoding según algoritmo.
- Escalado: `lead_time`, `adr` y otras numéricas para modelos sensibles a escala si aplica.
- Variables binarias desde nulos: `agent` -> `has_agent`, `company` -> `has_company`.
- Manejar outliers en `adr` y `lead_time` (corte o winsorización).
- Crear features adicionales: interacción `lead_time` x `deposit_type`, ratio de solicitudes por persona, etc.

## Cómo se usarán las variables en los algoritmos
- Regresión Logística: baseline, interpretabilidad de coeficientes (odds ratio).
- Árbol de Decisión: reglas de decisión claras y explicación.
- Random Forest: mejor rendimiento y ranking de importancia de variables.
- K-Means: segmentación con variables numéricas normalizadas.

## Integración con SQL Server y MongoDB
- SQL Server: almacenar datos normalizados (tablas: Hoteles, Reservas, Clientes, Canales, Habitaciones, Estados, Fechas). Crear una vista `vw_reservas_ml` que exponga las columnas necesarias para modelado.
- Python leerá `vw_reservas_ml` vía `pyodbc`/`pandas.read_sql_query` para entrenamiento y scoring.
- MongoDB: persistencia documental para experimentos — cada doc guarda fecha, algoritmo, hiperparámetros y métricas.

Ejemplo de documento de experimento (MongoDB):
```
{
  "fecha": "2026-06-03",
  "algoritmo": "Random Forest",
  "hiperparametros": {"n_estimators": 100, "max_depth": 10, "random_state": 42},
  "metricas": {"accuracy": 0.87, "precision": 0.84, "recall": 0.81, "f1_score": 0.82}
}
```

## Respuestas preparadas para la docente
- Respuesta corta (1-2 frases): "Usaremos variables disponibles antes del resultado (anticipación, duración, tipo de cliente, canal, historial de cancelaciones, depósito, precio y solicitudes especiales) para predecir `is_canceled`. Descartamos columnas que muestran el resultado final como `reservation_status` para evitar fuga de información." 
- Respuesta muy corta (frase): "Usamos columnas previas al resultado (lead_time, previous_cancellations, deposit_type, adr, etc.) y descartamos las que revelan el resultado final."

## Próximos pasos sugeridos
1. Revisar el `hotel_bookings.csv` y confirmar la cobertura de `agent` y `company` (porcentaje de nulos).
2. Definir la vista `vw_reservas_ml` en SQL Server con las columnas seleccionadas.
3. Implementar notebook de extracción `pd.read_sql_query(...)` y notebook de preprocesamiento con pasos reproducibles.
4. Guardar experimentos en MongoDB y documentar cada corrida.

---
_Este Readme se generó a partir del análisis del equipo._
