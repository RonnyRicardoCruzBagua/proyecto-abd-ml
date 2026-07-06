from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["hotel_booking_ml"]
coleccion = db["resultados_experimentos"]

print("Documentos almacenados:", coleccion.count_documents({}))

for doc in coleccion.find({}, {"_id": 0, "proyecto": 1, "tipo_modelado": 1, "archivo_origen": 1, "fecha_insercion": 1}):
    print(doc)
