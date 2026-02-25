import streamlit as st
import pandas as pd
from io import BytesIO

st.set_page_config(page_title="Reporte Maestro Tech Ops", layout="wide")

st.title("📊 Auditoría Técnica Tech Ops - Reporte Integral")
st.markdown("---")

# --- GUÍA DE COLORES ---
st.subheader("💡 Guía de Colores")
c1, c2, c3, c4, c5 = st.columns(5)
c1.markdown("<div style='background-color: #f8bbd0; padding: 10px; border-radius: 5px; color: black; text-align: center;'><b>ROSADO</b><br>Coincide / OK</div>", unsafe_allow_html=True)
c2.markdown("<div style='background-color: #80cbc4; padding: 10px; border-radius: 5px; color: black; text-align: center;'><b>VERDE AZULADO</b><br>Conflictos / Mantención</div>", unsafe_allow_html=True)
c3.markdown("<div style='background-color: #c8e6c9; padding: 10px; border-radius: 5px; color: black; text-align: center;'><b>VERDE</b><br>No Coincide</div>", unsafe_allow_html=True)
c4.markdown("<div style='background-color: #ffe0b2; padding: 10px; border-radius: 5px; color: black; text-align: center;'><b>NARANJO</b><br>Sin Código</div>", unsafe_allow_html=True)
c5.markdown("<div style='background-color: #bbdefb; padding: 10px; border-radius: 5px; color: black; text-align: center;'><b>AZUL</b><br>De Baja</div>", unsafe_allow_html=True)

# --- 1. LISTADO GENERAL COMPLETO ---
st.header("1. Listado General de Inventario (Completo)")
inv_data = [
    ["Agitador Magnetico (16 posiciones)", "EQ-CB-023", "ROSADO"],
    ["Balanza (max 100kg)", "EQ-CB-217", "ROSADO"],
    ["Balanza de (Max 30 kg / min: 1 g)", "EQ-CB-175", "ROSADO"],
    ["Horno de secado", "EQ-CB-066", "ROSADO"],
    ["Balanza (Max: 30Kg / 196)", "EQ-CB-196", "ROSADO"],
    ["Balanza (Max: 30Kg / 197)", "EQ-CB-197", "ROSADO"],
    ["Campana de extracción Quimica", "EQ-CB-092", "ROSADO"],
    ["Multiparametro pH/ORP/ISE Meter", "EQ-CB-105", "ROSADO"],
    ["Agitador Magnetico 10 posiciones", "EQ-CB-111", "ROSADO"],
    ["Agitador Magnetico Pequeño", "EQ-CB-112", "ROSADO"],
    ["Balanza Analitica (120g)", "EQ-CB-021", "AZUL"],
    ["Agitador Magnetico Pequeño (122)", "EQ-CB-122", "ROSADO"],
    ["Multiparametro pH/ORP/ISE Meter (127)", "EQ-CB-127", "ROSADO"],
    ["Medidor de gases WolfPack (153)", "EQ-CB-153", "ROSADO"],
    ["Medidor de gases WolfPack (154)", "EQ-CB-154", "ROSADO"],
    ["Balanza semi analítica (1kg)", "EQ-CB-176", "ROSADO"],
    ["Balanza 60Kg (224)", "EQ-CB-224", "ROSADO"],
    ["Refrigerador convencional", "EQ-CB-178", "ROSADO"],
    ["Balanza (3000g - 225)", "EQ-CB-225", "ROSADO"],
    ["Equipo Medición de gases (192)", "EQ-CB-192", "ROSADO"],
    ["Balanza (Max: 6Kk - 210)", "EQ-CB-210", "ROSADO"],
    ["Medidor NO2 (219)", "EQ-CB-219", "ROSADO"],
    ["Medidor NO2 (220)", "EQ-CB-220", "VERDE AZULADO"],
    ["Multiparametro portatil (222)", "EQ-CB-222", "ROSADO"],
    ["Balanza (3000g - 226)", "EQ-CB-226", "ROSADO"],
    ["Celular (228)", "EQ-CB-228", "ROSADO"],
    ["Celular (229)", "EQ-CB-229", "ROSADO"],
    ["Balanza digital (242)", "EQ-CB-242", "ROSADO"],
    ["Celular (236)", "EQ-CB-236", "ROSADO"],
    ["Celular (237)", "EQ-CB-237", "ROSADO"],
    ["Equipo Medición de gases (239)", "EQ-CB-239", "ROSADO"],
    ["Balanza digital (243)", "EQ-CB-243", "VERDE AZULADO"],
    ["Balanza digital (244)", "EQ-CB-244", "VERDE AZULADO"],
    ["Balanza digital (245)", "EQ-CB-245", "VERDE AZULADO"],
    ["Balanza digital (246)", "EQ-CB-246", "VERDE AZULADO"],
    ["Medidor H2S (252)", "EQ-CB-252", "ROSADO"],
    ["Medidor SO2 (253)", "EQ-CB-253", "ROSADO"],
    ["Anemómetro (254)", "EQ-CB-254", "VERDE AZULADO"],
    ["Anemómetro (255)", "EQ-CB-255", "VERDE AZULADO"],
    ["Anemómetro (256)", "EQ-CB-256", "VERDE AZULADO"],
    ["Hidrolavadora GHP200", "EQ-CB-258", "ROSADO"],
    ["Medidor NO2 (LIX-009)", "EQ-LIX-009", "ROSADO"],
    ["Medidor NO (LIX-010)", "EQ-LIX-010", "VERDE"],
    ["Balanza digital (610g)", "EQ-CB-003", "ROSADO"],
    ["Balanza Digital (124)", "EQ-CB-124", "AZUL"],
    ["Anemometro (198)", "EQ-CB-198", "VERDE AZULADO"],
    ["Multiparametro (057)", "EQ-CB-057", "VERDE AZULADO"],
    ["Multiparametro Portatil", "SIN CODIGO", "NARANJO"],
    ["Alzador electrico", "SIN CODIGO", "NARANJO"],
    ["Carro amarillo", "SIN CODIGO", "NARANJO"],
    ["Traspaleta", "SIN CODIGO", "NARANJO"],
    ["Bomba de residuo", "SIN CODIGO", "NARANJO"],
    ["Equipo Autonomo", "SIN CODIGO", "NARANJO"],
    ["Ups (2)", "SIN CODIGO", "NARANJO"]
]
df_gen = pd.DataFrame(inv_data, columns=["Instrumento", "Código", "Clasificación"])

def style_gen(row):
    color_map = {'ROSADO': 'background-color: #f8bbd0', 'AZUL': 'background-color: #bbdefb', 
                 'VERDE AZULADO': 'background-color: #80cbc4', 'VERDE': 'background-color: #c8e6c9',
                 'NARANJO': 'background-color: #ffe0b2'}
    return [color_map.get(row['Clasificación'], '')] * len(row)

st.dataframe(df_gen.style.apply(style_gen, axis=1), height=500, use_container_width=True)

# --- 2. HOJA 1: DUPLICADOS Y CONFLICTOS ---
st.header("2. Instrumentos Duplicados y Conflictos (Mejora de Gestión)")
data_h1 = [
    ["Anemometro", "EQ-CB-198", "Conflicto con Balanza digital"],
    ["Balanza digital", "EQ-CB-198", "No inventariada / Código duplicado"],
    ["Plancha calefactora", "EQ-CB-223", "Conflicto con Balanza 60Kg"],
    ["Balanza 60Kg", "EQ-CB-223", "No inventariada / Código duplicado"],
    ["Equipo Autonomo", "EQ-CB-218", "Conflicto con Campana"],
    ["Campana de extracción", "EQ-CB-218", "No inventariada"],
    ["Multiparametro pH-ISE", "EQ-CB-220", "No pertenece a área"],
    ["Medidor NO2", "EQ-CB-220", "Código duplicado"],
    ["Baño Ultrasonico", "EQ-CB-057", "No pertenece a área"],
    ["Multiparametro pH/ORP", "EQ-CB-057", "Conflicto con Baño"],
    ["Multiparametro Portatil", "EQ-CB-215", "Código inexistente"],
    ["Carro rojo", "EQ-CB-215", "Conflicto con Multiparámetro"],
    ["Balanza analitica", "EQ-CB-205", "Lab Analítico"],
    ["Bomba de vacio", "EQ-CB-205", "Conflicto con Balanza"]
]
df_h1 = pd.DataFrame(data_h1, columns=["Instrumento", "Código", "Detalle Mejora"])
st.dataframe(df_h1.style.applymap(lambda x: 'background-color: #80cbc4; color: black'), use_container_width=True)

# --- 3. HOJA 2: MANTENCIONES MARZO (ACTUALIZADO) ---
st.header("3. Listado de Mantenciones - Mes de Marzo")
data_maint = [
    ["Agitador Magnetico (16 posiciones)", "EQ-CB-023", "2/25/2026", "N/A"],
    ["Horno de secado", "EQ-CB-066", "2/25/2026", "N/A"],
    ["Campana de extracción Quimica sin ducto", "EQ-CB-092", "8/7/2025", "8/7/2023"],
    ["Multiparametro pH/ORP/ISE Meter", "EQ-CB-105", "8/1/2025", "N/A"],
    ["Agitador Magnetico 10 posiciones", "EQ-CB-111", "2/25/2026", "N/A"],
    ["Agitador Magnetico Pequeño", "EQ-CB-112", "2/25/2026", "N/A"],
    ["Agitador Magnetico Pequeño", "EQ-CB-122", "2/25/2026", "N/A"],
    ["Multiparametro pH/ORP/ISE Meter", "EQ-CB-127", "11/18/2025", "11/18/2025"],
    ["Medidor de gases The WolfPack DSII 8 PROBEE", "EQ-CB-154", "8/5/2025", "8/28/2024"],
    ["Refrigerador convencional", "EQ-CB-178", "2/25/2026", "N/A"],
    ["Balanza (max 3000g - d= 0,1g)", "EQ-CB-225", "4/11/2025", "N/A"],
    ["Balanza (Max: 6Kk / Min 1g /d=0,1g)", "EQ-CB-210", "7/11/2025", "N/A"],
    ["Multiparametro portatil", "EQ-CB-222", "8/1/2025", "N/A"],
    ["Medidor NO", "EQ-LIX-010", "2/1/2026", "7/24/2025"],
    ["Multiparametro pH/ORP/ISE Meter", "EQ-CB-057", "2/25/2026", "N/A"],
    ["Celular", "EQ-CB-237", "2/25/2026", "N/A"]
]
df_maint = pd.DataFrame(data_maint, columns=["Equipo", "Código", "Proxima mantención", "Ultima mantención"])

# Estilo para destacar la Hoja 2
st.dataframe(df_maint.style.applymap(lambda x: 'background-color: #80cbc4; color: black'), use_container_width=True)

# --- DESCARGA ---
output = BytesIO()
with pd.ExcelWriter(output, engine='openpyxl') as writer:
    df_gen.to_excel(writer, sheet_name='Listado_Completo', index=False)
    df_h1.to_excel(writer, sheet_name='Conflictos_Hoja1', index=False)
    df_maint.to_excel(writer, sheet_name='Mantencion_Marzo', index=False)

st.download_button(label="📥 Descargar Reporte Final Tech Ops (.xlsx)", data=output.getvalue(), 
                   file_name="Auditoria_TechOps_Marzo.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
