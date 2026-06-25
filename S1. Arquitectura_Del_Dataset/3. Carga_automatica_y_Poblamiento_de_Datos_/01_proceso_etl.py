import pandas as pd
import pyodbc
import os

print(" Iniciando ETL...")

# -----------------------------
# CONEXIÓN A SQL SERVER
# -----------------------------
try:
    conn = pyodbc.connect(
        'DRIVER={ODBC Driver 17 for SQL Server};'
        'SERVER=localhost;'
        'DATABASE=HotelDB;'
        'Trusted_Connection=yes;'
    )
    cursor = conn.cursor()
    print("Conexión exitosa a SQL Server")

except Exception as e:
    print(" Error al conectar:", e)
    exit()


# -----------------------------
# CARGAR DATASET
# -----------------------------
try:
    ruta = os.path.join(os.path.dirname(__file__), 'database', 'hotel_bookings.csv')
    df = pd.read_csv(ruta)

    print(" Dataset cargado correctamente")
    print(" Ruta:", ruta)
    print(" Filas y columnas:", df.shape)
    print(df.head())

except Exception as e:
    print(" Error al cargar CSV:", e)
    exit()

# -----------------------------
# INSERTAR HOTELES
# -----------------------------
try:
    print(" Insertando hoteles...")

    hoteles = df['hotel'].drop_duplicates()

    for h in hoteles:
        cursor.execute("INSERT INTO Hoteles (nombre) VALUES (?)", h)

    conn.commit()

    print(" Hoteles insertados correctamente")

except Exception as e:
    print(" Error al insertar hoteles:", e)

# Crear DataFrame de clientes (usar columnas relevantes y eliminar duplicados)
try:
    clientes = df[[
        'country', 'customer_type', 'is_repeated_guest',
        'previous_cancellations', 'previous_bookings_not_canceled'
    ]].drop_duplicates().reset_index(drop=True)
except Exception as e:
    print(" Error al preparar clientes:", e)
    clientes = pd.DataFrame(columns=[
        'country', 'customer_type', 'is_repeated_guest',
        'previous_cancellations', 'previous_bookings_not_canceled'
    ])

# Insertar clientes
for _, fila in clientes.iterrows():
    try:
        cursor.execute("""
            INSERT INTO Clientes (
                country, customer_type, is_repeated_guest,
                previous_cancellations, previous_bookings_not_canceled
            )
            VALUES (?, ?, ?, ?, ?)
        """,
        fila['country'],
        fila['customer_type'],
        int(float(fila['is_repeated_guest'])) if fila['is_repeated_guest'] not in (None, '') else 0,
        int(float(fila['previous_cancellations'])) if fila['previous_cancellations'] not in (None, '') else 0,
        int(float(fila['previous_bookings_not_canceled'])) if fila['previous_bookings_not_canceled'] not in (None, '') else 0
        )
    except Exception:
        continue

conn.commit()
print(" Clientes insertados correctamente")

# -----------------------------
# CREAR DATAFRAME CANALES
# -----------------------------
canales = df[['market_segment','distribution_channel']].drop_duplicates()

# -----------------------------
# INSERTAR CANALES
# -----------------------------
try:
    print(" Insertando canales...")

    for _, fila in canales.iterrows():
        try:
            cursor.execute("""
                INSERT INTO CanalesReserva (
                    market_segment, distribution_channel
                )
                VALUES (?, ?)
            """,
            fila['market_segment'],
            fila['distribution_channel']
            )
        except:
            continue

    conn.commit()

    print(" Canales insertados correctamente")

except Exception as e:
    print(" Error al insertar canales:", e)

# -----------------------------
# CREAR DATAFRAME HABITACIONES
# -----------------------------
habitaciones = df[['reserved_room_type','assigned_room_type']].drop_duplicates()

# -----------------------------
# INSERTAR HABITACIONES
# -----------------------------
try:
    print(" Insertando habitaciones...")

    for _, fila in habitaciones.iterrows():
        try:
            cursor.execute("""
                INSERT INTO Habitaciones (
                    reserved_room_type, assigned_room_type
                )
                VALUES (?, ?)
            """,
            fila['reserved_room_type'],
            fila['assigned_room_type']
            )
        except:
            continue

    conn.commit()

    print(" Habitaciones insertadas correctamente")

except Exception as e:
    print(" Error al insertar habitaciones:", e)

# -----------------------------
# CREAR DATAFRAME ESTADOS
# -----------------------------
estados = df[['is_canceled']].drop_duplicates()

# -----------------------------
# INSERTAR ESTADOS
# -----------------------------
try:
    print(" Insertando estados...")

    for _, fila in estados.iterrows():
        try:
            cursor.execute("""
                INSERT INTO EstadosReserva (is_canceled)
                VALUES (?)
            """,
            int(fila['is_canceled'])
            )
        except:
            continue

    conn.commit()

    print(" Estados insertados correctamente")

except Exception as e:
    print(" Error al insertar estados:", e)

# -----------------------------
# CREAR DATAFRAME FECHAS
# -----------------------------
fechas = df[['arrival_date_year',
             'arrival_date_month',
             'arrival_date_week_number',
             'arrival_date_day_of_month']].drop_duplicates()

# -----------------------------
# INSERTAR FECHAS
# -----------------------------
try:
    print(" Insertando fechas...")

    for _, fila in fechas.iterrows():
        try:
            cursor.execute("""
                INSERT INTO FechasLlegada (
                    arrival_date_year,
                    arrival_date_month,
                    arrival_date_week_number,
                    arrival_date_day_of_month
                )
                VALUES (?, ?, ?, ?)
            """,
            int(fila['arrival_date_year']),
            fila['arrival_date_month'],
            int(fila['arrival_date_week_number']),
            int(fila['arrival_date_day_of_month'])
            )
        except:
            continue

    conn.commit()

    print(" Fechas insertadas correctamente")

except Exception as e:
    print(" Error al insertar fechas:", e)

cursor.execute("SELECT id_hotel, nombre FROM Hoteles")
map_hoteles = {row.nombre: row.id_hotel for row in cursor.fetchall()}

cursor.execute("SELECT id_cliente, country, customer_type FROM Clientes")
map_clientes = {(row.country, row.customer_type): row.id_cliente for row in cursor.fetchall()}

cursor.execute("SELECT id_canal, market_segment, distribution_channel FROM CanalesReserva")
map_canales = {(row.market_segment, row.distribution_channel): row.id_canal for row in cursor.fetchall()}

cursor.execute("SELECT id_habitacion, reserved_room_type, assigned_room_type FROM Habitaciones")
map_habitaciones = {(row.reserved_room_type, row.assigned_room_type): row.id_habitacion for row in cursor.fetchall()}

cursor.execute("SELECT id_estado, is_canceled FROM EstadosReserva")
map_estados = {row.is_canceled: row.id_estado for row in cursor.fetchall()}

cursor.execute("SELECT id_fecha, arrival_date_year, arrival_date_month, arrival_date_week_number, arrival_date_day_of_month FROM FechasLlegada")
map_fechas = {
    (row.arrival_date_year, row.arrival_date_month, row.arrival_date_week_number, row.arrival_date_day_of_month): row.id_fecha
    for row in cursor.fetchall()
}

print(" Insertando reservas...")

for _, fila in df.iterrows():
    try:
        id_hotel = map_hoteles.get(fila['hotel'])
        id_cliente = map_clientes.get((fila['country'], fila['customer_type']))
        id_canal = map_canales.get((fila['market_segment'], fila['distribution_channel']))
        id_habitacion = map_habitaciones.get((fila['reserved_room_type'], fila['assigned_room_type']))
        id_estado = map_estados.get(int(fila['is_canceled']))
        id_fecha = map_fechas.get((
            fila['arrival_date_year'],
            fila['arrival_date_month'],
            fila['arrival_date_week_number'],
            fila['arrival_date_day_of_month']
        ))

        if None in (id_hotel, id_cliente, id_canal, id_habitacion, id_estado, id_fecha):
            continue

        cursor.execute("""
            INSERT INTO Reservas (
                id_hotel, id_cliente, id_canal, id_habitacion,
                id_estado, id_fecha,
                lead_time, stays_in_weekend_nights, stays_in_week_nights,
                adults, children, babies, adr
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        id_hotel, id_cliente, id_canal, id_habitacion, id_estado, id_fecha,
        int(fila['lead_time']),
        int(fila['stays_in_weekend_nights']),
        int(fila['stays_in_week_nights']),
        int(fila['adults']),
        int(fila['children']) if not pd.isna(fila['children']) else 0,
        int(fila['babies']),
        float(fila['adr'])
        )

    except:
        continue

conn.commit()

print(" Reservas insertadas correctamente")
