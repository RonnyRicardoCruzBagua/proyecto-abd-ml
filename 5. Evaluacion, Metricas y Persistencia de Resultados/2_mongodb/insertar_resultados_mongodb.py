from pymongo import MongoClient
import json
from pathlib import Path
from datetime import datetime

# Requisitos:
# pip install pymongo
# MongoDB local activo en mongodb://localhost:27017/

BASE = Path(__file__).resolve().parent.parent
JSON_DIR = BASE / "json"

client = MongoClient("mongodb://localhost:27017/")
db = client["hotel_booking_ml"]
coleccion = db["resultados_experimentos"]

archivos = [
    "resultados_modelos_supervisados.json",
    "resultados_clustering.json",
    "resultados_finales_proyecto.json"
]

for archivo in archivos:
    with open(JSON_DIR / archivo, "r", encoding="utf-8") as f:
        documento = json.load(f)
    documento["fecha_insercion"] = datetime.now().isoformat()
    documento["archivo_origen"] = archivo
    coleccion.insert_one(documento)
    print(f"Insertado en MongoDB: {archivo}")

print("Total de documentos en coleccion:", coleccion.count_documents({}))
