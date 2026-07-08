from __future__ import annotations

import os
from datetime import datetime, date
from pathlib import Path
from typing import Any

import pandas as pd
import streamlit as st
import streamlit.components.v1 as components
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

USUARIOS_VALIDOS = {
    "admin": {"password": "admin123", "rol": "Administrador"},
    "usuario": {"password": "usuario123", "rol": "Usuario común"},
}

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
    "No Deposit": "Pago al llegar al hotel",
    "Refundable": "Pago parcial por adelantado",
    "Non Refund": "Pago completo por adelantado",
    "TA/TO": "Agencia/operador",
    "GDS": "GDS",
    "Undefined": "No definido",
    "SC": "Sin alimentación",
    "BB": "Desayuno incluido",
    "HB": "Desayuno + Cena",
    "FB": "Buffet completo (Desayuno, Almuerzo y Cena)",
    "A": "Estándar (A)",
    "B": "Ejecutiva (B)",
    "C": "Deluxe (C)",
    "D": "Junior Suite (D)",
    "E": "Premium Suite (E)",
    "F": "Familiar (F)",
    "G": "Presidencial (G)",
    "H": "Habitación Superior (H)",
    "L": "Suite Ejecutiva (L)",
    "P": "Suite Premium Plus (P)",
    "PAG": "Habitación Especial (PAG)",
    "I": "Suite Imperial (I)",
    "K": "Suite King (K)",
    "PRT": "Portugal",
    "ESP": "España",
    "GBR": "Reino Unido",
    "USA": "Estados Unidos",
    "FRA": "Francia",
    "DEU": "Alemania",
    "ITA": "Italia",
    "IRL": "Irlanda",
    "BRA": "Brasil",
    "ECU": "Ecuador",
    "ABW": "Aruba",
    "AIA": "Anguila",
    "ALB": "Albania",
    "AND": "Andorra",
    "ARE": "Emiratos Árabes Unidos",
    "ARG": "Argentina",
    "ASM": "Samoa Americana",
    "LUX": "Luxemburgo",
    "LVA": "Letonia",
    "MAC": "Macao",
    "MAR": "Marruecos",
    "MCO": "Mónaco",
    "MDV": "Maldivas",
    "MEX": "México",
    "MKD": "Macedonia del Norte",
    "MLI": "Malí",
    "MLT": "Malta",
    "MMR": "Myanmar",
    "MNE": "Montenegro",
    "MOZ": "Mozambique",
    "MRT": "Mauritania",
    "MWI": "Malaui",
    "MYS": "Malasia",
    "MYT": "Mayotte",
    "NAM": "Namibia",
    "NCL": "Nueva Caledonia",
    "NGA": "Nigeria",
    "NIC": "Nicaragua",
    "NLD": "Países Bajos",
    "NPL": "Nepal",
    "NZL": "Nueva Zelanda",
    "OMN": "Omán",
    "PAK": "Pakistán",
    "PER": "Perú",
    "PHL": "Filipinas",
    "POL": "Polonia",
    "PRI": "Puerto Rico",
    "QAT": "Catar",
    "RUS": "Rusia",
    "RWA": "Ruanda",
    "SAU": "Arabia Saudita",
    "SGP": "Singapur",
    "SVK": "Eslovaquia",
    "SVN": "Eslovenia",
    "SWE": "Suecia",
    "THA": "Tailandia",
    "TUR": "Turquía",
    "TZA": "Tanzania",
    "UGA": "Uganda",
    "URY": "Uruguay",
    "USA": "Estados Unidos",
    "UZB": "Uzbekistán",
    "VEN": "Venezuela",
    "VNM": "Vietnam",
    "ZAF": "Sudáfrica",
    "ZMB": "Zambia",
    "ZWE": "Zimbabue",
    "AGO": "Angola",
    "ARM": "Armenia",
    "AUT": "Austria",
    "BEL": "Bélgica",
    "BGR": "Bulgaria",
    "BHR": "Baréin",
    "BLR": "Bielorrusia",
    "CAN": "Canadá",
    "CHE": "Suiza",
    "CHL": "Chile",
    "CHN": "China",
    "CIV": "Costa de Marfil",
    "CMR": "Camerún",
    "COL": "Colombia",
    "CPV": "Cabo Verde",
    "CRI": "Costa Rica",
    "CUB": "Cuba",
    "CYP": "Chipre",
    "CZE": "República Checa",
    "DNK": "Dinamarca",
    "DZA": "Argelia",
    "EGY": "Egipto",
    "FIN": "Finlandia",
    "GRC": "Grecia",
    "HKG": "Hong Kong",
    "HRV": "Croacia",
    "HUN": "Hungría",
    "IDN": "Indonesia",
    "ISR": "Israel",
    "JPN": "Japón",
    "KOR": "Corea del Sur",
    "KWT": "Kuwait",
    "LTU": "Lituania",
    "MUS": "Mauricio",
    "NOR": "Noruega",
    "PAN": "Panamá",
    "ROU": "Rumanía",
    "SDN": "Sudán",
    "SEN": "Senegal",
    "SLE": "Sierra Leona",
    "SLV": "El Salvador",
    "SMR": "San Marino",
    "SRB": "Serbia",
    "STP": "Santo Tomé y Príncipe",
    "SUR": "Surinam",
    "SYC": "Seychelles",
    "SYR": "Siria",
    "TGO": "Togo",
    "TJK": "Tayikistán",
    "TUN": "Túnez",
    "UKR": "Ucrania",
    "UMI": "Islas Ultramarinas Menores de EE. UU.",
    "VGB": "Islas Vírgenes Británicas",
    "PLW": "Palau",
    "PYF": "Polinesia Francesa",
    "TMP": "Timor-Leste"
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


def init_session_state() -> None:
    if "autenticado" not in st.session_state:
        st.session_state["autenticado"] = False
        st.session_state["rol"] = "Invitado"
        st.session_state["login_attempted"] = False
        st.session_state["input_usuario"] = ""
        st.session_state["input_contrasena"] = ""


def render_login_page() -> None:
    st.title("Acceso al sistema")
    st.write("Inicie sesión para continuar")

    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        st.subheader("Inicio de sesión")

        with st.form("login_form", clear_on_submit=False):
            usuario = st.text_input(
                "Usuario",
                value=st.session_state.get("input_usuario", ""),
                key="input_usuario"
            )

            contrasena = st.text_input(
                "Contraseña",
                type="password",
                key="input_contrasena"
            )

            submitted = st.form_submit_button("Iniciar sesión")

            if submitted:
                st.session_state["login_attempted"] = True

                usuario = usuario.strip()
                contrasena = contrasena.strip()

                if usuario in USUARIOS_VALIDOS and contrasena == USUARIOS_VALIDOS[usuario]["password"]:
                    st.session_state["autenticado"] = True
                    st.session_state["rol"] = USUARIOS_VALIDOS[usuario]["rol"]
                    st.rerun()
                else:
                    st.session_state["autenticado"] = False
                    st.session_state["rol"] = "Invitado"
                    st.error("Usuario o contraseña inválidos.")

        if not st.session_state.get("login_attempted"):
            st.info("Usuario de prueba: usuario / usuario123")
            st.info("Administrador: admin / admin123")


def option_selector(
    label: str,
    column: str,
    clean_df: pd.DataFrame,
    default: Any | None = None,
    key: str | None = None,
) -> Any:
    options = sorted(clean_df[column].dropna().unique().tolist(), key=lambda item: display_value(item))

    if column == "country":
        labels = [
            SPANISH_LABELS.get(str(option), f"País/territorio ({option})")
            for option in options
        ]
    else:
        labels = [display_value(option) for option in options]

    default_index = 0
    if default in options:
        default_index = options.index(default)

    selected_label = st.selectbox(
        label,
        labels,
        index=default_index,
        key=key,
        label_visibility="collapsed"
    )

    if column == "country":
        lookup = {
            SPANISH_LABELS.get(str(value), f"País/territorio ({value})"): value
            for value in options
        }
        return lookup.get(selected_label, selected_label)

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
        "Completa las características de la reserva para que el modelo calcule el riesgo de cancelación.",
    )

    left, middle, right = st.columns(3, gap="large")
    with left:
        field_hint("Hotel", "Tipo de establecimiento donde se realizó la reserva.")
        hotel = option_selector("Hotel", "hotel", clean_df, defaults["hotel"], key=f"{key_prefix}_hotel")
        field_hint(
            "Fecha de llegada",
            "Seleccione la fecha programada para el ingreso al hotel."
        )
        fecha_llegada = st.date_input(
            "Fecha de llegada",
            value=date.today(),
            format="DD/MM/YYYY",
            key=f"{key_prefix}_fecha_llegada",
            label_visibility="collapsed"
        )
        st.caption(
            fecha_llegada.strftime("%d de %B de %Y")
        )
        arrival_date_year = fecha_llegada.year
        arrival_date_month = fecha_llegada.strftime("%B")
        arrival_date_day_of_month = fecha_llegada.day
        arrival_date_week_number = fecha_llegada.isocalendar().week

        field_hint("Días de anticipación", "Cantidad de días entre la reserva y la llegada del huésped.")
        lead_time = st.slider("Dias de anticipación", 0, 365, 60, key=f"{key_prefix}_lead", label_visibility="collapsed")

        field_hint("Tipo de cliente", "Clasificación comercial del cliente o grupo que reserva.")
        customer_type = option_selector(
            "Tipo de cliente",
            "customer_type",
            clean_df,
            defaults["customer_type"],
            key=f"{key_prefix}_customer_type",
        )

    with middle:
        field_hint(
            "Selección de noches",
            "Elige el tipo de estadía y la cantidad de noches reservadas."
        )
        tipo_noches = st.selectbox(
            "Selección de noches",
            ["Entre semana", "Fin de semana", "Mixta"],
            key=f"{key_prefix}_tipo_noches",
            label_visibility="collapsed"
        )
        if tipo_noches == "Entre semana":
            stays_in_weekend_nights = 0
            stays_in_week_nights = st.slider(
                "Cantidad de noches entre semana",
                0,
                30,
                2,
                key=f"{key_prefix}_weeknights",
                label_visibility="collapsed",
            )
        elif tipo_noches == "Fin de semana":
            stays_in_weekend_nights = st.slider(
                "Cantidad de noches de fin de semana",
                0,
                10,
                1,
                key=f"{key_prefix}_weekend",
                label_visibility="collapsed",
            )
            stays_in_week_nights = 0
        else:
            col_weekend, col_weekdays = st.columns(2, gap="medium")
            with col_weekend:
                field_hint(
                    "Fin de semana",
                    "Noches reservadas entre sábado y domingo."
                )
                stays_in_weekend_nights = st.slider(
                    "Noches de fin de semana",
                    0,
                    10,
                    1,
                    key=f"{key_prefix}_weekend",
                    label_visibility="collapsed",
                )
            with col_weekdays:
                field_hint(
                    "Entre semana",
                    "Noches reservadas de lunes a viernes."
                )
                stays_in_week_nights = st.slider(
                    "Noches entre semana",
                    0,
                    30,
                    2,
                    key=f"{key_prefix}_weeknights",
                    label_visibility="collapsed",
                )

        total_noches = stays_in_weekend_nights + stays_in_week_nights
        st.caption(f"Total de noches seleccionadas: {total_noches}")

        field_hint("Adultos", "Número de adultos incluidos en la reserva.")
        adults = st.number_input(
            "Adultos",
            0,
            10,
            2,
            key=f"{key_prefix}_adults",
            label_visibility="collapsed"
        )
        field_hint(
            "Menores (1 a 15 años)",
            "Cantidad total de niños y bebés incluidos en la reserva."
        )
        menores_1_15 = st.number_input(
            "Menores (1 a 15 años)",
            0,
            15,
            0,
            key=f"{key_prefix}_menores", 
            label_visibility="collapsed"
        )
        field_hint("Tipo de comida", "Plan de alimentación contratado para la estadía.")
        meal = option_selector("Tipo de comida", "meal", clean_df, defaults["meal"], key=f"{key_prefix}_meal")
        field_hint("País", "País de origen del huésped principal.")
        country = option_selector("Pais", "country", clean_df, defaults["country"], key=f"{key_prefix}_country")

    with right:
        field_hint(
            "Origen de la reserva",
            "Seleccione el segmento comercial y el canal utilizado para concretar la reserva."
        )

        market_col, channel_col = st.columns([5, 5])

        with market_col:
            st.caption("Segmento de mercado")
            market_segment = option_selector(
                "Segmento de mercado",
                "market_segment",
                clean_df,
                defaults["market_segment"],
                key=f"{key_prefix}_market_segment",
            )

        with channel_col:
            st.caption("Canal de distribución")
            distribution_channel = option_selector(
                "Canal de distribución",
                "distribution_channel",
                clean_df,
                defaults["distribution_channel"],
                key=f"{key_prefix}_distribution",
            )
        
        field_hint("Habitación reservada", "Tipo de habitación solicitado inicialmente.")
        reserved_room_type = option_selector(
            "Habitacion reservada",
            "reserved_room_type",
            clean_df,
            defaults["reserved_room_type"],
            key=f"{key_prefix}_reserved_room",
        )
        room_relations = {
            "A": ["A", "B"],
            "B": ["B", "C"],
            "C": ["C", "D"],
            "D": ["D", "E"],
            "E": ["E", "F"],
            "F": ["F", "G"],
            "G": ["G"],
            "H": ["H", "G"],
            "I": ["I", "G"],
            "K": ["K", "G"],
            "L": ["L", "G"],
            "P": ["P", "G"],
            "PAG": ["PAG", "G"],
        }
        
        field_hint("Habitación asignada", "Tipo de habitación finalmente asignado por el hotel.")
        available_rooms = room_relations.get(
            reserved_room_type,
            [reserved_room_type]
        )
        room_labels = [
            display_value(room)
            for room in available_rooms
        ]
        selected_room = st.selectbox(
            "Habitación asignada",
            room_labels,
            key=f"{key_prefix}_assigned_room",
            label_visibility="collapsed",
        )
        assigned_room_type = decode_value(
            "assigned_room_type",
            selected_room,
            available_rooms,
        )

        field_hint("Depósito", "Condición del pago previo o reembolso de la reserva.")
        deposit_type = option_selector(
            "Depósito",
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
    extra_left, extra_right = st.columns(2, gap="large")
    with extra_left:
        field_hint("Cliente repetido", "Actívalo si el huésped ya ha reservado antes en el hotel.")
        is_repeated_guest = st.toggle("Cliente repetido", value=False, key=f"{key_prefix}_repeated", label_visibility="collapsed")
        field_hint("Cancelaciones previas", "Número de reservas anteriores canceladas por el cliente.")
        previous_cancellations = st.number_input(
            "Cancelaciones previas",
            0,
            30,
            0,
            key=f"{key_prefix}_prev_cancel",
            label_visibility="collapsed",
        )
        field_hint("Reservas previas no canceladas", "Reservas históricas que el cliente completó correctamente.")
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
        field_hint("Días en lista de espera", "Tiempo que la reserva permaneció esperando confirmación.")
        days_in_waiting_list = st.number_input(
            "Dias en lista de espera",
            0,
            400,
            0,
            key=f"{key_prefix}_waiting",
            label_visibility="collapsed",
        )
        field_hint("Solicitudes especiales", "Número de requerimientos adicionales del huésped.")
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
        "children": float(menores_1_15),
        "babies": 0,
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
    st.sidebar.header("Sesión")

    if st.session_state.get("autenticado"):
        st.sidebar.success(f"Sesión iniciada como: {st.session_state.get('rol')}")
        if st.sidebar.button("🔄 Cambiar sesión"):
            st.session_state["autenticado"] = False
            st.session_state["rol"] = "Invitado"
            st.session_state["login_attempted"] = False
            st.session_state["input_usuario"] = ""
            st.session_state["input_contrasena"] = ""
            st.rerun()
    else:
        st.sidebar.info("Inicie sesión en el formulario central para continuar.")

    default_sql = os.getenv(
        "HOTEL_SQL_CONNECTION",
        "DRIVER={ODBC Driver 17 for SQL Server};SERVER=localhost\\SQLEXPRESS;DATABASE=HotelDB;Trusted_Connection=yes;",
    )

    sql_connection = default_sql
    mongo_uri = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
    mongo_db = os.getenv("MONGO_DB", "hotel_booking_ml")
    mongo_collection = os.getenv("MONGO_COLLECTION", "predicciones_streamlit")

    if st.session_state.get("autenticado") and st.session_state.get("rol") == "Administrador":
        st.sidebar.divider()
        st.sidebar.subheader("Configuración técnica")

        mostrar_config = st.sidebar.toggle(
            "Mostrar conexiones",
            value=False
        )

        if mostrar_config:
            sql_connection = st.sidebar.text_input(
                "Servidor SQL",
                value=default_sql,
                type="password"
            )

            mongo_uri = st.sidebar.text_input(
                "URI de MongoDB",
                value=mongo_uri,
                type="password"
            )

            mongo_db = st.sidebar.text_input(
                "Base de datos MongoDB",
                value=mongo_db
            )

            mongo_collection = st.sidebar.text_input(
                "Colección",
                value=mongo_collection
            )

    return {
        "sql_connection": sql_connection,
        "mongo_uri": mongo_uri,
        "mongo_db": mongo_db,
        "mongo_collection": mongo_collection,
        "usuario": st.session_state.get("input_usuario", ""),
        "rol": st.session_state.get("rol", "Invitado"),
        "autenticado": st.session_state.get("autenticado", False),
    }

## Icono ##
def render_spline_badge() -> None:
    components.html(
        """
        <script type="module" src="https://unpkg.com/@splinetool/viewer@1.12.98/build/spline-viewer.js"></script>

        <style>
            body {
                margin: 0;
                background: transparent;
                overflow: hidden;
            }

            .badge-outer {
                width: 155px;
                height: 155px;
                overflow: hidden;
                border-radius: 18px;
                background: rgba(8, 13, 22, 0.15);
                position: relative;
                margin-top: 25px;
            }

            .badge-inner {
                width: 600px;
                height: 600px;
                position: absolute;
                top: 70%;
                left: 55%;
                transform: translate(-50%, -50%) scale(0.35);
                transform-origin: center center;
            }

            spline-viewer {
                width: 600px;
                height: 600px;
            }
        </style>

        <div class="badge-outer">
            <div class="badge-inner">
                <spline-viewer url="https://prod.spline.design/BTaahd3vFOCdv5B0/scene.splinecode"></spline-viewer>
            </div>
        </div>
        """,
        height=185,
        width=165,
    )


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
            background: rgba(22, 33, 48, 0.72);
            border: 1px solid rgba(255, 255, 255, 0.22);
            border-radius: 8px;
            box-shadow: 0 24px 70px rgba(0, 0, 0, 0.28);
            backdrop-filter: blur(4px);
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
            background: linear-gradient(135deg, rgba(15, 23, 42, 0.96), rgba(30, 64, 105, 0.90));
        border: 1px solid rgba(96, 165, 250, 0.55);
            padding: 14px 16px;
            border-radius: 10px;
            box-shadow: 0 10px 28px rgba(0, 0, 0, 0.35);
        }
        div[data-testid="stMetric"] label {
            color: #93c5fd!important;
            font-weight: 700 !important;
        }
        div[data-testid="stMetric"] p,
        div[data-testid="stMetric"] span {
            color: #ffffff !important;
        }
        div[data-testid="stMetricValue"] {
            color: #ffffff !important;
            font-weight: 800 !important;
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
            margin: 16px 0 6px;
            line-height: 1.25;
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

    init_session_state()
    settings = render_sidebar()
    if not settings["autenticado"]:
        render_login_page()
        st.stop()

    clean_df, transformed_df = load_project_data()

    label_maps = build_label_maps(clean_df, transformed_df)
    model, metrics = train_model(transformed_df)

## Cambio de titulo ##
    
    header_left, header_right = st.columns([5, 1])

    with header_left:
        st.title("Gigachad Suites")
        st.caption("Predicción de cancelaciones, consulta de reservas y persistencia híbrida")


## Icono 3D ##    
    with header_right:
        render_spline_badge()


    render_metric_cards(metrics)

    if settings["rol"] == "Administrador":
        tab_predict, tab_data, tab_analysis, tab_db = st.tabs(
            ["Predicción", "Reservas", "Analítica", "Base de datos"]
        )
    else:
        tab_predict, tab_data, tab_analysis = st.tabs(
            ["Predicción", "Reservas", "Analítica"]
        )
        tab_db = None

    with tab_predict:
        st.subheader("Predicción de cancelación")
        section_hint(
            "Objetivo de esta pantalla",
            "Ingresa una reserva simulada y el modelo estima si podría cancelarse antes de su llegada.",
        )
        input_row = build_reservation_form(clean_df, "predict")
        encoded_input = encode_input(input_row, label_maps)
        probability = float(model.predict_proba(encoded_input)[0][1])
        prediction = int(probability >= 0.5)

        result_left, result_right = st.columns([1, 2])
        with result_left:
            st.metric("Probabilidad de cancelación", f"{probability:.1%}")
            if prediction:
                st.error("Riesgo alto de cancelación")
            else:
                st.success("Riesgo bajo de cancelación")
        with result_right:
            importance = pd.DataFrame(
                {
                    "variable": FEATURE_COLUMNS,
                    "importancia": model.feature_importances_,
                }
            ).sort_values("importancia", ascending=False).head(10)
            st.bar_chart(importance, x="variable", y="importancia")

        section_hint(
            "Acciones de la reserva",
            "Puedes guardar la predicción o registrar esta información como una nueva reserva."
        )

        accion_prediccion, accion_reserva = st.columns(2, gap="large")

        with accion_prediccion:
            field_hint(
                "Guardar predicción",
                "Registra esta simulación en el archivo local y en MongoDB si la conexión está activa."
            )

            if st.button("Guardar predicción", type="primary", key="btn_guardar_prediccion"):
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
                    st.success("Predicción guardada en CSV local y MongoDB.")
                except Exception as exc:
                    st.warning(f"Predicción guardada en CSV local. MongoDB no disponible: {exc}")


        with accion_reserva:
            field_hint(
                "Nueva reserva",
                "Activa esta opción si deseas registrar esta simulación como una reserva."
            )

            mostrar_registro = st.toggle(
                "Realizar nueva reserva",
                value=False,
                key="toggle_nueva_reserva"
            )

        if mostrar_registro:
            section_hint(
                "Registro de nueva reserva",
                "Confirma el estado real de la reserva antes de guardarla."
            )

            field_hint(
                "Estado real de la reserva",
                "Si todavía no se conoce el resultado final, deja la opción Pendiente."
            )

            estado_reserva = st.selectbox(
                "Estado real de la reserva",
                ["Pendiente", "No cancelada", "Cancelada"],
                key="estado_real_reserva",
                label_visibility="collapsed"
            )

            if st.button("Registrar nueva reserva", type="primary", key="btn_registrar_nueva_reserva"):
                record = {
                    "fecha_registro": datetime.now().isoformat(timespec="seconds"),
                    "origen": "streamlit",
                    "probabilidad_cancelacion": probability,
                    "prediccion_cancelacion": prediction,
                    **input_row,
                }

                if estado_reserva != "Pendiente":
                    record[TARGET] = 1 if estado_reserva == "Cancelada" else 0

                append_local_reservation(record)
                st.success("Nueva reserva registrada correctamente en streamlit_data/reservas_interfaz.csv.")

    with tab_data:
        st.subheader("Reservas registradas")
        section_hint(
            "Consulta de reservas",
            "Elige una fuente de datos para revisar registros existentes, cancelaciones y resumenes rapidos.",
        )
        if settings["rol"] == "Administrador":
            fuentes_disponibles = ["Dataset del proyecto", "Registros de la interfaz", "SQL Server"]
        else:
            fuentes_disponibles = ["Dataset del proyecto", "Registros de la interfaz"]

        source = st.radio(
            "Fuente",
            fuentes_disponibles,
            horizontal=True
        )

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

    if tab_db is not None:
        with tab_db:
            st.subheader("Estado de conexiones")

            section_hint(
                "Pruebas de persistencia híbrida",
                "Usa estos botones para comprobar si SQL Server y MongoDB están disponibles desde esta interfaz.",
            )

            db_left, db_right = st.columns(2)

            with db_left:
                field_hint(
                    "Probar SQL Server",
                    "Verifica la conexión con la vista dbo.vw_prediccion_cancelacion."
                )

                if st.button("Probar SQL Server"):
                    try:
                        preview = load_sql_view(settings["sql_connection"]).head(5)
                        st.success("Conexión SQL Server correcta.")
                        st.dataframe(preview, use_container_width=True, hide_index=True)
                    except Exception as exc:
                        st.error(f"SQL Server no disponible: {exc}")

            with db_right:
                field_hint(
                    "Probar MongoDB",
                    "Verifica la conexión con la colección donde se guardan predicciones."
                )

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

            # =========================================================
            # Datasets del proyecto, solo visible para el administrador
            # =========================================================

            st.subheader("Datasets del proyecto")

            section_hint(
                "Gestión de datasets",
                "Esta sección permite revisar los archivos utilizados en el flujo de Machine Learning."
            )

            datasets_admin = {
                "Dataset limpio": CLEAN_DATA_FILE,
                "Dataset transformado": TRANSFORMED_DATA_FILE,
                "Métricas del modelo": METRICS_FILE,
            }

            dataset_seleccionado = st.selectbox(
                "Seleccione un dataset",
                list(datasets_admin.keys())
            )

            ruta_dataset = datasets_admin[dataset_seleccionado]

            if ruta_dataset.exists():
                df_admin = pd.read_csv(ruta_dataset)

                col1, col2, col3 = st.columns(3)

                col1.metric("Registros", f"{df_admin.shape[0]:,}")
                col2.metric("Columnas", f"{df_admin.shape[1]:,}")
                col3.metric("Valores nulos", f"{int(df_admin.isnull().sum().sum()):,}")

                st.dataframe(
                    df_admin.head(100),
                    use_container_width=True,
                    hide_index=True
                )

                # Distribución de la variable objetivo, si existe en el dataset seleccionado
                if TARGET in df_admin.columns:
                    st.subheader("Distribución de la variable objetivo")

                    distribucion_objetivo = (
                        df_admin[TARGET]
                        .value_counts()
                        .reset_index()
                    )

                    distribucion_objetivo.columns = ["Clase", "Cantidad"]

                    st.dataframe(
                        distribucion_objetivo,
                        use_container_width=True,
                        hide_index=True
                    )

                    st.bar_chart(
                        distribucion_objetivo,
                        x="Clase",
                        y="Cantidad"
                    )

            else:
                st.warning(f"No se encontró el archivo: {ruta_dataset}")

            # =========================================================
            # Persistencia local
            # =========================================================

            st.subheader("Persistencia local")

            local_data = read_local_reservations()

            st.write(f"Archivo: `{LOCAL_RESERVATIONS_FILE.relative_to(BASE_DIR)}`")
            st.metric("Registros locales", len(local_data))

            if not local_data.empty:
                st.dataframe(
                    local_data.tail(25),
                    use_container_width=True,
                    hide_index=True
                )

if __name__ == "__main__":
    main()
    

