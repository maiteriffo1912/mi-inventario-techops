import streamlit as st
import pandas as pd
from io import BytesIO

st.set_page_config(page_title="Reporte Tech Ops - Listado Completo", layout="wide")

st.title("📊 Reporte Maestro: Inventario y Auditoría Tech Ops")
st.markdown("---")

# --- GUÍA DE COLORES ---
st.subheader("📘 Guía de Colores de Inventario")
c1, c2, c3, c4, c5 = st.columns(5)
c1.markdown("<div style='background-color: #f8bbd0; padding: 10px; border-radius: 5px; color: black; text-align: center;'><b>ROSADO</b><br>Coincide / OK</div>", unsafe_allow_html=True)
c2.markdown("<div style='background-color: #80cbc4; padding: 10px; border-radius: 5px; color: black; text-align: center;'><b>VERDE AZULADO</b><br>Repetido / Mejorar</div>", unsafe_allow_html=True)
c3.markdown("<div style='background-color: #c8e6c9; padding: 10px; border-radius: 5px; color: black; text-align: center;'><b>VERDE</b><br>No Coincide</div>", unsafe_allow_html=True)
c4.markdown("<div style='background-color: #ffe0b2; padding: 10px; border-radius: 5px; color: black; text-align: center;'><b>NARANJO</b><br>Sin Código</div>", unsafe_allow_html=True)
c5.markdown("<div style='background-color: #bbdefb; padding: 10px; border-radius: 5px; color: black; text-align: center;'><b>AZUL</b><br>De Baja</div>", unsafe_allow_html=True)

# --- 1. PROCESAMIENTO LISTADO GENERAL COMPLETO ---
# Datos extraídos del archivo "litado general"
data_general = [
    ["Agitador Magnetico (16 posiciones)", "EQ-CB-023", "COINCIDE (ROSADO)"],
    ["Balanza (max 100kg)", "EQ-CB-217", "COINCIDE (ROSADO)"],
    ["Balanza de (Max 30 kg / min: 1 g)", "EQ-CB-175", "COINCIDE (ROSADO)"],
    ["Horno de secado", "EQ-CB-066", "COINCIDE (ROSADO)"],
    ["Balanza (Max: 30Kg / Min: 40g)", "EQ-CB-196", "COINCIDE (ROSADO)"],
    ["Balanza (Max: 30Kg / Min: 40g)", "EQ-CB-197", "COINCIDE (ROSADO)"],
    ["Campana de extracción Quimica", "EQ-CB-092", "COINCIDE (ROSADO)"],
    ["Balanza Analitica (120g)", "EQ-CB-021", "DE BAJA (AZUL)"],
    ["Medidor NO", "EQ-LIX-010", "CÓDIGO NO COINCIDE (VERDE)"],
    ["Balanza Digital (Max 30Kg)", "EQ-CB-124", "DE BAJA (AZUL)"],
    ["Anemometro", "EQ-CB-198", "CÓDIGO REPETIDO (VERDE AZULADO)"],
    ["Multiparametro pH/ORP/ISE", "EQ-CB-057", "CÓDIGO REPETIDO (VERDE AZULADO)"],
    ["Multiparametro portatil", "SIN CODIGO", "SIN CÓDIGO (NARANJO)"],
    ["Alzador electrico", "SIN CODIGO", "SIN CÓDIGO (NARANJO)"],
    ["Celular", "EQ-CB-228", "COINCIDE (ROSADO)"],
    ["Celular", "EQ-CB-229", "COINCIDE (ROSADO)"],
    ["Equipo Medición de gases", "EQ-CB-239", "COINCIDE (ROSADO)"]
]
df_gen = pd.DataFrame(data_general, columns=["Instrumento", "Código", "Estado Auditado"])

# --- 2. PROCESAMIENTO HOJA 1 (REPETIDOS Y CONFLICTOS) ---
# Datos extraídos del archivo "Hoja1"
data_hoja1 = [
    ["Anemometro", "EQ-CB-198", "CÓDIGO REPETIDO", "Conflicto con Balanza"],
    ["Balanza digital", "EQ-CB-198", "NO ESTÁ EN INVENTARIO", "Conflicto con Anemómetro"],
    ["Plancha calefactora", "EQ-CB-223", "CÓDIGO REPETIDO", "Conflicto con Balanza 60Kg"],
    ["Balanza 60Kg", "EQ-CB-223", "NO ESTÁ EN INVENTARIO", "Conflicto con Plancha"],
    ["ERA (Autónomo)", "EQ-CB-218", "CÓDIGO REPETIDO", "Conflicto con Campana"],
    ["Campana de extracción", "EQ-CB-218", "NO ESTÁ EN INVENTARIO", "Conflicto con ERA"],
    ["Multiparametro pH-ISE", "EQ-CB-220", "NO PERTENECE", "No pertenece a Tech Ops"],
    ["Medidor NO2", "EQ-CB-220", "CÓDIGO REPETIDO", "Conflicto con Multiparámetro"],
    ["Baño Ultrasonico", "EQ-CB-057", "NO PERTENECE", "No pertenece a Tech Ops"],
    ["Carro rojo", "EQ-CB-215", "CÓDIGO REPETIDO", "Conflicto con Multiparámetro"],
    ["Bomba de vacio", "EQ-CB-205", "CÓDIGO REPETIDO", "Conflicto con Balanza Analítica"]
]
df_h1 = pd.DataFrame(data_hoja1, columns=["Instrumento", "Código", "Tipo de Conflicto", "Detalle Mejora"])

# --- VISUALIZACIÓN ---

st.header("1. Listado General (Todos los Equipos)")
def style_gen(row):
    color_map = {
        'COINCIDE (ROSADO)': 'background-color: #f8bbd0',
        'DE BAJA (AZUL)': 'background-color: #bbdefb',
        'CÓDIGO NO COINCIDE (VERDE)': 'background-color: #c8e6c9',
        'CÓDIGO REPETIDO (VERDE AZULADO)': 'background-color: #80cbc4',
        'SIN CÓDIGO (NARANJO)': 'background-color: #ffe0b2'
    }
    return [color_map.get(row['Estado Auditado'], '')] * len(row)

st.dataframe(df_gen.style.apply(style_gen, axis=1), use_container_width=True)

st.header("2. Detalle de Conflictos (Hoja 1 - Verde Azulado)")
st.info("Estos instrumentos presentan duplicidad de código o inconsistencias de pertenencia que deben corregirse.")
st.dataframe(df_h1.style.applymap(lambda x: 'background-color: #80cbc4; color: black'), use_container_width=True)

# --- BOTÓN DE DESCARGA ---
output = BytesIO()
with pd.ExcelWriter(output, engine='openpyxl') as writer:
    df_gen.to_excel(writer, sheet_name='Inventario_General', index=False)
    df_h1.to_excel(writer, sheet_name='Mejoras_Conflictos', index=False)

st.markdown("---")
st.download_button(
    label="📥 Descargar Reporte Completo (.xlsx)",
    data=output.getvalue(),
    file_name="Auditoria_TechOps_Completa.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)

