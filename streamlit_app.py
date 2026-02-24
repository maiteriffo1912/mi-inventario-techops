import streamlit as st
import pandas as pd
from io import BytesIO

st.set_page_config(page_title="Reporte Maestro Tech Ops", layout="wide")

st.title("📊 Reporte Maestro: Inventario y Plan de Mantención")

# --- GUÍA DE COLORES PARA EL JEFE ---
st.subheader("💡 Guía de Estados y Colores")
c1, c2, c3, c4, c5 = st.columns(5)
c1.markdown("<div style='background-color: #f8bbd0; padding: 10px; border-radius: 5px; color: black; text-align: center;'><b>ROSADO</b><br>Coincide / OK</div>", unsafe_allow_html=True)
c2.markdown("<div style='background-color: #80cbc4; padding: 10px; border-radius: 5px; color: black; text-align: center;'><b>VERDE AZULADO</b><br>Código Repetido</div>", unsafe_allow_html=True)
c3.markdown("<div style='background-color: #c8e6c9; padding: 10px; border-radius: 5px; color: black; text-align: center;'><b>VERDE</b><br>No Coincide</div>", unsafe_allow_html=True)
c4.markdown("<div style='background-color: #ffe0b2; padding: 10px; border-radius: 5px; color: black; text-align: center;'><b>NARANJO</b><br>Sin Código</div>", unsafe_allow_html=True)
c5.markdown("<div style='background-color: #bbdefb; padding: 10px; border-radius: 5px; color: black; text-align: center;'><b>AZUL</b><br>De Baja</div>", unsafe_allow_html=True)

st.markdown("---")

# --- BASE DE DATOS REAL (Basada en tus archivos) ---
datos = [
    ["Agitador Magnetico (16 pos)", "EQ-CB-023", "2026-02-25", "COINCIDE (ROSADO)", "Operativo"],
    ["Balanza (max 100kg)", "EQ-CB-217", "2026-04-04", "COINCIDE (ROSADO)", "Operativo"],
    ["Campana de extracción", "EQ-CB-092", "2025-08-07", "COINCIDE (ROSADO)", "MANTENCIÓN VENCIDA"],
    ["Balanza Analitica", "EQ-CB-021", "-", "DE BAJA (AZUL)", "Retirar de inventario"],
    ["Medidor NO", "EQ-LIX-010", "2026-02-01", "CÓDIGO NO COINCIDE (VERDE)", "ERROR: Dice EQ-CB-152"],
    ["Balanza digital (30kg)", "EQ-CB-243", "2026-07-15", "CÓDIGO REPETIDO (VERDE AZULADO)", "Duplicado con 244-246"],
    ["Anemómetro", "EQ-CB-254", "SIN FECHA", "CÓDIGO REPETIDO (VERDE AZULADO)", "Repetido / Programar"],
    ["Multiparametro portatil", "SIN CODIGO", "SIN FECHA", "SIN CÓDIGO (NARANJO)", "Regularizar placa"],
    ["Alzador electrico", "SIN CODIGO", "-", "SIN CÓDIGO (NARANJO)", "Pendiente"],
    ["Hidrolavadora GHP200", "EQ-CB-258", "SIN FECHA", "COINCIDE (ROSADO)", "Programar Mantención"],
    ["Anemometro (198)", "EQ-CB-198", "SIN FECHA", "COINCIDE (ROSADO)", "Programar Mantención"],
    ["Balanza Digital (124)", "EQ-CB-124", "-", "DE BAJA (AZUL)", "Dada de baja"],
]

df = pd.DataFrame(datos, columns=["Equipo", "Código", "Próxima Mantención", "Estado", "Observación/Acción"])

# --- LÓGICA DE VISUALIZACIÓN ---
def color_tabla(row):
    color_map = {
        'COINCIDE (ROSADO)': 'background-color: #f8bbd0',
        'CÓDIGO REPETIDO (VERDE AZULADO)': 'background-color: #80cbc4',
        'CÓDIGO NO COINCIDE (VERDE)': 'background-color: #c8e6c9',
        'SIN CÓDIGO (NARANJO)': 'background-color: #ffe0b2',
        'DE BAJA (AZUL)': 'background-color: #bbdefb'
    }
    return [color_map.get(row['Estado'], '')] * len(row)

st.subheader("📋 Inventario Completo Detallado")
st.dataframe(df.style.apply(color_tabla, axis=1), use_container_width=True)

# --- EXPLICACIÓN DE HALLAZGOS ---
st.subheader("🔍 Explicación de Hallazgos Críticos")
with st.expander("Ver detalles para Jefatura"):
    st.write("- **Error de Etiquetado:** El Medidor NO figura como 010 pero tiene la placa 152. Riesgo de trazabilidad.")
    st.write("- **Duplicidad:** Las Balanzas y Anemómetros al final de la lista comparten códigos. Requieren folios únicos.")
    st.write("- **Mantenimiento:** Equipos como la Campana de Extracción están con fecha vencida desde 2025.")

# --- BOTÓN DE DESCARGA ---
output = BytesIO()
with pd.ExcelWriter(output, engine='openpyxl') as writer:
    df.to_excel(writer, index=False, sheet_name='Inventario')
    
st.download_button(
    label="📥 Descargar Documento Excel Profesional",
    data=output.getvalue(),
    file_name="Reporte_Inventario_TechOps.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)
