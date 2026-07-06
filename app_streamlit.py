from __future__ import annotations

import os
from datetime import datetime
from pathlib import Path
from typing import Any

import pandas as pd
import streamlit as st
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score
from sklearn.model_selection import train_test_split

try:
    import pyodbc
except ImportError:  # pragma: no cover - optional runtime dependency
    pyodbc = None

try:
    from pymongo import MongoClient
except ImportError:  # pragma: no cover - optional runtime dependency
    MongoClient = None


BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "S3. Flujo_de_trabajo_para_ML" / "2. Preprocesamiento y limpieza de datos"
RESULTS_DIR = BASE_DIR / "S3. Flujo_de_trabajo_para_ML" / "4. Modelado Supervisado y Comparacion de modelos" / "0_resultados"
LOCAL_DB_DIR = BASE_DIR / "streamlit_data"
LOCAL_RESERVATIONS_FILE = LOCAL_DB_DIR / "reservas_interfaz.csv"

CLEAN_DATA_FILE = DATA_DIR / "6_dataset_limpio.csv"
TRANSFORMED_DATA_FILE = DATA_DIR / "7_dataset_transformado.csv"
METRICS_FILE = RESULTS_DIR / "3_metricas_modelos_supervisados.csv"

TARGET = "is_canceled"
LEAKAGE_COLUMNS = {"reservation_status", "reservation_status_date"}
FEATURE_COLUMNS = [
    "hotel",
    "lead_time",
    "arrival_date_year",
    "arrival_date_month",
    "arrival_date_week_number",
    "arrival_date_day_of_month",
    "stays_in_weekend_nights",
    "stays_in_week_nights",
    "adults",
    "children",
    "babies",
    "meal",
    "country",
    "market_segment",
    "distribution_channel",
    "is_repeated_guest",
    "previous_cancellations",
    "previous_bookings_not_canceled",
    "reserved_room_type",
    "assigned_room_type",
    "booking_changes",
    "deposit_type",
    "agent",
    "days_in_waiting_list",
    "customer_type",
    "adr",
    "required_car_parking_spaces",
    "total_of_special_requests",
]

CATEGORICAL_COLUMNS = [
    "hotel",
    "arrival_date_month",
    "meal",
    "country",
    "market_segment",
    "distribution_channel",
    "reserved_room_type",
    "assigned_room_type",
    "deposit_type",
    "customer_type",
]

SPANISH_LABELS = {
    "City Hotel": "Hotel urbano",
    "Resort Hotel": "Hotel resort",
    "Transient": "Transitorio",
    "Transient-Party": "Grupo transitorio",
    "Contract": "Contrato",
    "Group": "Grupo",
    "Direct": "Directo",
    "Corporate": "Corporativo",
    "Online TA": "Agencia online",
    "Offline TA/TO": "Agencia offline",
    "Complementary": "Complementario",
    "Groups": "Grupos",
    "Aviation": "Aviacion",
    "No Deposit": "Sin deposito",
    "Non Refund": "No reembolsable",
    "Refundable": "Reembolsable",
    "TA/TO": "Agencia/operador",
    "GDS": "GDS",
    "Undefined": "No definido",
    "SC": "Sin comida",
    "BB": "Desayuno",
    "HB": "Media pension",
    "FB": "Pension completa",
}


def display_value(value: Any) -> str:
    if pd.isna(value):
        return "Sin dato"
    text = str(value)
    return SPANISH_LABELS.get(text, text)


def decode_value(column: str, display_text: str, options: list[Any]) -> Any:
    lookup = {display_value(value): value for value in options}
    return lookup.get(display_text, display_text)


@st.cache_data(show_spinner=False)
def load_project_data() -> tuple[pd.DataFrame, pd.DataFrame]:
    clean_df = pd.read_csv(CLEAN_DATA_FILE)
    transformed_df = pd.read_csv(TRANSFORMED_DATA_FILE)
    clean_df.columns = clean_df.columns.str.strip()
    transformed_df.columns = transformed_df.columns.str.strip()
    return clean_df, transformed_df


@st.cache_data(show_spinner=False)
def build_label_maps(clean_df: pd.DataFrame, transformed_df: pd.DataFrame) -> dict[str, dict[Any, Any]]:
    maps: dict[str, dict[Any, Any]] = {}
    for column in CATEGORICAL_COLUMNS:
        pairs = (
            pd.DataFrame({"raw": clean_df[column], "encoded": transformed_df[column]})
            .drop_duplicates()
            .dropna(subset=["raw"])
        )
        maps[column] = dict(zip(pairs["raw"], pairs["encoded"]))
    return maps


@st.cache_resource(show_spinner="Entrenando modelo Random Forest...")
def train_model(transformed_df: pd.DataFrame) -> tuple[RandomForestClassifier, dict[str, float]]:
    df = transformed_df.copy()
    y = df[TARGET].astype(int)
    x = df[FEATURE_COLUMNS].apply(pd.to_numeric, errors="coerce").fillna(0)

    x_train, x_test, y_train, y_test = train_test_split(
        x,
        y,
        test_size=0.2,
        random_state=42,
        stratify=y,
    )

    model = RandomForestClassifier(
        n_estimators=120,
        max_depth=12,
        class_weight="balanced",
        random_state=42,
        n_jobs=-1,
    )
    model.fit(x_train, y_train)
    y_pred = model.predict(x_test)

    metrics = {
        "accuracy": accuracy_score(y_test, y_pred),
        "precision": precision_score(y_test, y_pred, zero_division=0),
        "recall": recall_score(y_test, y_pred, zero_division=0),
        "f1": f1_score(y_test, y_pred, zero_division=0),
    }
    return model, metrics


def load_sql_view(connection_string: str) -> pd.DataFrame:
    if pyodbc is None:
        raise RuntimeError("pyodbc no esta instalado en el entorno actual.")
    with pyodbc.connect(connection_string, timeout=4) as conn:
        return pd.read_sql("SELECT * FROM dbo.vw_prediccion_cancelacion", conn)


def get_mongo_collection(uri: str, db_name: str, collection_name: str):
    if MongoClient is None:
        raise RuntimeError("pymongo no esta instalado en el entorno actual.")
    client = MongoClient(uri, serverSelectionTimeoutMS=3000)
    client.admin.command("ping")
    return client[db_name][collection_name]


def read_local_reservations() -> pd.DataFrame:
    if LOCAL_RESERVATIONS_FILE.exists():
        return pd.read_csv(LOCAL_RESERVATIONS_FILE)
    return pd.DataFrame()


def append_local_reservation(row: dict[str, Any]) -> None:
    LOCAL_DB_DIR.mkdir(exist_ok=True)
    existing = read_local_reservations()
    new_row = pd.DataFrame([row])
    pd.concat([existing, new_row], ignore_index=True).to_csv(LOCAL_RESERVATIONS_FILE, index=False)


def encode_input(row: dict[str, Any], label_maps: dict[str, dict[Any, Any]]) -> pd.DataFrame:
    encoded = {}
    for column in FEATURE_COLUMNS:
        value = row[column]
        if column in label_maps:
            encoded[column] = label_maps[column].get(value, 0)
        else:
            encoded[column] = value
    return pd.DataFrame([encoded], columns=FEATURE_COLUMNS).apply(pd.to_numeric, errors="coerce").fillna(0)


def section_hint(title: str, description: str) -> None:
    st.markdown(
        f"""
        <div class="section-hint">
            <strong>{title}</strong>
            <span>{description}</span>
        </div>
        """,
        unsafe_allow_html=True,
    )


def field_hint(title: str, description: str) -> None:
    st.markdown(
        f"""
        <div class="field-hint">
            <strong>{title}</strong>
            <span>{description}</span>
        </div>
        """,
        unsafe_allow_html=True,
    )


def option_selector(
    label: str,
    column: str,
    clean_df: pd.DataFrame,
    default: Any | None = None,
    key: str | None = None,
) -> Any:
    options = sorted(clean_df[column].dropna().unique().tolist(), key=lambda item: display_value(item))
    labels = [display_value(option) for option in options]
    default_index = 0
    if default in options:
        default_index = options.index(default)
    selected_label = st.selectbox(label, labels, index=default_index, key=key, label_visibility="collapsed")
    return decode_value(column, selected_label, options)


def build_reservation_form(clean_df: pd.DataFrame, key_prefix: str) -> dict[str, Any]:
    defaults = {
        "hotel": clean_df["hotel"].mode().iloc[0],
        "arrival_date_year": int(clean_df["arrival_date_year"].mode().iloc[0]),
        "arrival_date_month": clean_df["arrival_date_month"].mode().iloc[0],
        "arrival_date_week_number": int(clean_df["arrival_date_week_number"].median()),
        "arrival_date_day_of_month": int(clean_df["arrival_date_day_of_month"].median()),
        "meal": clean_df["meal"].mode().iloc[0],
        "country": clean_df["country"].mode().iloc[0],
        "market_segment": clean_df["market_segment"].mode().iloc[0],
        "distribution_channel": clean_df["distribution_channel"].mode().iloc[0],
        "reserved_room_type": clean_df["reserved_room_type"].mode().iloc[0],
        "assigned_room_type": clean_df["assigned_room_type"].mode().iloc[0],
        "deposit_type": clean_df["deposit_type"].mode().iloc[0],
        "customer_type": clean_df["customer_type"].mode().iloc[0],
    }

    section_hint(
        "Datos de la reserva",
        "Completa las caracteristicas de la reserva para que el modelo calcule el riesgo de cancelacion.",
    )

    left, middle, right = st.columns(3)
    with left:
        field_hint("Hotel", "Tipo de establecimiento donde se realizo la reserva.")
        hotel = option_selector("Hotel", "hotel", clean_df, defaults["hotel"], key=f"{key_prefix}_hotel")
        field_hint("Dias de anticipacion", "Cantidad de dias entre la reserva y la llegada del huesped.")
        lead_time = st.slider("Dias de anticipacion", 0, 365, 60, key=f"{key_prefix}_lead", label_visibility="collapsed")
        field_hint("Anio de llegada", "Anio programado para el ingreso al hotel.")
        arrival_date_year = st.selectbox(
            "Anio de llegada",
            sorted(clean_df["arrival_date_year"].dropna().astype(int).unique().tolist()),
            index=1,
            key=f"{key_prefix}_year",
            label_visibility="collapsed",
        )
        field_hint("Mes de llegada", "Mes en el que inicia la estadia.")
        arrival_date_month = option_selector(
            "Mes de llegada",
            "arrival_date_month",
            clean_df,
            defaults["arrival_date_month"],
            key=f"{key_prefix}_month",
        )
        field_hint("Semana del anio", "Numero de semana del calendario para la llegada.")
        arrival_date_week_number = st.slider(
            "Semana del anio",
            1,
            53,
            defaults["arrival_date_week_number"],
            key=f"{key_prefix}_week",
            label_visibility="collapsed",
        )
        field_hint("Dia del mes", "Dia exacto del mes en que llega el huesped.")
        arrival_date_day_of_month = st.slider(
            "Dia del mes",
            1,
            31,
            defaults["arrival_date_day_of_month"],
            key=f"{key_prefix}_day",
            label_visibility="collapsed",
        )
        field_hint("Tipo de cliente", "Clasificacion comercial del cliente o grupo que reserva.")
        customer_type = option_selector(
            "Tipo de cliente",
            "customer_type",
            clean_df,
            defaults["customer_type"],
            key=f"{key_prefix}_customer_type",
        )

    with middle:
        field_hint("Noches de fin de semana", "Cantidad de noches reservadas entre sabado y domingo.")
        stays_in_weekend_nights = st.slider(
            "Noches de fin de semana",
            0,
            10,
            1,
            key=f"{key_prefix}_weekend",
            label_visibility="collapsed",
        )
        field_hint("Noches entre semana", "Cantidad de noches reservadas de lunes a viernes.")
        stays_in_week_nights = st.slider(
            "Noches entre semana",
            0,
            30,
            2,
            key=f"{key_prefix}_weeknights",
            label_visibility="collapsed",
        )
        field_hint("Adultos", "Numero de adultos incluidos en la reserva.")
        adults = st.number_input("Adultos", 0, 10, 2, key=f"{key_prefix}_adults", label_visibility="collapsed")
        field_hint("Ninos", "Numero de ninos incluidos en la reserva.")
        children = st.number_input("Ninos", 0, 10, 0, key=f"{key_prefix}_children", label_visibility="collapsed")
        field_hint("Bebes", "Numero de bebes incluidos en la reserva.")
        babies = st.number_input("Bebes", 0, 5, 0, key=f"{key_prefix}_babies", label_visibility="collapsed")
        field_hint("Tipo de comida", "Plan de alimentacion contratado para la estadia.")
        meal = option_selector("Tipo de comida", "meal", clean_df, defaults["meal"], key=f"{key_prefix}_meal")
        field_hint("Pais", "Pais de origen del huesped principal.")
        country = option_selector("Pais", "country", clean_df, defaults["country"], key=f"{key_prefix}_country")

    with right:
        field_hint("Segmento de mercado", "Origen comercial de la reserva, por ejemplo agencia online u offline.")
        market_segment = option_selector(
            "Segmento de mercado",
            "market_segment",
            clean_df,
            defaults["market_segment"],
            key=f"{key_prefix}_market_segment",
        )
        field_hint("Canal de distribucion", "Medio usado para concretar la reserva.")
        distribution_channel = option_selector(
            "Canal de distribucion",
            "distribution_channel",
            clean_df,
            defaults["distribution_channel"],
            key=f"{key_prefix}_distribution",
        )
        field_hint("Habitacion reservada", "Tipo de habitacion solicitado inicialmente.")
        reserved_room_type = option_selector(
            "Habitacion reservada",
            "reserved_room_type",
            clean_df,
            defaults["reserved_room_type"],
            key=f"{key_prefix}_reserved_room",
        )
        field_hint("Habitacion asignada", "Tipo de habitacion finalmente asignado por el hotel.")
        assigned_room_type = option_selector(
            "Habitacion asignada",
            "assigned_room_type",
            clean_df,
            defaults["assigned_room_type"],
            key=f"{key_prefix}_assigned_room",
        )
        field_hint("Deposito", "Condicion del pago previo o reembolso de la reserva.")
        deposit_type = option_selector(
            "Deposito",
            "deposit_type",
            clean_df,
            defaults["deposit_type"],
            key=f"{key_prefix}_deposit",
        )
        field_hint("Tarifa diaria promedio", "Precio promedio por noche de la reserva.")
        adr = st.number_input(
            "Tarifa diaria promedio",
            -100.0,
            10000.0,
            90.0,
            step=5.0,
            key=f"{key_prefix}_adr",
            label_visibility="collapsed",
        )
        field_hint("Parqueaderos requeridos", "Cantidad de espacios de estacionamiento solicitados.")
        required_car_parking_spaces = st.number_input(
            "Parqueaderos requeridos",
            0,
            8,
            0,
            key=f"{key_prefix}_parking",
            label_visibility="collapsed",
        )

    section_hint(
        "Historial y cambios",
        "Estos datos ayudan a estimar el comportamiento del cliente antes de la fecha de llegada.",
    )
    extra_left, extra_right = st.columns(2)
    with extra_left:
        field_hint("Cliente repetido", "Activalo si el huesped ya ha reservado antes en el hotel.")
        is_repeated_guest = st.toggle("Cliente repetido", value=False, key=f"{key_prefix}_repeated", label_visibility="collapsed")
        field_hint("Cancelaciones previas", "Numero de reservas anteriores canceladas por el cliente.")
        previous_cancellations = st.number_input(
            "Cancelaciones previas",
            0,
            30,
            0,
            key=f"{key_prefix}_prev_cancel",
            label_visibility="collapsed",
        )
        field_hint("Reservas previas no canceladas", "Reservas historicas que el cliente completo correctamente.")
        previous_bookings_not_canceled = st.number_input(
            "Reservas previas no canceladas",
            0,
            100,
            0,
            key=f"{key_prefix}_prev_not_cancel",
            label_visibility="collapsed",
        )
    with extra_right:
        field_hint("Cambios en la reserva", "Cantidad de modificaciones realizadas antes de la llegada.")
        booking_changes = st.number_input(
            "Cambios en la reserva",
            0,
            30,
            0,
            key=f"{key_prefix}_changes",
            label_visibility="collapsed",
        )
        field_hint("Dias en lista de espera", "Tiempo que la reserva permanecio esperando confirmacion.")
        days_in_waiting_list = st.number_input(
            "Dias en lista de espera",
            0,
            400,
            0,
            key=f"{key_prefix}_waiting",
            label_visibility="collapsed",
        )
        field_hint("Solicitudes especiales", "Numero de requerimientos adicionales del huesped.")
        total_of_special_requests = st.number_input(
            "Solicitudes especiales",
            0,
            10,
            0,
            key=f"{key_prefix}_requests",
            label_visibility="collapsed",
        )
        field_hint("Codigo de agente", "Identificador del agente o intermediario de la reserva.")
        agent = st.number_input(
            "Codigo de agente",
            0.0,
            600.0,
            0.0,
            step=1.0,
            key=f"{key_prefix}_agent",
            label_visibility="collapsed",
        )

    return {
        "hotel": hotel,
        "lead_time": int(lead_time),
        "arrival_date_year": int(arrival_date_year),
        "arrival_date_month": arrival_date_month,
        "arrival_date_week_number": int(arrival_date_week_number),
        "arrival_date_day_of_month": int(arrival_date_day_of_month),
        "stays_in_weekend_nights": int(stays_in_weekend_nights),
        "stays_in_week_nights": int(stays_in_week_nights),
        "adults": int(adults),
        "children": float(children),
        "babies": int(babies),
        "meal": meal,
        "country": country,
        "market_segment": market_segment,
        "distribution_channel": distribution_channel,
        "is_repeated_guest": int(is_repeated_guest),
        "previous_cancellations": int(previous_cancellations),
        "previous_bookings_not_canceled": int(previous_bookings_not_canceled),
        "reserved_room_type": reserved_room_type,
        "assigned_room_type": assigned_room_type,
        "booking_changes": int(booking_changes),
        "deposit_type": deposit_type,
        "agent": float(agent),
        "days_in_waiting_list": int(days_in_waiting_list),
        "customer_type": customer_type,
        "adr": float(adr),
        "required_car_parking_spaces": int(required_car_parking_spaces),
        "total_of_special_requests": int(total_of_special_requests),
    }


def render_metric_cards(metrics: dict[str, float]) -> None:
    cols = st.columns(4)
    labels = [("Accuracy", "accuracy"), ("Precision", "precision"), ("Recall", "recall"), ("F1-score", "f1")]
    for col, (label, key) in zip(cols, labels):
        col.metric(label, f"{metrics[key]:.3f}")


def render_sidebar() -> dict[str, str]:
    st.sidebar.image(str(BASE_DIR / "Unach.png"), use_container_width=True)
    st.sidebar.header("Conexiones")

    default_sql = os.getenv(
        "HOTEL_SQL_CONNECTION",
        "DRIVER={ODBC Driver 17 for SQL Server};SERVER=localhost\\SQLEXPRESS;DATABASE=HotelDB;Trusted_Connection=yes;",
    )
    sql_connection = st.sidebar.text_input("SQL Server", value=default_sql, type="password")

    mongo_uri = st.sidebar.text_input("MongoDB URI", value=os.getenv("MONGO_URI", "mongodb://localhost:27017/"), type="password")
    mongo_db = st.sidebar.text_input("Base MongoDB", value=os.getenv("MONGO_DB", "hotel_booking_ml"))
    mongo_collection = st.sidebar.text_input("Coleccion", value=os.getenv("MONGO_COLLECTION", "predicciones_streamlit"))

    return {
        "sql_connection": sql_connection,
        "mongo_uri": mongo_uri,
        "mongo_db": mongo_db,
        "mongo_collection": mongo_collection,
    }


def main() -> None:
    st.set_page_config(
        page_title="Hotel Booking Demand ML",
        page_icon="HB",
        layout="wide",
    )

    st.markdown(
        """
        <style>
        .stApp {
            background:
                linear-gradient(135deg, rgba(6, 11, 20, 0.84), rgba(19, 34, 48, 0.70)),
                url("https://images.unsplash.com/photo-1566073771259-6a8506099945?auto=format&fit=crop&w=2200&q=80");
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        }
        .block-container {
            max-width: 1480px;
            padding-top: 1.5rem;
            padding-bottom: 2rem;
            background: rgba(9, 14, 24, 0.78);
            border: 1px solid rgba(255, 255, 255, 0.16);
            border-radius: 8px;
            box-shadow: 0 24px 70px rgba(0, 0, 0, 0.38);
            backdrop-filter: blur(5px);
        }
        h1, h2, h3, .stMarkdown, .stCaption, label, p, span {
            color: #f8fafc;
        }
        div[data-testid="stTabs"] button p {
            color: #f8fafc;
            font-weight: 700;
        }
        div[data-testid="stTabs"] button[aria-selected="true"] p {
            color: #ff4b4b;
        }
        section[data-testid="stSidebar"] {
            background: rgba(7, 12, 22, 0.92);
        }
        section[data-testid="stSidebar"] label,
        section[data-testid="stSidebar"] p,
        section[data-testid="stSidebar"] span {
            color: #f8fafc;
        }
        div[data-testid="stMetric"] {
            background: rgba(255, 255, 255, 0.94);
            border: 1px solid rgba(255, 255, 255, 0.34);
            padding: 14px 16px;
            border-radius: 8px;
        }
        div[data-testid="stMetric"] label,
        div[data-testid="stMetric"] p,
        div[data-testid="stMetric"] span {
            color: #111827;
        }
        .section-hint {
            margin: 18px 0 12px;
            padding: 12px 14px;
            border-left: 4px solid #ff4b4b;
            border-radius: 8px;
            background: rgba(255, 255, 255, 0.12);
        }
        .section-hint strong {
            display: block;
            color: #ffffff;
            font-size: 1rem;
        }
        .section-hint span {
            display: block;
            margin-top: 3px;
            color: #d9e2ef;
            font-size: 0.91rem;
        }
        .field-hint {
            margin: 10px 0 5px;
            line-height: 1.18;
        }
        .field-hint strong {
            display: block;
            color: #ffffff;
            font-size: 0.92rem;
        }
        .field-hint span {
            display: block;
            color: #cbd5e1;
            font-size: 0.78rem;
        }
        div[data-testid="stAlert"] p,
        div[data-testid="stAlert"] span {
            color: inherit;
        }
        div[data-testid="stDataFrame"],
        div[data-testid="stTable"] {
            background: rgba(255, 255, 255, 0.96);
            border-radius: 8px;
        }
        .stSelectbox div[data-baseweb="select"] > div,
        .stNumberInput input,
        .stTextInput input {
            background: #20232d;
            color: #ffffff;
            border-color: rgba(255, 255, 255, 0.18);
        }
        div[data-testid="stSlider"] span {
            color: #f8fafc;
        }
        button[kind="primary"] {
            font-weight: 700;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    settings = render_sidebar()
    clean_df, transformed_df = load_project_data()
    label_maps = build_label_maps(clean_df, transformed_df)
    model, metrics = train_model(transformed_df)

    st.title("Hotel Booking Demand")
    st.caption("Prediccion de cancelaciones, consulta de reservas y persistencia hibrida")
    render_metric_cards(metrics)

    tab_predict, tab_data, tab_new, tab_analysis, tab_db = st.tabs(
        ["Prediccion", "Reservas", "Nueva reserva", "Analitica", "Base de datos"]
    )

    with tab_predict:
        st.subheader("Prediccion de cancelacion")
        section_hint(
            "Objetivo de esta pantalla",
            "Ingresa una reserva simulada y el modelo estima si podria cancelarse antes de su llegada.",
        )
        input_row = build_reservation_form(clean_df, "predict")
        encoded_input = encode_input(input_row, label_maps)
        probability = float(model.predict_proba(encoded_input)[0][1])
        prediction = int(probability >= 0.5)

        result_left, result_right = st.columns([1, 2])
        with result_left:
            st.metric("Probabilidad de cancelacion", f"{probability:.1%}")
            if prediction:
                st.error("Riesgo alto de cancelacion")
            else:
                st.success("Riesgo bajo de cancelacion")
        with result_right:
            importance = pd.DataFrame(
                {
                    "variable": FEATURE_COLUMNS,
                    "importancia": model.feature_importances_,
                }
            ).sort_values("importancia", ascending=False).head(10)
            st.bar_chart(importance, x="variable", y="importancia")

        field_hint("Guardar prediccion", "Registra esta simulacion en el archivo local y en MongoDB si la conexion esta activa.")
        if st.button("Guardar prediccion", type="primary"):
            document = {
                "fecha_registro": datetime.now().isoformat(timespec="seconds"),
                "origen": "streamlit",
                "probabilidad_cancelacion": probability,
                "prediccion_cancelacion": prediction,
                **input_row,
            }
            append_local_reservation(document)
            try:
                collection = get_mongo_collection(
                    settings["mongo_uri"],
                    settings["mongo_db"],
                    settings["mongo_collection"],
                )
                collection.insert_one(document)
                st.success("Prediccion guardada en CSV local y MongoDB.")
            except Exception as exc:
                st.warning(f"Prediccion guardada en CSV local. MongoDB no disponible: {exc}")

    with tab_data:
        st.subheader("Reservas registradas")
        section_hint(
            "Consulta de reservas",
            "Elige una fuente de datos para revisar registros existentes, cancelaciones y resumenes rapidos.",
        )
        source = st.radio("Fuente", ["Dataset del proyecto", "Registros de la interfaz", "SQL Server"], horizontal=True)

        if source == "Dataset del proyecto":
            data = clean_df.copy()
        elif source == "Registros de la interfaz":
            data = read_local_reservations()
        else:
            try:
                data = load_sql_view(settings["sql_connection"])
                st.success("Datos cargados desde vw_prediccion_cancelacion.")
            except Exception as exc:
                data = pd.DataFrame()
                st.error(f"No se pudo conectar a SQL Server: {exc}")

        if not data.empty:
            hotel_filter = st.multiselect("Filtrar hotel", sorted(data["hotel"].dropna().unique()) if "hotel" in data else [])
            status_filter = st.selectbox("Estado", ["Todas", "Canceladas", "No canceladas"])
            filtered = data.copy()
            if hotel_filter and "hotel" in filtered:
                filtered = filtered[filtered["hotel"].isin(hotel_filter)]
            if status_filter != "Todas" and TARGET in filtered:
                filtered = filtered[filtered[TARGET].astype(int).eq(1 if status_filter == "Canceladas" else 0)]

            top_cols = st.columns(4)
            top_cols[0].metric("Registros", f"{len(filtered):,}")
            if TARGET in filtered:
                top_cols[1].metric("Canceladas", f"{int(filtered[TARGET].astype(int).sum()):,}")
                top_cols[2].metric("No canceladas", f"{int((1 - filtered[TARGET].astype(int)).sum()):,}")
                top_cols[3].metric("Tasa cancelacion", f"{filtered[TARGET].astype(int).mean():.1%}")
            st.dataframe(filtered.head(1000), use_container_width=True, hide_index=True)
        else:
            st.info("No hay registros disponibles en esta fuente.")

    with tab_new:
        st.subheader("Registro de nueva reserva")
        section_hint(
            "Crear una reserva",
            "Llena los datos reales o simulados de una reserva y guardalos para mostrarlos durante la exposicion.",
        )
        new_row = build_reservation_form(clean_df, "new")
        encoded_new = encode_input(new_row, label_maps)
        new_probability = float(model.predict_proba(encoded_new)[0][1])
        new_prediction = int(new_probability >= 0.5)

        st.metric("Prediccion antes de guardar", f"{new_probability:.1%}")
        field_hint("Estado real de la reserva", "Si todavia no se conoce el resultado final, deja la opcion Pendiente.")
        is_canceled = st.selectbox(
            "Estado real de la reserva",
            ["Pendiente", "No cancelada", "Cancelada"],
            label_visibility="collapsed",
        )

        field_hint("Registrar reserva", "Guarda esta reserva en el archivo local usado por la interfaz.")
        if st.button("Registrar reserva", type="primary"):
            record = {
                "fecha_registro": datetime.now().isoformat(timespec="seconds"),
                "origen": "streamlit",
                "probabilidad_cancelacion": new_probability,
                "prediccion_cancelacion": new_prediction,
                **new_row,
            }
            if is_canceled != "Pendiente":
                record[TARGET] = 1 if is_canceled == "Cancelada" else 0
            append_local_reservation(record)
            st.success("Reserva registrada en streamlit_data/reservas_interfaz.csv.")

    with tab_analysis:
        st.subheader("Analitica hotelera")
        section_hint(
            "Lectura de resultados",
            "Estas graficas resumen el comportamiento historico de cancelaciones por hotel, mes y segmento.",
        )
        col_a, col_b = st.columns(2)
        with col_a:
            cancel_rate = (
                clean_df.groupby("hotel")[TARGET]
                .mean()
                .reset_index()
                .rename(columns={TARGET: "tasa_cancelacion"})
            )
            st.bar_chart(cancel_rate, x="hotel", y="tasa_cancelacion")
        with col_b:
            segment = (
                clean_df.groupby("market_segment")[TARGET]
                .agg(["count", "mean"])
                .reset_index()
                .rename(columns={"count": "reservas", "mean": "tasa_cancelacion"})
                .sort_values("reservas", ascending=False)
            )
            st.dataframe(segment, use_container_width=True, hide_index=True)

        chart_left, chart_right = st.columns(2)
        with chart_left:
            monthly = (
                clean_df.groupby("arrival_date_month")[TARGET]
                .mean()
                .reindex(
                    [
                        "January",
                        "February",
                        "March",
                        "April",
                        "May",
                        "June",
                        "July",
                        "August",
                        "September",
                        "October",
                        "November",
                        "December",
                    ]
                )
                .dropna()
                .reset_index()
                .rename(columns={TARGET: "tasa_cancelacion"})
            )
            st.line_chart(monthly, x="arrival_date_month", y="tasa_cancelacion")
        with chart_right:
            st.scatter_chart(clean_df.sample(min(len(clean_df), 3000), random_state=42), x="lead_time", y="adr", color=TARGET)

        if METRICS_FILE.exists():
            st.subheader("Metricas del proyecto")
            st.dataframe(pd.read_csv(METRICS_FILE), use_container_width=True, hide_index=True)

    with tab_db:
        st.subheader("Estado de conexiones")
        section_hint(
            "Pruebas de persistencia hibrida",
            "Usa estos botones para comprobar si SQL Server y MongoDB estan disponibles desde esta interfaz.",
        )
        db_left, db_right = st.columns(2)
        with db_left:
            field_hint("Probar SQL Server", "Verifica la conexion con la vista dbo.vw_prediccion_cancelacion.")
            if st.button("Probar SQL Server"):
                try:
                    preview = load_sql_view(settings["sql_connection"]).head(5)
                    st.success("Conexion SQL Server correcta.")
                    st.dataframe(preview, use_container_width=True, hide_index=True)
                except Exception as exc:
                    st.error(f"SQL Server no disponible: {exc}")
        with db_right:
            field_hint("Probar MongoDB", "Verifica la conexion con la coleccion donde se guardan predicciones.")
            if st.button("Probar MongoDB"):
                try:
                    collection = get_mongo_collection(
                        settings["mongo_uri"],
                        settings["mongo_db"],
                        settings["mongo_collection"],
                    )
                    count = collection.count_documents({})
                    st.success(f"MongoDB conectado. Documentos: {count}")
                except Exception as exc:
                    st.error(f"MongoDB no disponible: {exc}")

        local_data = read_local_reservations()
        st.subheader("Persistencia local")
        st.write(f"Archivo: `{LOCAL_RESERVATIONS_FILE.relative_to(BASE_DIR)}`")
        st.metric("Registros locales", len(local_data))
        if not local_data.empty:
            st.dataframe(local_data.tail(25), use_container_width=True, hide_index=True)


if __name__ == "__main__":
    main()
