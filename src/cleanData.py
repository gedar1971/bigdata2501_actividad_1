import pandas as pd
from static.db.config  import create_connection, create_table
from utils.helpers import create_file, format_number, log_step, get_output_txt, convert_to_numeric, convert_to_lowercase
import numpy as np


log_step(f"Inicio proceso de limpieza de datos\n")


table_name = "coincap" 
table_clean = "coincap_clean"
conn = create_connection('bd_analisis.sqlite')
cursor = conn.cursor()
cursor.execute(f"SELECT * FROM {table_name}")

log_step(f"Conexión a la base de datos establecida y datos recuperados de {table_name}\n")

df_bd_coincap = pd.DataFrame(cursor.fetchall(), columns=[x[0] for x in cursor.description])
log_step(f"DataFrame inicial creada con forma:\n{df_bd_coincap.shape}\n")


df_coincap_log = get_output_txt(df_bd_coincap, 'info')
log_step(f"Información de DataFrame:\n{df_coincap_log}\n")

nonullos=df_bd_coincap['maxSupply'].isnull().sum()
print(nonullos)


df_clean = df_bd_coincap.drop_duplicates()
log_step(f"Duplicados eliminados. Nueva forma:\n{df_clean.shape}\n")



numeric_columns = ['maxSupply', 'supply', 'marketCapUsd','volumeUsd24Hr','priceUsd','changePercent24Hr','vwap24Hr']
log_step(f"Creando el array con las columnas que van a convertirse a numéricas: \n{numeric_columns}\n")

# for column in numeric_columns:
#     df_clean[column] = pd.to_numeric(df_clean[column], errors='coerce')
convert_to_numeric(df_clean, numeric_columns)
log_step("convertiendo las columnas a numéricas\n")

convert_to_lowercase(df_clean, ['name'])
log_step("convertiendo las columna name a minuscula\n")

df_clean_log = get_output_txt(df_clean, 'info')
log_step(f"información de DataFrame con las columnas convertidas a numéricas: \n{df_clean_log}\n")
df_clean_end = df_clean


log_step(f"DataFrame final creada con forma: \n{df_clean_end.shape}\n")




log_step("Llenando valores nulos\n")
df_clean_end = df_clean.fillna({
    'maxSupply': 0, 
    'supply': 0,
    'marketCapUsd': 0,
    'volumeUsd24Hr': 0,
    'priceUsd': 0,
    'changePercent24Hr': 0,
    'vwap24Hr': 0,
    'explorer': 'Sin datos'
})


df_clean_log_end = get_output_txt(df_clean_end, 'info')
log_step(f"DataFrameb despues de eliminar  elementos son nulos: \n{df_clean_log_end}\n")



create_file(df_clean_end, 'src/static/cleaned_data/cleaned_data.csv', file_format='csv')
log_step("Archivo CSV generado\n")

create_file(df_clean_end,'src/static/cleaned_data/cleaned_data.xlsx', file_format='xlsx')
log_step("Archivo Excel generado\n")


create_table(conn, table_clean, df_clean_end)
log_step(f"Tabla de limpieza creada: \n{table_clean}\n")


