# **Conexión y extracción de datos desde SQL Server**

Objetivo
> Permitir que Python se conecte a SQL Server, ejecute consultas y cargue los resultados en DataFrames de Pandas para análisis y ML.

Resumen del flujo
- SQL Server → Conexión con `pyodbc` → Ejecución de consultas SQL → Carga en `pandas.DataFrame` → Procesamiento / ML

Prerrequisitos
- Python 3.8+ instalado.
- Controlador ODBC: `ODBC Driver 17 for SQL Server` (o superior) instalado en la máquina.
- Entorno virtual recomendado.
- Dependencias listadas en el archivo raíz `requirements.txt`.

Instalación y ejecución rápida
1. Crear y activar entorno virtual (PowerShell):

```powershell
python -m venv venv
venv\Scripts\Activate.ps1
```

2. Instalar dependencias:

```powershell
pip install -r requirements.txt
```

Configuración de la conexión
- Se recomienda usar variables de entorno para no exponer credenciales.
- Variables sugeridas: `DB_DRIVER`, `DB_SERVER`, `DB_DATABASE`, `DB_TRUSTED`.

Ejemplo de conexión (mínimo reproducible)

```python
import os
import pyodbc
import pandas as pd

driver = os.getenv('DB_DRIVER', 'ODBC Driver 17 for SQL Server')
server = os.getenv('DB_SERVER', r'DESKTOP-UDI71R1\\SQLEXPRESS')
database = os.getenv('DB_DATABASE', 'HotelDB')
trusted = os.getenv('DB_TRUSTED', 'yes')

conn_str = (
	f"DRIVER={{{driver}}};"
	f"SERVER={server};"
	f"DATABASE={database};"
	f"Trusted_Connection={trusted};"
)

try:
	conn = pyodbc.connect(conn_str)
	print('Conexión establecida')
	query = 'SELECT TOP 10 * FROM reservas'  # ejemplo: ajustar a la tabla real
	df = pd.read_sql_query(query, conn)
	print(df.head())
finally:
	conn.close()
```

Notebooks incluidos
- `1_conexion_sql.ipynb`: establece la conexión a SQL Server (ejemplo de `pyodbc.connect`).
- `2_consulta.ipynb`: espacio para las consultas SQL; actualmente contiene el bloque de conexión (agregar consultas y `pandas` cuando proceda).
- `3_extraccion_datos.ipynb`: pensado para extraer los resultados y convertirlos en DataFrames; actualmente contiene el bloque de conexión (añadir `pd.read_sql_query`, limpieza y ejemplos de guardado).

Recomendaciones / próximas mejoras
- Añadir en cada notebook ejemplos concretos de consultas (tablas/vistas usadas) y columnas esperadas.
- Incluir manejo de errores y logs (por ejemplo, `try/except` y cierre correcto de conexión).
- No subir credenciales: usar variables de entorno o archivos `.env` ignorados por git.
- Documentar qué permisos necesita el usuario de la base de datos (lectura en las vistas/tablas usadas).

Seguridad y permisos
- El README asume autenticación integrada (Trusted Connection). Si se usa SQL Auth, no almacenar usuario/contraseña en el repositorio.

Autor y contacto
- Notebooks creados por el equipo de `Flujo_de_trabajo_para_ML`. Para dudas, contactar al autor del notebook correspondiente.

¿Quieres que complete los notebooks con ejemplos de consulta y extracción (yo los edito)?
