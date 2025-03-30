import pandas as pd
import sqlite3
import os


def create_connection(db_name:str):
    db_path = os.path.join(os.curdir,db_name)
    connection = None
    try:
        connection = sqlite3.connect(db_path)
        print("Connection to SQLite DB successful")
    except sqlite3.Error as e:
        print(f"The error '{e}' occurred")
    return connection

def create_table(conn, table_name:str, data:list):
    try:
        # Replace applymap with map for each column
        df_api = data.copy()
        for column in df_api.columns:
            df_api[column] = df_api[column].map(lambda x: str(x) if isinstance(x, list) else x)
        
        df_api.to_sql(table_name, conn, if_exists='replace', index=False)
        print(f"Datos insertados en la tabla {table_name} exitosamente.")
    except Exception as e:
        print(f"Error al crear la tabla: {str(e)}")
    # if isinstance(data, dict):
    #     data = [data]

    # # data = pd.json_normalize(data, record_path=['data'], meta=['timestamp'])
    # if conn:
    #     df_api = data.applymap(lambda x: str(x) if isinstance(x, list) else x)
    #     df_api.to_sql(table_name, conn, if_exists='replace', index=False)
    #     print("Datos insertados en la base de datos exitosamente.")
    #     conn.close()
