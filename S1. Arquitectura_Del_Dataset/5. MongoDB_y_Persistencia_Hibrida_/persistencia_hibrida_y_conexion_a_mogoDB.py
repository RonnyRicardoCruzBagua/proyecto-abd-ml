# ==================================
# PERSISTENCIA HÍBRIDA
# SQL + ML + MongoDB
# ==================================

import pyodbc
import pandas as pd

from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score
)

from datetime import datetime


# ==================================
# 1. CONEXIÓN A SQL SERVER
# ==================================

print("🔹 Conectando a SQL Server...")

conn = pyodbc.connect(
    r"DRIVER={ODBC Driver 17 for SQL Server};"
    r"SERVER=DESKTOP-5NRS7M9\SQLEXPRESS;"
    r"DATABASE=HotelDB;"
    r"Trusted_Connection=yes;"
    r"TrustServerCertificate=yes;"
)

print("✅ Conexión exitosa a SQL Server")


# ==================================
# 2. OBTENER DATOS DESDE SQL
# ==================================

query = "SELECT * FROM vw_prediccion_cancelacion"

df = pd.read_sql(query, conn)

print("✅ Datos cargados:", df.shape)

# Limpiar espacios invisibles de los nombres
# de las columnas
df.columns = df.columns.str.strip()

print("Columnas del DataFrame:")
print(df.columns.tolist())


# ==================================
# 3. PREPARAR DATOS
# ==================================

print("🔹 Preparando datos...")

col_objetivo = "is_canceled"

# Comprobar que la columna objetivo existe
if col_objetivo not in df.columns:
    raise ValueError(
        f"No existe la columna '{col_objetivo}'. "
        f"Columnas encontradas: {df.columns.tolist()}"
    )

# Convertir la columna objetivo a número
df[col_objetivo] = pd.to_numeric(
    df[col_objetivo],
    errors="coerce"
)

# Eliminar registros sin valor objetivo
df = df.dropna(subset=[col_objetivo])

df[col_objetivo] = df[col_objetivo].astype(int)

# Variable que se quiere predecir
y = df[col_objetivo]

# Seleccionar columnas numéricas
X = df.select_dtypes(
    include=["number"]
).drop(
    columns=[col_objetivo],
    errors="ignore"
)

# Reemplazar valores vacíos en variables predictoras
X = X.fillna(0)

print("Variables utilizadas por el modelo:")
print(X.columns.tolist())

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)


# ==================================
# 4. MODELO MACHINE LEARNING
# ==================================

print("🔹 Entrenando modelo...")

modelo = RandomForestClassifier(
    n_estimators=100,
    max_depth=10,
    random_state=42
)

modelo.fit(X_train, y_train)

y_pred = modelo.predict(X_test)


# ==================================
# 5. MÉTRICAS
# ==================================

accuracy = accuracy_score(y_test, y_pred)

precision = precision_score(
    y_test,
    y_pred,
    zero_division=0
)

recall = recall_score(
    y_test,
    y_pred,
    zero_division=0
)

f1 = f1_score(
    y_test,
    y_pred,
    zero_division=0
)

print("✅ Accuracy:", accuracy)
print("✅ Precision:", precision)
print("✅ Recall:", recall)
print("✅ F1 Score:", f1)


# ==================================
# 6. CONEXIÓN A MONGODB
# ==================================

print("🔹 Conectando a MongoDB...")

try:
    # MongoDB local mostrado en Compass
    uri = "mongodb://localhost:27017/"

    client = MongoClient(
        uri,
        serverSelectionTimeoutMS=5000
    )

    # Comprobar la conexión
    client.admin.command("ping")

    # Base de datos
    db = client["HotelML"]

    # Colección
    coleccion = db["experimentos_ml"]

    print("✅ Conexión exitosa a MongoDB")
    print("✅ Base de datos: HotelML")
    print("✅ Colección: experimentos_ml")

except ServerSelectionTimeoutError as error:
    print("❌ No se pudo conectar a MongoDB")
    print(error)

    conn.close()

    raise


# ==================================
# 7. DOCUMENTO JSON
# ==================================

documento = {
    "fecha": datetime.now(),
    "algoritmo": "Random Forest",

    "hiperparametros": {
        "n_estimators": 100,
        "max_depth": 10,
        "random_state": 42
    },

    "datos_entrenamiento": {
        "total_registros": int(len(df)),
        "registros_entrenamiento": int(len(X_train)),
        "registros_prueba": int(len(X_test)),
        "cantidad_variables": int(X.shape[1])
    },

    "metricas": {
        "accuracy": float(accuracy),
        "precision": float(precision),
        "recall": float(recall),
        "f1_score": float(f1)
    }
}


# ==================================
# 8. INSERTAR EN MONGODB
# ==================================

resultado = coleccion.insert_one(documento)

print("✅ Experimento guardado en MongoDB")
print("✅ ID del documento:", resultado.inserted_id)


# ==================================
# 9. EVIDENCIA
# ==================================

print("\n📄 ÚLTIMOS DOCUMENTOS EN MONGODB:")

documentos = coleccion.find().sort(
    "fecha",
    -1
).limit(3)

for doc in documentos:
    print(doc)


# ==================================
# 10. CERRAR CONEXIONES
# ==================================

conn.close()
client.close()

print("\n✅ Conexión a SQL Server cerrada")
print("✅ Conexión a MongoDB cerrada")
print("✅ Proceso terminado correctamente")