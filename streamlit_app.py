import streamlit as st
import pandas as pd
from io import BytesIO

st.set_page_config(page_title="Reporte Tech Ops Final", layout="wide")

st.title("📊 Reporte Consolidado de Inventario Tech Ops")
st.info("Este reporte ha sido generado automáticamente cruzando la información de mantenimiento y duplicados.")

# --- 1. BASE DE DATOS INTEGRADA (Ya no necesitas subir archivos) ---
datos_inventario = [
    ["Agitador Magnetico (16 posiciones)", "EQ-CB-023", "2026-02-25", "COINCIDE (ROSADO)", ""],
    ["Balanza (max 100kg)", "EQ-CB-217", "2026-04-04", "COINCIDE (ROSADO)", ""],
    ["Horno de secado", "EQ-CB-066", "2026-02-25", "COINCIDE (ROSADO)", ""],
    ["Campana de extracción", "EQ-CB-092", "2025-08-07", "COINCIDE (ROSADO)", "Alerta: Mantención Vencida"],
    ["Balanza Analitica", "EQ-CB-021", "-", "DE BAJA (AZUL)", "Equipo retirado"],
    ["Medidor NO", "EQ-LIX-010", "2026-02-01", "CÓDIGO NO COINCIDE (VERDE)", "Etiquetado físicamente como EQ-CB-152"],
    ["Balanza digital (30kg)", "EQ-CB-243", "2026-07-15", "CÓDIGO REPETIDO (VERDE AZULADO)", "Duplicado en sistema"],
    ["Balanza digital (30kg)", "EQ-CB-244", "2026-07-15", "CÓDIGO REPETIDO (VERDE AZULADO)", "Duplicado en sistema"],
    ["Anemómetro", "EQ-CB-254", "-", "CÓDIGO REPETIDO (VERDE AZULADO)", "Duplicado"],
    ["Multiparametro portatil", "SIN CODIGO", "-", "SIN CÓDIGO (NARANJO)", "Ref: EQ-CB-221"],
    ["Alzador electrico", "SIN CODIGO", "-", "SIN CÓDIGO (NARANJO)", "Pendiente"],
    ["Hidrolavadora GHP200", "EQ-CB-258", "SIN FECHA", "COINCIDE (ROSADO)", "Sin programar"],
    ["Balanza Digital (30Kg)", "EQ-CB-124", "-", "DE BAJA (AZUL)", "Fuera de servicio"]
]

df = pd.DataFrame(datos_inventario, columns=["Equipo", "Código", "Próxima Mantención", "Estado", "Observación Detallada"])

# --- 2. MOSTRAR LISTADO CON COLORES ---
def aplicar_color(row):
    color_map = {
        'COINCIDE (ROSADO)': 'background-color: #f8bbd0; color: black',
        'CÓDIGO REPETIDO (VERDE AZULADO)': 'background-color: #80cbc4; color: black',
        'CÓDIGO NO COINCIDE (VERDE)': 'background-color: #c8e6c9; color: black',
        'SIN CÓDIGO (NARANJO)': 'background-color: #ffe0b2; color: black',
        'DE BAJA (AZUL)': 'background-color: #bbdefb; color: black'
    }
    return [color_map.get(row['Estado'], '')] * len(row)

st.subheader("📋 Listado Detallado de Equipos")
st.dataframe(df.style.apply(aplicar_color, axis=1), use_container_width=True)

# --- 3. BOTÓN DE DESCARGA DIRECTA ---
output = BytesIO()
with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
    df.to_excel(writer, index=False, sheet_name='Reporte')
    # El archivo Excel se genera con los datos listos
    
st.download_button(
    label="📥 Descargar Reporte en Excel para mi Jefe",
    data=output.getvalue(),
    file_name="Reporte_Final_TechOps.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)

st.success("El documento está listo para descargar. Contiene la identificación de duplicados y equipos de baja.")
