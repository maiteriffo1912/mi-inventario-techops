import pandas as pd
import numpy as np

# 1. Cargar los archivos CSV (asegúrate de que los nombres coincidan con tus archivos)
# Omitimos las primeras filas de 'repetidos.csv' que contienen la leyenda de colores
df_inventario = pd.read_csv('Mantencion equipos tech ops (1).xlsx - repetidos.csv', skiprows=10) 
df_mantencion = pd.read_csv('Mantencion equipos tech ops (1).xlsx - Hoja2.csv', skiprows=3)

# Limpiar nombres de columnas para evitar errores por espacios extra
df_inventario.columns = ['Equipos', 'Codigos', 'Observaciones']
df_mantencion.columns = ['Equipos', 'Codigos', 'Proxima mantencion', 'Ultima mantencion']

# 2. Unir ambas tablas usando el nombre del equipo como referencia principal
df_master = pd.merge(df_inventario, df_mantencion, on='Equipos', how='left')

# 3. Función para determinar el Estado (Simulando tus colores)
def determinar_estado(row):
    codigo = str(row['Codigos_x']).strip().upper()
    obs = str(row['Observaciones']).strip().lower()
    
    # Azul: De baja (Asumiendo que lo anotas en la observación)
    if 'baja' in obs:
        return 'De Baja (Azul)'
    
    # Naranjo: Sin código
    if codigo == 'SIN CODIGO' or codigo == 'NAN':
        return 'Sin Código (Naranjo)'
    
    # Verde: Inconsistencia (etiquetado diferente)
    if 'etiquetado como' in obs or 'pertenece a otro' in obs:
        return 'No Coincide (Verde)'
    
    return 'Por Evaluar'

# Aplicar la función para crear la columna de Estado
df_master['Estado_Sugerido'] = df_master.apply(determinar_estado, axis=1)

# 4. Detectar Duplicados (Verde Azulado)
# Marcamos como duplicados aquellos códigos que aparecen más de una vez y no son "SIN CODIGO"
codigos_validos = df_master[df_master['Codigos_x'] != 'SIN CODIGO']
duplicados = codigos_validos[codigos_validos.duplicated(subset=['Codigos_x'], keep=False)]['Codigos_x'].unique()

df_master.loc[df_master['Codigos_x'].isin(duplicados), 'Estado_Sugerido'] = 'Código Repetido (Verde Azulado)'

# Asignar 'Óptimo (Rosa)' a los que pasaron todas las pruebas y no tienen problemas
df_master.loc[df_master['Estado_Sugerido'] == 'Por Evaluar', 'Estado_Sugerido'] = 'Óptimo (Rosa)'

# 5. Limpieza final de columnas
df_master = df_master[['Equipos', 'Codigos_x', 'Estado_Sugerido', 'Proxima mantencion', 'Ultima mantencion', 'Observaciones']]
df_master.rename(columns={'Codigos_x': 'Codigo'}, inplace=True)

# 6. Exportar el resultado a un nuevo archivo Excel
nombre_archivo_salida = 'Reporte_Auditoria_Tech_Ops.xlsx'
df_master.to_excel(nombre_archivo_salida, index=False)

print(f"¡Reporte generado con éxito! Revisa el archivo: {nombre_archivo_salida}")