import pandas as pd
import os
from dotenv import load_dotenv
from api.apiBase import fetch_data_from_api
from static.db.config  import create_connection, create_table
from utils.helpers import  create_file, audit_data


load_dotenv()

def main():

    api_url = 'https://api.coincap.io/v2/assets'
    
    data = fetch_data_from_api(api_url)

    df_api = pd.json_normalize(data, record_path=['data'], meta=['timestamp'])

    audit_data(df_api)

    create_file(df_api, 'src/static/xlsx/request_api_xlsx.xlsx', file_format='xlsx')

    conn = create_connection('bd_analisis.sqlite')

    create_table(conn, table_name='coincap', data=df_api)

if __name__ == '__main__':
    main()