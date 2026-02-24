import pandas as pd

# 1. CREACIÓN DE LA DATA BASADA EN TUS ARCHIVOS
data = {
    'Equipo': [
        'Agitador Magnetico (16 posiciones)', 'Balanza (max 100kg)', 'Horno de secado', 
        'Campana de extracción', 'Balanza Analitica', 'Medidor NO', 'Balanza digital (30kg)',
        'Balanza digital (30kg)', 'Anemómetro', 'Anemómetro', 'Multiparametro portatil', 
        'Alzador electrico', 'Hidrolavadora GHP200', 'Balanza Digital (30Kg)'
    ],
    'Codigo': [
        'EQ-CB-023', 'EQ-CB-217', 'EQ-CB-066', 'EQ-CB-092', 'EQ-CB-021', 
        'EQ-LIX-010', 'EQ-CB-243', 'EQ-CB-244', 'EQ-CB-254', 'EQ-CB-255', 
        'SIN CODIGO', 'SIN CODIGO', 'EQ-CB-258', 'EQ-CB-124'
    ],
    'Observacion_Original': [
        '', '', '', '', 'De baja', 
        'etiquetado como EQ-CB-152', 'repetido', 'repetido', 'repetido', 'repetido',
        'EQ-CB-221', '', 'Sin fecha mantencion', 'De baja'
    ]
}

df = pd.DataFrame(data)

# 2. LÓGICA DE IDENTIFICACIÓN DE ESTADOS
def asignar_estado(row):
    obs = str(row['Observacion_Original']).lower()
    cod = str(row['Codigo']).upper()
    
    if 'baja' in obs:
        return 'DE BAJA (AZUL)'
    if 'sin codigo' in cod:
        return 'SIN CÓDIGO (NARANJO)'
    if 'etiquetado como' in obs:
        return 'CÓDIGO NO COINCIDE (VERDE)'
    if 'repetido' in obs:
        return 'CÓDIGO REPETIDO (VERDE AZULADO)'
    return 'COINCIDE (ROSADO)'

df['Estado Auditado'] = df.apply(asignar_estado, axis=1)

# 3. EXPORTAR A EXCEL CON FORMATO PROFESIONAL
nombre_archivo = 'Reporte_Final_TechOps.xlsx'
writer = pd.ExcelWriter(nombre_archivo, engine='openpyxl')
df.to_excel(writer, index=False, sheet_name='Reporte Auditoria')

# Aplicar colores a las celdas de Excel
from openpyxl.styles import PatternFill

ws = writer.sheets['Reporte Auditoria']
colores = {
    'COINCIDE (ROSADO)': 'F8BBD0',
    'CÓDIGO REPETIDO (VERDE AZULADO)': '80CBC4',
    'CÓDIGO NO COINCIDE (VERDE)': 'C8E6C9',
    'SIN CÓDIGO (NARANJO)': 'FFE0B2',
    'DE BAJA (AZUL)': 'BBDEFBA'
}

for row in range(2, len(df) + 2):
    estado = ws.cell(row=row, column=4).value
    if estado in colores:
        color_hex = colores[estado]
        fill = PatternFill(start_color=color_hex, end_color=color_hex, fill_type='solid')
        ws.cell(row=row, column=4).fill = fill

writer.close()
print(f"✅ Archivo '{nombre_archivo}' generado con éxito.")
