import os
import json
import psycopg2
from decouple import config
from datetime import datetime

from db import disp_seg_db as disp_seg
from db import pru_db as pru
from db import horizontal_db as horizontal
from db import vertical_db as vertical

db_host = config('DB_HOST', default='localhost')
db_name = config('DB_NAME', default='Teste')
db_user = config('DB_USER', default='postgres')
db_password = config('DB_PASSWORD', default='teste')

connection = psycopg2.connect(
    host=db_host,
    database=db_name,
    user=db_user,
    password=db_password
)

dict_type = {
    'DSEG': disp_seg,
    'PRU': pru,
    'SH': horizontal,
    'SV': vertical
}

id_mapping = {"DSEG": "ds_id", "PRU": "ru_id", "SH": "ID", "SV": "ID"}


def get_id_key(key_dictionary_db):
    return id_mapping.get(key_dictionary_db, "ID")


def db_execute(dictionary, key_dictionary_db):
    query, values = dict_type[key_dictionary_db].select_query(dictionary)
    cursor.execute(query, values)
    result = cursor.fetchone()   
    id = get_id_key(key_dictionary_db)

    if result:
        try:
            if key_dictionary_db == 'SV' or key_dictionary_db == 'SH':
                modification_date_result =result[-1]
            
                if modification_date_result >= datetime(2024, 1, 24).date():
                    print("Data Depois, não faça nada")
                    return

            #print("Data Antes, atualize")
            update_query, update_values  = dict_type[key_dictionary_db].update_query(dictionary, result)
            cursor.execute(update_query, update_values)
            print(f"UPDATE bem-sucedido na tabela de {key_dictionary_db}. De ID {dictionary[id]} no JSON")
                
        except Exception as e:
            print(f"Erro ao executar o UPDATE do elemento {dictionary[id]}: {e}")
        finally:
            connection.commit()
    else:
        try:
            insert_query, insert_values = dict_type[key_dictionary_db].insert_query(dictionary)
            cursor.execute(insert_query, insert_values)
            print(f"INSERT bem-sucedido na tabela de {key_dictionary_db}. De ID {dictionary[id]} no JSON")
        except Exception as e:
            print(f"Erro ao executar o INSERT do elemento {dictionary[id]}: {e}")
        finally:
            connection.commit()


def process_file_json(path_file_json):
    with open(path_file_json, 'r', encoding='utf-8') as arquivo_json:
        data_dict = json.load(arquivo_json)
            
    for dictionary in data_dict:
        db_execute(dictionary, path_file_json.split('/')[-1].split('_')[0])

    print(f'\n{len(data_dict)} elementos atualizado/inserido com SUCESSO')


if __name__ == "__main__": 
    json_directory = 'JSON/Falta/'
    cursor = connection.cursor()

    for file_name in os.listdir(json_directory):
        if file_name.endswith(".json"):
            caminho_arquivo = os.path.join(json_directory, file_name)
            process_file_json(caminho_arquivo)

    cursor.close()
    connection.close()
    print("FIM")




