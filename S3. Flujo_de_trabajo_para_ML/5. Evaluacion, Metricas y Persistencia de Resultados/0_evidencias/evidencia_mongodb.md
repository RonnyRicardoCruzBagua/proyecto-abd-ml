# Evidencia de almacenamiento de resultados en MongoDB

## Base de datos
`hotel_booking_ml`

## Coleccion
`resultados_experimentos`

## Documentos insertados
1. resultados_modelos_supervisados.json
2. resultados_clustering.json
3. resultados_finales_proyecto.json

## Comandos de verificacion en MongoDB Shell
```javascript
use hotel_booking_ml
show collections
db.resultados_experimentos.countDocuments()
db.resultados_experimentos.find({}, {proyecto:1, tipo_modelado:1, archivo_origen:1}).pretty()
```

## Resultado esperado
La coleccion debe contener documentos JSON con las metricas supervisadas, las metricas de K-Means, el perfil de clusters y la conclusion final del proyecto.
