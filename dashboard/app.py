import streamlit as st
import pandas as pd
from sqlalchemy import create_engine, text
import os
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="Ofertas CR", layout="wide")
st.title("🛒 Ofertas CR - Comparador de Precios")

@st.cache_resource
def get_connection():
    url = os.getenv("SUPABASE_URL")
    return create_engine(url)

def get_ofertas_recientes():
    engine = get_connection()
    query = text("""
        SELECT 
            p.nombre as producto,
            t.nombre as tienda,
            pr.precio_actual,
            pr.precio_regular,
            pr.porcentaje_descuento,
            pr.fecha_extraccion
        FROM precios pr
        JOIN productos p ON pr.producto_id = p.id
        JOIN tiendas t ON pr.tienda_id = t.id
        WHERE pr.es_oferta = true
        ORDER BY pr.porcentaje_descuento DESC
        LIMIT 20
    """)
    return pd.read_sql(query, engine)

st.sidebar.header("📊 Filtros")
opcion = st.sidebar.radio("Ver:", ["Ofertas del Día", "Todos los Productos"])

if opcion == "Ofertas del Día":
    st.header("🔥 Ofertas del Día")
    df = get_ofertas_recientes()
    if not df.empty:
        st.dataframe(df)
    else:
        st.info("No hay ofertas registradas. ¡Vuelve pronto!")
else:
    st.header("📋 Comparador de Precios")
    st.info("Próximamente: todos los productos")
