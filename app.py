import streamlit as st
from datetime import date
from generar_pptx import generar_pptx

st.set_page_config(page_title="Generador Arrimaq", page_icon="A", layout="wide")

CATALOGO = {
    "RRE120B":{"cap":1200,"cc":600,"ext":5432,"plg":2182,"bat":"48V/310Ah"},
    "RRE160H2":{"cap":1400,"cc":600,"ext":7540,"plg":2887,"bat":"48V/465Ah"},
    "RRE160HN":{"cap":1400,"cc":600,"ext":7540,"plg":2887,"bat":"48V/310Ah"},
    "RRE160HR2":{"cap":1600,"cc":600,"ext":7610,"plg":2957,"bat":"48V/620Ah"},
    "SPE120XR":{"cap":1200,"cc":600,"ext":5920,"plg":2259,"bat":"24V/300Ah"},
    "SPE120":{"cap":1200,"cc":600,"ext":4657,"plg":2020,"bat":"24V/300Ah"},
    "SPE140S":{"cap":1400,"cc":600,"ext":4668,"plg":1955,"bat":"24V/300Ah"},
    "SWE120XR":{"cap":1200,"cc":600,"ext":5920,"plg":2459,"bat":"24V/300Ah"},
    "SWE140S":{"cap":1400,"cc":600,"ext":4668,"plg":1955,"bat":"24V/300Ah"},
    "SWE145":{"cap":1450,"cc":600,"ext":4668,"plg":1955,"bat":"24V/300Ah"},
    "8FBE20T":{"cap":1500,"cc":500,"ext":3870,"plg":2120,"bat":"48V/440Ah"},
    "8FBM20T":{"cap":1600,"cc":500,"ext":3870,"plg":2120,"bat":"48V/550Ah"},
    "9FBM25T":{"cap":2000,"cc":500,"ext":3979,"plg":2235,"bat":"80V/500Ah"},
    "9FBM30T":{"cap":2000,"cc":500,"ext":3979,"plg":2235,"bat":"80V/500Ah"},
    "LPE200":{"cap":2000,"cc":600,"ext":None,"plg":None,"bat":"24V/300Ah"},
    "LWE140":{"cap":1400,"cc":600,"ext":None,"plg":None,"bat":"24V/150Ah"},
    "OSE100":{"cap":1000,"cc":600,"ext":2570,"plg":1550,"bat":"24V/465Ah"},
    "VRE150":{"cap":1500,"cc":600,"ext":7095,"plg":3135,"bat":"48V/620Ah"},
}

FAMILIAS = {
    "Reach electrico (RRE)":["RRE120B","RRE160H2","RRE160HN","RRE160HR2"],
    "Apilador electrico (SPE/SWE)":["SPE120","SPE120XR","SPE140S","SWE120XR","SWE140S","SWE145"],
    "Contrabalanceado (8FBE/8FBM/9FBM)":["8FBE20T","8FBM20T","9FBM25T","9FBM30T"],
    "Transpaleta electrica (LPE/LWE)":["LPE200","LWE140"],
    "Order Picker (OSE)":["OSE100"],
    "Very Narrow Aisle (VRE)":["VRE150"],
}

st.title("Generador de Propuestas - Arrimaq SPA")
st.markdown("---")

col1, col2 = st.columns([3,2], gap="large")

with col1:
    st.subheader("1. Datos del ejecutivo")
    c1,c2 = st.columns(2)
    ejecutivo = c1.text_input("Nombre", placeholder="Gonzalo Araya Wohllk")
    email_ejec = c2.text_input("Email", placeholder="garaya@arrimaq.com")
    c3,c4 = st.columns(2)
    banco = c3.selectbox("Banco", ["BCI - Cta. Cte. 10669817", "Banco Consorcio - Cta. Cte. 4210003189"])
    fecha = c4.date_input("Fecha", value=date.today())

    st.subheader("2. Datos del cliente")
    c1,c2 = st.columns(2)
    empresa = c1.text_input("Empresa", placeholder="Nombre empresa")
    contacto = c2.text_input("Contacto", placeholder="Nombre contacto")
    ref = st.text_input("Referencia", placeholder="Ej: Cotizacion equipos BT")

    st.subheader("3. Tipo de operacion")
    tipo = st.radio("", ["Venta","Arriendo","Venta + Arriendo"], horizontal=True, label_visibility="collapsed")
    tipo_key = {"Venta":"venta","Arriendo":"arriendo","Venta + Arriendo":"ambos"}[tipo]

    st.subheader("4. Equipo")
    c1,c2 = st.columns(2)
    familia = c1.selectbox("Familia", ["- Seleccionar -"]+list(FAMILIAS.keys()))
    mods = FAMILIAS.get(familia,[]) if familia != "- Seleccionar -" else []
    mod_opts = ["- Seleccionar -"]+[f"{m} ({CATALOGO[m]['cap']}kg)" if m in CATALOGO else m for m in mods]
    mod_sel = c2.selectbox("Modelo", mod_opts)
    modelo = mod_sel.split(" ")[0] if mod_sel != "- Seleccionar -" else ""

    specs_auto = CATALOGO.get(modelo,{}) if modelo else {}
    if specs_auto:
        st.success(f"Specs: {specs_auto.get('cap','')}kg | Mastil: {specs_auto.get('ext','')}mm | Bat: {specs_auto.get('bat','')}")

    c1,c2,c3 = st.columns(3)
    nombre_eq = c1.text_input("Nombre equipo", value=modelo)
    estado = c2.selectbox("Estado", ["Nuevo","Reacondicionado","Usado"])
    cantidad = c3.number_input("Cantidad", min_value=1, value=1)

    st.markdown("**Especificaciones**")
    c1,c2 = st.columns(2)
    marca = c1.text_input("Marca", value="BT")
    procedencia = c2.text_input("Procedencia", value="Suecia")
    c1,c2 = st.columns(2)
    cap = c1.text_input("Capacidad (kg)", value=str(specs_auto.get("cap","")) if specs_auto else "")
    cc = c2.text_input("Centro carga (mm)", value=str(specs_auto.get("cc","")) if specs_auto else "")
    c1,c2 = st.columns(2)
    ext = c1.text_input("Mastil extendido (mm)", value=str(specs_auto.get("ext","")) if specs_auto and specs_auto.get("ext") else "")
    plg = c2.text_input("Mastil plegado (mm)", value=str(specs_auto.get("plg","")) if specs_auto and specs_auto.get("plg") else "")
    c1,c2 = st.columns(2)
    bat = c1.text_input("Bateria", value=specs_auto.get("bat","") if spe
