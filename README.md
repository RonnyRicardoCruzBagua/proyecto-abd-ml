# **Universidad Nacional de Chimborazo**

![Unach](Unach.png)

## Título del proyecto
Predicción de cancelación de reservas hoteleras y segmentación de clientes mediante Machine Learning y persistencia
híbrida.

## Dataset a usar:
    - Hotel booking demanda
Se encuentra en el siguiente enlace: https://www.kaggle.com/datasets/jessemostipak/hotel-booking-demand

## Objetivo general:
- Diseñar e implementar una solución analítica e infraestructural integral que combine una arquitectura de persistencia híbrida (SQL Server y MongoDB) para asegurar la gestión, gobernanza e integridad de datos masivos, con el entrenamiento, evaluación y despliegue de modelos de Machine Learning (supervisados y no supervisados) orientados a resolver una problemática real del entorno actual.

## Intengrantes:
    - Isacc Cadena
    - Ronny Cruz
    - Cristina Lima
    - Victoria Moyon
    - Cristopher Sanchéz

## Nuestro Objetivo:
Desarrollar una solución basada en una infraestructura de persistencia híbrida y técnicas de Machine Learning para
predecir la cancelación de reservas hoteleras, apoyando la toma de decisiones en la gestión de hoteles urbanos y
resorts.

## Objetivos Especificos:
1. Analizar y procesar los datos históricos de reservas hoteleras, considerando variables como fecha de llegada, duración de la estadía, tipo de cliente, canal de distribución, país de origen, historial de cancelaciones, solicitudes especiales y tarifa diaria promedio.
2. Diseñar e implementar una infraestructura de persistencia híbrida que permita almacenar, gestionar y consultar eficientemente la información de las reservas hoteleras.
3. Entrenar y evaluar un modelo de Machine Learning capaz de predecir la probabilidad de cancelación de una reserva a partir de los datos históricos disponibles.
4. Comparar el desempeño del modelo mediante métricas de evaluación adecuadas para garantizar la precisión y confiabilidad de las predicciones.
5. Desplegar el modelo predictivo en un entorno funcional que facilite su uso como herramienta de apoyo para la toma de decisiones en la gestión hotelera.
6. Generar información útil para optimizar la planificación operativa y reducir el impacto de las cancelaciones en los establecimientos hoteleros.

## Tecnologias Usadas:

### Bases de Datos
- SQL Server
- MongoDB

### Lenguajes de Programación
- Python
- Tsql
- Jupiter Notebooks

### Librerías para Ciencia de Datos
- Pandas
- NumPy
- Scikit-Learn
- Matplotlib
- Seaborn

### Entorno de Desarrollo
- Visual Studio Code
- Jupyter Notebook

### Control de Versiones
- Git
- GitHub

### Dataset
- Hotel Booking Demand

## Interfaz visual con Streamlit

La actividad final se implemento en `app_streamlit.py`. La aplicacion permite:

- Ingresar datos de una nueva reserva hotelera mediante formularios interactivos.
- Predecir en tiempo real la probabilidad de cancelacion con Random Forest.
- Consultar reservas del dataset del proyecto, registros creados desde la interfaz y, si esta disponible, la vista `vw_prediccion_cancelacion` de SQL Server.
- Registrar nuevas reservas y guardar predicciones en `streamlit_data/reservas_interfaz.csv`.
- Conectarse opcionalmente a MongoDB para persistir predicciones.
- Visualizar indicadores y graficas de cancelaciones por hotel, mes y segmento de mercado.

Ejecucion sugerida:

```bash
pip install -r requirements.txt
streamlit run app_streamlit.py
```

Si SQL Server o MongoDB no estan activos, la aplicacion sigue funcionando con los archivos CSV del proyecto.
