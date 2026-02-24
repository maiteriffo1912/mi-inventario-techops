import streamlit as st
import pandas as pd
import io

# Configuración visual del reporte
st.set_page_config(page_title="Reporte Tech Ops", layout="wide")

st.title("📋 Reporte Profesional de Auditoría - Tech Ops")
st.markdown("---")

# Función para asignar estados y colores basados en las reglas del usuario
def procesar_inventario(df_rep, df_maint):
    # Unir las tablas por el nombre del equipo
    df_merged = pd.merge(df_rep, df_maint[['Equipos', 'Proxima mantención', 'Ultima mantención']], 
                         left_on='Equipos', right_on='Equipos', how='left')
    
    # Identificar duplicados en la columna de códigos (Verde Azulado)
    codigos_repetidos = df_merged[df_merged['codigos'].duplicated(keep=False) & 
                                  (df_merged['codigos'].notna()) & 
                                  (df_merged['codigos'] != 'SIN CODIGO')]['codigos'].unique()

    def clasificar(row):
        obs = str(row.get('Unnamed: 2', '')).lower()
        cod = str(row['codigos']).upper()
        
        if 'baja' in obs:
            return 'DE BAJA (AZUL)'
        if 'sin codigo' in cod or 'nan' in str(cod).lower():
            return 'SIN CÓDIGO (NARANJO)'
        if 'etiquetado como' in obs or 'pertenece a otro' in obs:
            return 'CÓDIGO NO COINCIDE (VERDE)'
        if row['codigos'] in codigos_repetidos:
            return 'CÓDIGO REPETIDO (VERDE AZULADO)'
        return 'COINCIDE (ROSADO)'

    df_merged['Estado Auditado'] = df_merged.apply(clasificar, axis=1)
    return df_merged

# Carga de archivos
col1, col2 = st.columns(2)
with col1:
    file_rep = st.file_uploader("Archivo 'Repetidos' (CSV)", type="csv")
with col2:
    file_maint = st.file_uploader("Archivo 'Hoja 2' (CSV)", type="csv")

if file_rep and file_maint:
    # Leer archivos saltando encabezados basura
    df_rep = pd.read_csv(file_rep, skiprows=8)
    df_maint = pd.read_csv(file_maint, skiprows=3)

    # Procesamiento
    reporte_final = procesar_inventario(df_rep, df_maint)

    # --- DISEÑO DEL REPORTE PARA JEFATURA ---
    st.header("1. Resumen Ejecutivo")
    
    m1, m2, m3, m4, m5 = st.columns(5)
    m1.metric("Óptimos (Rosado)", len(reporte_final[reporte_final['Estado Auditado'] == 'COINCIDE (ROSADO)']))
    m2.metric("Duplicados", len(reporte_final[reporte_final['Estado Auditado'] == 'CÓDIGO REPETIDO (VERDE AZULADO)']))
    m3.metric("No Coincide", len(reporte_final[reporte_final['Estado Auditado'] == 'CÓDIGO NO COINCIDE (VERDE)']))
    m4.metric("Sin Código", len(reporte_final[reporte_final['Estado Auditado'] == 'SIN CÓDIGO (NARANJO)']))
    m5.metric("De Baja", len(reporte_final[reporte_final['Estado Auditado'] == 'DE BAJA (AZUL)']))

    st.markdown("---")
    st.header("2. Detalle de Equipos y Mantenciones")

    # Estilo de celdas
    def color_rows(val):
        color_map = {
            'COINCIDE (ROSADO)': 'background-color: #f8bbd0',
            'CÓDIGO REPETIDO (VERDE AZULADO)': 'background-color: #80cbc4',
            'CÓDIGO NO COINCIDE (VERDE)': 'background-color: #c8e6c9',
            'SIN CÓDIGO (NARANJO)': 'background-color: #ffe0b2',
            'DE BAJA (AZUL)': 'background-color: #bbdefb'
        }
        return color_map.get(val, '')

    # Mostrar tabla profesional
    st.dataframe(reporte_final.style.applymap(color_rows, subset=['Estado Auditado']), use_container_width=True)

    # Botón de descarga
    buffer = io.BytesIO()
    reporte_final.to_excel(buffer, index=False)
    st.download_button(
        label="📥 Descargar Reporte Profesional (Excel)",
        data=buffer,
        file_name="Reporte_Inventario_TechOps.xlsx",
        mime="application/vnd.ms-excel"
    )
