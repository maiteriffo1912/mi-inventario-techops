import streamlit as st
import pandas as pd

# Configuración de la página
st.set_page_config(page_title="Tech Ops Inventory", layout="wide")

st.title("📊 Sistema de Inventario Tech Ops")
st.markdown("Sube los archivos CSV para generar el reporte automático.")

# 1. Subida de archivos en la interfaz
col1, col2 = st.columns(2)
with col1:
    file_inv = st.file_uploader("Subir archivo 'Repetidos' (CSV)", type="csv")
with col2:
    file_man = st.file_uploader("Subir archivo 'Hoja 2' (CSV)", type="csv")

if file_inv and file_man:
    try:
        # 2. Carga de datos con los saltos de línea correctos según tus archivos
        # skiprows=9 para repetidos porque la tabla empieza en la fila 10
        df_inventario = pd.read_csv(file_inv, skiprows=9) 
        # skiprows=3 para Hoja2 porque la tabla empieza en la fila 4
        df_mantencion = pd.read_csv(file_man, skiprows=3)

        # Limpiar nombres de columnas (basado en tus archivos reales)
        df_inventario.columns = ['Equipos', 'Codigos', 'Observaciones']
        df_mantencion.columns = ['Equipos', 'Codigos_M', 'Proxima mantencion', 'Ultima mantencion', 'Extra']

        # 3. Unir tablas
        df_master = pd.merge(df_inventario, df_mantencion[['Equipos', 'Proxima mantencion', 'Ultima mantencion']], on='Equipos', how='left')

        # 4. Función de lógica de estados (tus colores)
        def determinar_estado(row):
            codigo = str(row['Codigos']).strip().upper()
            obs = str(row['Observaciones']).strip().lower()
            
            if 'baja' in obs:
                return 'De Baja (Azul)'
            if codigo == 'SIN CODIGO' or codigo == 'NAN':
                return 'Sin Código (Naranjo)'
            if 'etiquetado como' in obs or 'pertenece a otro' in obs:
                return 'No Coincide (Verde)'
            return 'Óptimo (Rosa)'

        df_master['Estado_Sugerido'] = df_master.apply(determinar_estado, axis=1)

        # 5. Detectar Duplicados (Verde Azulado)
        codigos_validos = df_master[df_master['Codigos'] != 'SIN CODIGO']
        duplicados = codigos_validos[codigos_validos.duplicated(subset=['Codigos'], keep=False)]['Codigos'].unique()
        df_master.loc[df_master['Codigos'].isin(duplicados), 'Estado_Sugerido'] = 'Código Repetido (Verde Azulado)'

        # 6. Aplicar Colores Visuales para la Web
        def style_estado(val):
            color_map = {
                'Óptimo (Rosa)': 'background-color: #fce4ec; color: black;',
                'Código Repetido (Verde Azulado)': 'background-color: #e0f2f1; color: black;',
                'No Coincide (Verde)': 'background-color: #e8f5e9; color: black;',
                'Sin Código (Naranjo)': 'background-color: #fff3e0; color: black;',
                'De Baja (Azul)': 'background-color: #e3f2fd; color: black;'
            }
            return color_map.get(val, '')

        # Mostrar Tabla
        st.subheader("📋 Reporte Consolidado")
        st.dataframe(df_master.style.applymap(style_estado, subset=['Estado_Sugerido']), use_container_width=True)

        # Botón para descargar el resultado
        csv = df_master.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Descargar Reporte en CSV", data=csv, file_name="Reporte_TechOps.csv", mime="text/csv")

    except Exception as e:
        st.error(f"Hubo un error procesando los archivos: {e}")
        st.info("Asegúrate de subir los archivos correctos que mostraste anteriormente.")

else:
    st.warning("Esperando que se suban ambos archivos para procesar...")
