# ==================================
# PERSISTENCIA HÍBRIDA
# SQL + ML + MongoDB
# ==================================

import pyodbc
import pandas as pd
from pymongo import MongoClient
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from datetime import datetime

# ==================================
# 1. CONEXIÓN A SQL SERVER
# ==================================
print("🔹 Conectando a SQL Server...")

conn = pyodbc.connect(
    r"DRIVER={ODBC Driver 17 for SQL Server};"
    r"SERVER=DESKTOP-UDI71R1\SQLEXPRESS;"
    r"DATABASE=HotelDB;"
    r"Trusted_Connection=yes;"
)

print("✅ Conexión exitosa a SQL Server")

# ==================================
# 2. OBTENER DATOS DESDE SQL
# ==================================
query = "SELECT * FROM vw_prediccion_cancelacion"

df = pd.read_sql(query, conn)

print("✅ Datos cargados:", df.shape)

# ✅ LIMPIAR ESPACIOS INVISIBLES (CLAVE)
df.columns = df.columns.str.strip()

print("Columnas del DataFrame:")
print(df.columns)

# ==================================
# 3. PREPARAR DATOS
# ==================================
print("🔹 Preparando datos...")

# ✅ USAR COLUMNA CORRECTA (BINARIA)
col_objetivo = "is_canceled"

# asegurar que sea tipo numérico (0 y 1)
df[col_objetivo] = df[col_objetivo].astype(int)

y = df[col_objetivo]

X = df.select_dtypes(include=['int64', 'float64']).drop(columns=[col_objetivo])

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2
)

# ==================================
# 4. MODELO MACHINE LEARNING
# ==================================
print("🔹 Entrenando modelo...")

modelo = RandomForestClassifier(
    n_estimators=100,
    max_depth=10
)

modelo.fit(X_train, y_train)

y_pred = modelo.predict(X_test)

# ==================================
# 5. MÉTRICAS (YA SIN ERROR ✅)
# ==================================
accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred)
recall = recall_score(y_test, y_pred)
f1 = f1_score(y_test, y_pred)

print("✅ Accuracy:", accuracy)
print("✅ Precision:", precision)
print("✅ Recall:", recall)
print("✅ F1 Score:", f1)

# ==================================
# 6. CONEXIÓN A MONGODB
# ==================================
print("🔹 Conectando a MongoDB...")

uri = "mongodb+srv://equipo:987654321@cluster0.p305n84.mongodb.net/?appName=Cluster0"

client = MongoClient(uri)

db = client["HotelML"]
coleccion = db["experimentos_ml"]

# ==================================
# 7. DOCUMENTO JSON
# ==================================
documento = {
    "fecha": datetime.now().strftime("%Y-%m-%d"),
    "algoritmo": "Random Forest",
    "hiperparametros": {
        "n_estimators": 100,
        "max_depth": 10
    },
    "metricas": {
        "accuracy": float(accuracy),
        "precision": float(precision),
        "recall": float(recall),
        "f1_score": float(f1)
    }
}

# ==================================
# 8. INSERTAR EN MONGO
# ==================================
coleccion.insert_one(documento)

print("✅ Experimento guardado en MongoDB")

# ==================================
# 9. EVIDENCIA
# ==================================
print("\n📄 DOCUMENTOS EN MONGO:")

for doc in coleccion.find().limit(3):
    print(doc)
