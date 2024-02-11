import json
import psycopg2
from decouple import config

import disp_seg_db as disp_seg
import pru_db as pru
import horizontal_db as horizontal
import vertical_db as vertical


db_host = config('DB_HOST', default='localhost')
db_name = config('DB_NAME', default='Teste')
db_user = config('DB_USER', default='postgres')
db_password = config('DB_PASSWORD', default='teste')

conexao = psycopg2.connect(
    host=db_host,
    database=db_name,
    user=db_user,
    password=db_password
)

dict_type = {
    'DSEG': disp_seg,
    'PRU': pru,
    'SH': horizontal,
    'idade_': vertical
}

def db_execute(dicionario, chave_dicionario_db):
    query, values = dict_type[chave_dicionario_db].select_query(dicionario)
    cursor.execute(query, values)
    resultado = cursor.fetchone()

    if resultado:
        try:
            update_query, update_values  = dict_type[chave_dicionario_db].update_query(dicionario)
            cursor.execute(update_query, update_values)
            print("UPDATE bem-sucedido. ", dicionario['ID'])
        except Exception as e:
            print(f"Erro ao executar o INSERT: {e}")
        finally:
            conexao.commit()
    else:
        try:
            insert_query, insert_values = dict_type[chave_dicionario_db].insert_query(dicionario)
            print(insert_query, insert_values)
            input()
            cursor.execute(insert_query, insert_values)
            print("INSERT bem-sucedido. ", dicionario['ID'])
        except Exception as e:
            print(f"Erro ao executar o INSERT: {e}")
        finally:
            conexao.commit()

if __name__ == "__main__": 
    path_file_json  = 'JSON/SH_CAMAPANHA_6.json'
    
    with open(path_file_json, 'r', encoding='utf-8') as arquivo_json:
        data_dict = json.load(arquivo_json)

    input(f'O dicionário tem {len(data_dict)} elementos.')

    cursor = conexao.cursor()
    for dicionario in data_dict:
        if "DSEG" in path_file_json:
            db_execute(dicionario, "DSEG")

        elif "PRU" in path_file_json:
            db_execute(dicionario, "PRU")
        
        elif "SH" in path_file_json:
            db_execute(dicionario, "SH")

    cursor.close()
    conexao.close()

    print(f'{len(data_dict)} elementos atualizado/inserido com SUCESSO')
    print("FIM")




