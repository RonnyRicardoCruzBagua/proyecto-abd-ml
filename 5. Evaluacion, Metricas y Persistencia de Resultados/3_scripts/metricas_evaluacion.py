import pandas as pd
import json
from pathlib import Path

# Script de evaluacion de metricas del proyecto Hotel Booking Demand
# Este script carga las metricas supervisadas y de clustering y genera archivos JSON.

BASE = Path(__file__).resolve().parent.parent
JSON_DIR = BASE / "json"
JSON_DIR.mkdir(exist_ok=True)

metricas_supervisadas = pd.DataFrame([
    {"Modelo": "Regresion Logistica", "Accuracy": 0.7757239327000115, "Precision": 0.6690839694656489, "Recall": 0.3648283038501561, "F1-score": 0.4721885521885522},
    {"Modelo": "Random Forest", "Accuracy": 0.8523520659265194, "Precision": 0.7736777367773677, "Recall": 0.6545265348595213, "F1-score": 0.7091319052987599}
])

mejor_modelo = metricas_supervisadas.sort_values("F1-score", ascending=False).iloc[0]
print("Metricas supervisadas:")
print(metricas_supervisadas)
print("\nMejor modelo:", mejor_modelo["Modelo"])

metricas_kmeans = pd.DataFrame([
    {"k":2,"inercia":2261582.994600403,"coeficiente_silueta":0.1670942744493208},
    {"k":3,"inercia":2119108.9504545606,"coeficiente_silueta":0.10867578424301241},
    {"k":4,"inercia":2024794.8570093247,"coeficiente_silueta":0.11714475614961625},
    {"k":5,"inercia":1934323.1725540117,"coeficiente_silueta":0.12356120844840075},
    {"k":6,"inercia":1857212.1168709286,"coeficiente_silueta":0.1037273685880784},
    {"k":7,"inercia":1788503.5085578943,"coeficiente_silueta":0.08704678668737023},
    {"k":8,"inercia":1716271.3006503005,"coeficiente_silueta":0.09442054675391946}
])

k_optimo = int(metricas_kmeans.sort_values("coeficiente_silueta", ascending=False).iloc[0]["k"])
print("\nMetricas K-Means:")
print(metricas_kmeans)
print("\nk optimo:", k_optimo)
