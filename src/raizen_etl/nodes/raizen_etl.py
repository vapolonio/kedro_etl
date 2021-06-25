from kedro.io import MemoryDataSet
from typing import Dict
import pandas as pd 

def download_file() -> MemoryDataSet:
    import wget
    file_url = 'http://www.anp.gov.br/arquivos/dados-estatisticos/vendas-combustiveis/vendas-combustiveis-m3.xls'
    path_file = f'data/01_raw/vendas-combustiveis-m3.xls'
    wget.download(file_url, path_file)
    return MemoryDataSet(data=[])
def convert_xls_ods(data: MemoryDataSet) -> MemoryDataSet:
    import os
    os.chdir(f'./data/01_raw/')
    stream = os.popen('soffice --headless --convert-to ods vendas-combustiveis-m3.xls')
    output = stream.read()
    print(output)
    return MemoryDataSet(data=[])
def partition_by_date(df: pd.DataFrame) -> Dict[str, pd.DataFrame]:
    parts = {}
    
    for year in df['year_month'].dt.year.unique():
        parts[f'date=={year}'] = df[df['year_month'].dt.year == year]
    return parts
def cleaning(data: MemoryDataSet) -> pd.DataFrame:
    from pandas_ods_reader import read_ods
    # import pandas as pd
    import os
    from kedro.extras.datasets.pandas import ParquetDataSet 
    from datetime import datetime
    pd.set_option('display.precision', 2)
    UF = {
        'Acre': 'AC',
        'Alagoas': 'AL',
        'Amazonas': 'AM',
        'Amapá': 'AP',
        'Bahia': 'BA',
        'Ceará': 'CE',
        'Distrito Federal': 'DF',
        'Espírito Santo': 'ES',
        'Goiás': 'GO',
        'Maranhão': 'MA',
        'Minas Gerais': 'MG',
        'Mato Grosso do Sul': 'MS',
        'Mato Grosso': 'MT',
        'Pará': 'PA',
        'Paraíba': 'PB',
        'Pernambuco': 'PE',
        'Piauí': 'PI',
        'Paraná': 'PR',
        'Rio de Janeiro': 'RJ',
        'Rio Grande do Norte': 'RN',
        'Rondônia': 'RO',
        'Roraima': 'RR',
        'Rio Grande do Sul': 'RS',
        'Santa Catarina': 'SC',
        'Sergipe': 'SE',
        'São Paulo': 'SP',
        'Tocantins': 'TO'
    }

    UF = dict((k.upper(), v.upper()) for k, v in UF.items()) 

    months = [
        'Jan',
        'Fev',
        'Mar',
        'Abr',
        'Mai',
        'Jun',
        'Jul',
        'Ago',
        'Set',
        'Out',
        'Nov',
        'Dez'
    ]

    derivados = ['ETANOL HIDRATADO', 'GASOLINA C', 'GASOLINA DE AVIAÇÃO', 'GLP', 'ÓLEO COMBUSTÍVEL', 'ÓLEO DIESEL', 'QUEROSENE DE AVIAÇÃO', 'QUEROSENE ILUMINANTE']
    diesel = ['ÓLEO DIESEL (OUTROS )', 'ÓLEO DIESEL MARÍTIMO', 'ÓLEO DIESEL S-10', 'ÓLEO DIESEL S-500', 'ÓLEO DIESEL S-1800']

    #Carregando arquivos ods
    os.chdir(f'../../')
    df_2 = read_ods('data/01_raw/vendas-combustiveis-m3.ods', 2)
    df_3 = read_ods('data/01_raw/vendas-combustiveis-m3.ods', 3)

    #concatenando e montando dataset
    dataset = pd.concat([df_2, df_3])

    final = list()
    for row in dataset.fillna(0).to_dict(orient='records'):
        _header = {
            'uf': UF[row['ESTADO']],
            'product': row['COMBUSTÍVEL'].replace(' (m3)', ''),
            'unit': 'm3',
        }
        if _header['product'] in derivados + diesel:
            for index, month in enumerate(months):
                final.append({
                  **{
                    'year_month': datetime.strptime(f"{int(row['ANO'])}-{index + 1}", '%Y-%m'),
                    'volume': row[month],
                    'created_at': datetime.now()
                }
                , **_header, 
                })
    return pd.DataFrame(final)[['year_month', 'uf', 'product', 'unit', 'volume', 'created_at']]
