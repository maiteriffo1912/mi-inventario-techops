import streamlit as st
import pandas as pd
from io import BytesIO
from datetime import datetime

st.set_page_config(page_title="Reporte Tech Ops Final", layout="wide")

st.title("📊 Reporte de Inventario y Plan de Mantención")
st.markdown("Este reporte identifica estados de equipos y prioridades de mantenimiento para jefatura.")

# --- 1. BASE DE DATOS INTEGRADA CON FECHAS ---
# Usamos la data real de tus archivos para que el reporte sea verídico
datos = [
    ["Agitador Magnetico", "EQ-CB-023", "2026-02-25", "COINCIDE (ROSADO)", "OK"],
    ["Balanza 100kg", "EQ-CB-217", "2026-04-04", "COINCIDE (ROSADO)", "OK"],
    ["Campana de extracción", "EQ-CB-092", "2025-08-07", "COINCIDE (ROSADO)", "MANTENCIÓN VENCIDA"],
    ["Balanza Analitica", "EQ-CB-021", "-", "DE BAJA (AZUL)", "No requiere mantención"],
    ["Medidor NO", "EQ-LIX-010", "2026-02-01", "CÓDIGO NO COINCIDE (VERDE)", "MANTENCIÓN VENCIDA"],
    ["Balanza digital", "EQ-CB-243", "2026-07-15", "CÓDIGO REPETIDO (VERDE AZULADO)", "Revisar duplicidad"],
    ["Anemómetro", "EQ-CB-254", "SIN FECHA", "CÓDIGO REPETIDO (VERDE AZULADO)", "URGENTE: Programar mantención"],
    ["Multiparametro portatil", "SIN CODIGO", "SIN FECHA", "SIN CÓDIGO (NARANJO)", "Pendiente codificar y programar"],
    ["Hidrolavadora GHP200", "EQ-CB-258", "SIN FECHA", "COINCIDE (ROSADO)", "URGENTE: Programar mantención"],
    ["Anemometro (198)", "EQ-CB-198", "SIN FECHA", "COINCIDE (ROSADO)", "URGENTE: Programar mantención"]
]

df = pd.DataFrame(datos, columns=["Equipo", "Código", "Próxima Mantención", "Estado", "Plan de Acción"])

# --- 2. LÓGICA DE ALERTAS DE MANTENIMIENTO ---
def resaltar_mantenimiento(val):
    if "VENCIDA" in val or "URGENTE" in val:
        return 'color: red; font-weight: bold'
    return ''

# --- 3. DISEÑO DEL REPORTE VISUAL ---
st.subheader("📋 Estado Actual y Necesidades de Mantenimiento")

# Colores para la tabla
def aplicar_estilos(row):
    colores = {
        'COINCIDE (ROSADO)': 'background-color: #f8bbd0; color: black',
        'CÓDIGO REPETIDO (VERDE AZULADO)': 'background-color: #80cbc4; color: black',
        'CÓDIGO NO COINCIDE (VERDE)': 'background-color: #c8e6c9; color: black',
        'SIN CÓDIGO (NARANJO)': 'background-color: #ffe0b2; color: black',
        'DE BAJA (AZUL)': 'background-color: #bbdefb; color: black'
    }
    return [colores.get(row['Estado'], '')] * len(row)

st.dataframe(
    df.style.apply(aplicar_estilos, axis=1)
            .applymap(resaltar_mantenimiento, subset=['Plan de Acción']),
    use_container_width=True
)



# --- 4. GENERACIÓN DEL EXCEL (Arreglo del Error xlsxwriter) ---
output = BytesIO()
# Usamos engine='xlsxwriter' porque ya lo agregamos al requirements.txt
with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
    df.to_excel(writer, index=False, sheet_name='Reporte_Jefatura')
    
st.download_button(
    label="📥 Descargar Reporte y Plan de Mantención (.xlsx)",
    data=output.getvalue(),
    file_name="Reporte_TechOps_Completo.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)

st.success("✅ Reporte listo. Se han identificado los equipos que requieren mantenimiento urgente en letras rojas.")
