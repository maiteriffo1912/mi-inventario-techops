import streamlit as st
import pandas as pd

st.set_page_config(page_title="Tech Ops Inventory Report", layout="wide")

st.title("📋 Reporte Profesional de Inventario Tech Ops")
st.markdown("---")

# Subida de archivos
col1, col2 = st.columns(2)
with col1:
    file_inv = st.file_uploader("Subir Hoja 'Repetidos'", type="csv")
with col2:
    file_man = st.file_uploader("Subir 'Hoja 2' (Mantenciones)", type="csv")

if file_inv and file_man:
    try:
        # Carga de datos
        df_inv = pd.read_csv(file_inv, skiprows=9)
        df_man = pd.read_csv(file_man, skiprows=3)

        # Limpieza inicial
        df_inv.columns = ['Equipo', 'Codigo', 'Observaciones']
        df_man = df_man[['Equipos', 'Proxima mantención', 'Ultima mantención']].rename(columns={'Equipos': 'Equipo'})

        # Cruzar información
        df_final = pd.merge(df_inv, df_man, on='Equipo', how='left')

        # Lógica de estados según tus instrucciones
        def asignar_estado(row):
            obs = str(row['Observaciones']).lower()
            cod = str(row['Codigo']).upper()
            
            if 'baja' in obs:
                return 'DE BAJA (AZUL)'
            if 'sin codigo' in cod or 'nan' in str(cod).lower():
                return 'SIN CÓDIGO (NARANJO)'
            if 'etiquetado como' in obs or 'pertenece a otro' in obs:
                return 'CÓDIGO NO COINCIDE (VERDE)'
            return 'VALOR PREDETERMINADO'

        df_final['Estado'] = df_final.apply(asignar_estado, axis=1)

        # Identificar Duplicados (VERDE AZULADO)
        # Buscamos códigos que se repiten en la lista
        codigos_limpios = df_final[df_final['Codigo'].notna() & (df_final['Codigo'] != 'SIN CODIGO')]
        duplicados = codigos_limpios[codigos_limpios.duplicated('Codigo', keep=False)]['Codigo'].unique()
        
        df_final.loc[df_final['Codigo'].isin(duplicados), 'Estado'] = 'CÓDIGO REPETIDO (VERDE AZULADO)'
        
        # El resto que no entró en categorías críticas es ROSADO
        df_final.loc[df_final['Estado'] == 'VALOR PREDETERMINADO', 'Estado'] = 'COINCIDE (ROSADO)'

        # --- REPORTE PARA EL JEFE ---
        st.subheader("📊 Resumen Ejecutivo para Jefatura")
        
        metrica1, metrica2, metrica3, metrica4 = st.columns(4)
        metrica1.metric("Total Equipos", len(df_final))
        metrica2.metric("Sin Código", len(df_final[df_final['Estado'] == 'SIN CÓDIGO (NARANJO)']))
        metrica3.metric("Duplicados", len(duplicados))
        metrica4.metric("De Baja", len(df_final[df_final['Estado'] == 'DE BAJA (AZUL)']))

        # Función para colorear la tabla
        def color_estilo(val):
            color_map = {
                'COINCIDE (ROSADO)': 'background-color: #f8bbd0; color: black',
                'CÓDIGO REPETIDO (VERDE AZULADO)': 'background-color: #80cbc4; color: black',
                'CÓDIGO NO COINCIDE (VERDE)': 'background-color: #c8e6c9; color: black',
                'SIN CÓDIGO (NARANJO)': 'background-color: #ffe0b2; color: black',
                'DE BAJA (AZUL)': 'background-color: #bbdefb; color: black'
            }
            return color_map.get(val, '')

        st.markdown("### Detalle de Inventario Auditado")
        st.dataframe(df_final.style.applymap(color_estilo, subset=['Estado']), use_container_width=True)

        # Botón de Descarga
        csv_data = df_final.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Descargar Reporte Final para Excel", data=csv_data, file_name="Reporte_Final_TechOps.csv")

    except Exception as e:
        st.error(f"Error en el proceso: {e}")
