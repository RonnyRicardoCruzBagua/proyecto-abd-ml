# Persistencia Hibrida y conexion a Mongo DB

Hemos implementado la persistencia híbrida, específicamente en:

•	Integrar el modelo de Machine Learning con una base de datos NoSQL (MongoDB)}

•	Guardar los resultados de los experimentos de forma estructurada

**¿Qué significa persistencia híbrida?**

“Persistencia híbrida es el uso de diferentes tipos de bases de datos para diferentes propósitos.”

En este caso:

-	SQL Server → para datos estructurados (reservas, clientes, etc.)

- MongoDB → para resultados del modelo de Machine Learning

**🔹 ¿Qué hice exactamente?**

*1. Conexión a MongoDB*

Utilicé MongoDB Atlas (en la nube) para no instalar nada local.
Python
from pymongo import MongoClient
client = MongoClient(uri)

*2. Creación de base y colección*

Se creó automáticamente:

-	Base de datos: HotelML

-	Colección: experimentos_ml

*3. Integración con Machine Learning*

Después de que el modelo se entrena en Python:

Tomé sus resultados:

- Accuracy

-	Precision

-	Recall

-	F1 Score

**4. Construcción del documento JSON**
Se creó un documento como este:
 
**5. Almacenamiento en MongoDB**

Python
coleccion.insert_one(documento)
Esto guarda automáticamente cada experimento

**🔹 ¿Por qué usar MongoDB?**

Porque:

-  Permite guardar datos flexibles (JSON)

-  No requiere un esquema rígido

-  Es ideal para resultados de modelos

-  Permite guardar múltiples experimentos fácilmente

Mi aporte fue implementar la persistencia híbrida utilizando MongoDB, donde se almacenan los resultados del modelo de Machine Learning en formato JSON. Esto permite guardar y gestionar experimentos de manera flexible sin afectar la base de datos transaccional en SQL Server.

