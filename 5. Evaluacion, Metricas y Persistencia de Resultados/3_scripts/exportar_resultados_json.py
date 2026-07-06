import json
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
JSON_DIR = BASE / "json"

with open(JSON_DIR / "resultados_finales_proyecto.json", "r", encoding="utf-8") as f:
    resultados = json.load(f)

print("Archivo JSON final cargado correctamente")
print("Proyecto:", resultados["proyecto"])
print("Mejor modelo supervisado:", resultados["resultado_supervisado"]["mejor_modelo"])
print("k optimo clustering:", resultados["resultado_clustering"]["k_optimo"])
