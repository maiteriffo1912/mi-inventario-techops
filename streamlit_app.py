import streamlit as st
import pandas as pd
from io import BytesIO

st.set_page_config(page_title="Auditoría Tech Ops - Reporte Maestro", layout="wide")

st.title("📋 Reporte Maestro de Inventario y Gestión Tech Ops")

# --- GUÍA DE COLORES PARA JEFATURA ---
st.subheader("💡 Guía de Colores de Auditoría")
c1, c2, c3, c4, c5 = st.columns(5)
c1.markdown("<div style='background-color: #f8bbd0; padding: 10px; border-radius: 5px; color: black; text-align: center;'><b>ROSADO</b><br>Coincide / OK</div>", unsafe_allow_html=True)
c2.markdown("<div style='background-color: #80cbc4; padding: 10px; border-radius: 5px; color: black; text-align: center;'><b>VERDE AZULADO</b><br>Repetido / Mantención</div>", unsafe_allow_html=True)
c3.markdown("<div style='background-color: #c8e6c9; padding: 10px; border-radius: 5px; color: black; text-align: center;'><b>VERDE</b><br>No Coincide</div>", unsafe_allow_html=True)
c4.markdown("<div style='background-color: #ffe0b2; padding: 10px; border-radius: 5px; color: black; text-align: center;'><b>NARANJO</b><br>Sin Código</div>", unsafe_allow_html=True)
c5.markdown("<div style='background-color: #bbdefb; padding: 10px; border-radius: 5px; color: black; text-align: center;'><b>AZUL</b><br>De Baja</div>", unsafe_allow_html=True)

# --- PROCESAMIENTO DE DATOS ---

# 1. LISTADO GENERAL (Basado en tu archivo "litado general")
listado_data = [
    ["Agitador Magnetico (16 posiciones)", "EQ-CB-023", "COINCIDE (ROSADO)"],
    ["Balanza (max 100kg)", "EQ-CB-217", "COINCIDE (ROSADO)"],
    ["Horno de secado", "EQ-CB-066", "COINCIDE (ROSADO)"],
    ["Balanza Analitica (120g)", "EQ-CB-021", "DE BAJA (AZUL)"],
    ["Medidor NO", "EQ-LIX-010", "CÓDIGO NO COINCIDE (VERDE)"],
    ["Balanza digital (30kg)", "EQ-CB-242", "COINCIDE (ROSADO)"],
    ["Multiparametro portatil", "EQ-CB-222", "COINCIDE (ROSADO)"],
    ["Balanza 60Kg", "EQ-CB-224", "COINCIDE (ROSADO)"],
    ["Celular", "EQ-CB-228", "COINCIDE (ROSADO)"],
    ["Celular", "EQ-CB-229", "COINCIDE (ROSADO)"],
    ["Equipo Medición de gases", "EQ-CB-239", "COINCIDE (ROSADO)"]
]
df_general = pd.DataFrame(listado_data, columns=["Equipo", "Código", "Estado Auditado"])

# 2. SECCIÓN REPETIDOS (Basado en Hoja 1 y Hoja 2)
repetidos_data = [
    ["Anemometro", "EQ-CB-198", "CÓDIGO REPETIDO (VERDE AZULADO)", "Aparece duplicado en Hoja 1"],
    ["Balanza digital (30kg)", "EQ-CB-198", "CÓDIGO REPETIDO (VERDE AZULADO)", "No está dentro del inventario"],
    ["Plancha calefactora", "EQ-CB-223", "CÓDIGO REPETIDO (VERDE AZULADO)", "Duplicidad de código"],
    ["Balanza 60Kg", "EQ-CB-223", "CÓDIGO REPETIDO (VERDE AZULADO)", "Conflicto de registro"],
    ["Anemómetro", "EQ-CB-254", "CÓDIGO REPETIDO (VERDE AZULADO)", "Repetido en sistema"],
    ["Anemómetro", "EQ-CB-255", "CÓDIGO REPETIDO (VERDE AZULADO)", "Repetido en sistema"]
]
df_mejorar = pd.DataFrame(repetidos_data, columns=["Equipo", "Código", "Estado", "Motivo Mejora"])

# 3. PLAN DE MANTENCIÓN (Basado en Hoja 2 - Verde Azulado)
mantencion_data = [
    ["Agitador Magnetico", "EQ-CB-023", "2026-02-25", "EJECUTAR"],
    ["Horno de secado", "EQ-CB-066", "2026-02-25", "EJECUTAR"],
    ["Medidor NO", "EQ-LIX-010", "2026-02-01", "VENCIDA"],
    ["Campana de extracción", "EQ-CB-092", "2025-08-07", "CRÍTICO"],
    ["Hidrolavadora GHP200", "EQ-CB-258", "SIN FECHA", "URGENTE"],
    ["Anemometro", "EQ-CB-198", "SIN FECHA", "URGENTE"]
]
df_maint = pd.DataFrame(mantencion_data, columns=["Equipo", "Código", "Próxima Fecha", "Estado"])

# --- VISUALIZACIÓN EN STREAMLIT ---

st.header("1. Inventario General")
def style_general(row):
    color_map = {
        'COINCIDE (ROSADO)': 'background-color: #f8bbd0',
        'DE BAJA (AZUL)': 'background-color: #bbdefb',
        'CÓDIGO NO COINCIDE (VERDE)': 'background-color: #c8e6c9'
    }
    return [color_map.get(row['Estado Auditado'], '')] * len(row)

st.dataframe(df_general.style.apply(style_general, axis=1), use_container_width=True)

st.header("2. Equipos Repetidos (Para Mejora de Gestión)")
st.info("Estos equipos presentan duplicidad de códigos o inconsistencias entre hojas. Requieren normalización.")
st.dataframe(df_mejorar.style.applymap(lambda x: 'background-color: #80cbc4; color: black', subset=['Estado']), use_container_width=True)

st.header("3. Plan de Mantención Inmediata (Estado Verde Azulado)")
st.dataframe(df_maint.style.applymap(lambda x: 'background-color: #80cbc4; color: black'), use_container_width=True)

# --- BOTÓN DE DESCARGA ---
output = BytesIO()
with pd.ExcelWriter(output, engine='openpyxl') as writer:
    df_general.to_excel(writer, sheet_name='Inventario_General', index=False)
    df_mejorar.to_excel(writer, sheet_name='Repetidos_Mejora', index=False)
    df_maint.to_excel(writer, sheet_name='Plan_Mantencion', index=False)

st.markdown("---")
st.download_button(
    label="📥 Descargar Reporte Completo (.xlsx)",
    data=output.getvalue(),
    file_name="Reporte_Final_TechOps_2026.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)
