import streamlit as st
import pandas as pd
from io import BytesIO

st.set_page_config(page_title="Reporte Integral Tech Ops", layout="wide")

st.title("📋 Reporte Maestro de Gestión: Inventario, Conflictos y Mantención")
st.markdown("---")

# --- GUÍA DE COLORES ---
st.subheader("💡 Guía de Referencia Visual")
c1, c2, c3, c4, c5 = st.columns(5)
c1.markdown("<div style='background-color: #f8bbd0; padding: 10px; border-radius: 5px; color: black; text-align: center;'><b>ROSADO</b><br>Coincide / OK</div>", unsafe_allow_html=True)
c2.markdown("<div style='background-color: #80cbc4; padding: 10px; border-radius: 5px; color: black; text-align: center;'><b>VERDE AZULADO</b><br>Repetido / Mantención</div>", unsafe_allow_html=True)
c3.markdown("<div style='background-color: #c8e6c9; padding: 10px; border-radius: 5px; color: black; text-align: center;'><b>VERDE</b><br>No Coincide</div>", unsafe_allow_html=True)
c4.markdown("<div style='background-color: #ffe0b2; padding: 10px; border-radius: 5px; color: black; text-align: center;'><b>NARANJO</b><br>Sin Código</div>", unsafe_allow_html=True)
c5.markdown("<div style='background-color: #bbdefb; padding: 10px; border-radius: 5px; color: black; text-align: center;'><b>AZUL</b><br>De Baja</div>", unsafe_allow_html=True)

# --- SECCIÓN 1: LISTADO GENERAL COMPLETO ---
st.header("1. Listado General de Inventario (Completo)")
data_gen = [
    ["Agitador Magnetico (16 posiciones)", "EQ-CB-023", "COINCIDE (ROSADO)"],
    ["Balanza (max 100kg)", "EQ-CB-217", "COINCIDE (ROSADO)"],
    ["Balanza de (Max 30 kg / min: 1 g)", "EQ-CB-175", "COINCIDE (ROSADO)"],
    ["Horno de secado", "EQ-CB-066", "COINCIDE (ROSADO)"],
    ["Balanza (Max: 30Kg / Min: 40g)", "EQ-CB-196", "COINCIDE (ROSADO)"],
    ["Balanza (Max: 30Kg / Min: 40g)", "EQ-CB-197", "COINCIDE (ROSADO)"],
    ["Campana de extracción Quimica", "EQ-CB-092", "COINCIDE (ROSADO)"],
    ["Multiparametro pH/ORP/ISE Meter", "EQ-CB-105", "COINCIDE (ROSADO)"],
    ["Agitador Magnetico 10 posiciones", "EQ-CB-111", "COINCIDE (ROSADO)"],
    ["Agitador Magnetico Pequeño", "EQ-CB-112", "COINCIDE (ROSADO)"],
    ["Balanza Analitica (120g)", "EQ-CB-021", "DE BAJA (AZUL)"],
    ["Agitador Magnetico Pequeño", "EQ-CB-122", "COINCIDE (ROSADO)"],
    ["Balanza Digital (Max 30Kg)", "EQ-CB-124", "DE BAJA (AZUL)"],
    ["Anemometro", "EQ-CB-198", "CÓDIGO REPETIDO (VERDE AZULADO)"],
    ["Celular", "EQ-CB-228", "COINCIDE (ROSADO)"],
    ["Celular", "EQ-CB-229", "COINCIDE (ROSADO)"],
    ["Equipo Medición de gases", "EQ-CB-239", "COINCIDE (ROSADO)"]
]
df_gen = pd.DataFrame(data_gen, columns=["Instrumento", "Código", "Estado"])

def style_gen(row):
    color_map = {'COINCIDE (ROSADO)': 'background-color: #f8bbd0', 'DE BAJA (AZUL)': 'background-color: #bbdefb', 
                 'CÓDIGO REPETIDO (VERDE AZULADO)': 'background-color: #80cbc4', 'CÓDIGO NO COINCIDE (VERDE)': 'background-color: #c8e6c9'}
    return [color_map.get(row['Estado'], '')] * len(row)

st.dataframe(df_gen.style.apply(style_gen, axis=1), use_container_width=True)

# --- SECCIÓN 2: HOJA 1 - INSTRUMENTOS DUPLICADOS Y MEJORAS ---
st.header("2. Reporte de Mejoras: Conflictos y Duplicados (Hoja 1)")
st.info("Listado independiente de discrepancias de códigos y pertenencia de equipos.")
data_h1 = [
    ["Anemometro", "EQ-CB-198", "Repetido con Balanza digital"],
    ["Balanza digital (30kg)", "EQ-CB-198", "No está en inventario"],
    ["Plancha calefactora", "EQ-CB-223", "Repetido con Balanza 60Kg"],
    ["Balanza 60Kg (min: 100g)", "EQ-CB-223", "No está en inventario"],
    ["Equipo de Respiración Autónomo", "EQ-CB-218", "Repetido con Campana"],
    ["Campana de extracción Quimica", "EQ-CB-218", "No está en inventario"],
    ["Multiparametro pH - ISE -EC", "EQ-CB-220", "No pertenece a Tech Ops"],
    ["Medidor NO2", "EQ-CB-220", "Conflicto con Multiparámetro"],
    ["Baño Ultrasonico", "EQ-CB-057", "No pertenece a Tech Ops"],
    ["Multiparametro pH/ORP/ISE", "EQ-CB-057", "Repetido con Baño"],
    ["Multiparametro Portatil", "EQ-CB-215", "Código inexistente"],
    ["Carro rojo", "EQ-CB-215", "Repetido con Multiparámetro"],
    ["Balanza analitica", "EQ-CB-205", "Lab Analítico"],
    ["Bomba de vacio", "EQ-CB-205", "Repetido con Balanza"]
]
df_h1 = pd.DataFrame(data_h1, columns=["Instrumento", "Código", "Detalle de Mejora"])
st.dataframe(df_h1.style.applymap(lambda x: 'background-color: #80cbc4; color: black'), use_container_width=True)

# --- SECCIÓN 3: HOJA 2 - PLAN DE MANTENCIÓN ACTUAL ---
st.header("3. Plan de Mantención Inmediata (Hoja 2)")
st.markdown("Equipos con mantención programada o vencida. Color Verde Azulado.")
data_maint = [
    ["Agitador Magnetico (16 posiciones)", "EQ-CB-023", "2026-02-25", "PROGRAMADA"],
    ["Horno de secado", "EQ-CB-066", "2026-02-25", "PROGRAMADA"],
    ["Medidor NO", "EQ-LIX-010", "2026-02-01", "VENCIDA"],
    ["Campana de extracción", "EQ-CB-092", "2025-08-07", "VENCIDA"],
    ["Hidrolavadora GHP200", "EQ-CB-258", "SIN FECHA", "URGENTE"],
    ["Anemometro", "EQ-CB-198", "SIN FECHA", "URGENTE"]
]
df_maint = pd.DataFrame(data_maint, columns=["Equipo", "Código", "Fecha Mantención", "Estatus"])
st.dataframe(df_maint.style.applymap(lambda x: 'background-color: #80cbc4; color: black'), use_container_width=True)

# --- DESCARGA ---
output = BytesIO()
with pd.ExcelWriter(output, engine='openpyxl') as writer:
    df_gen.to_excel(writer, sheet_name='Listado_General', index=False)
    df_h1.to_excel(writer, sheet_name='Hoja1_Mejoras', index=False)
    df_maint.to_excel(writer, sheet_name='Hoja2_Mantencion', index=False)

st.download_button(label="📥 Descargar Reporte Completo (.xlsx)", data=output.getvalue(), 
                   file_name="Auditoria_TechOps_Final.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
