from psycopg2 import sql

def select_query(dictionary):
    query = sql.SQL("SELECT * FROM public.tb_restricaodeultrapassagem WHERE auditoria = %s AND codigo_1 = %s")
    values = (dictionary['auditoria'], dictionary['codigo_1'])
    return query, values

def insert_query(dictionary):
    columns = ', '.join(dictionary.keys())
    values = ', '.join(['%s' for _ in dictionary.values()])
    insert_query = f"INSERT INTO public.tb_restricaodeultrapassagem ({columns}) VALUES ({values});"
    
    return insert_query, tuple(dictionary.values())

def update_query(dictionary, result):
    set_clause = ', '.join([f"{key} = %s" for key in dictionary.keys()])
    update_query = f"UPDATE public.tb_restricaodeultrapassagem SET {set_clause} WHERE auditoria = %s AND codigo_1 = %s;"

    return update_query, tuple(dictionary.values()) + (dictionary['auditoria'], dictionary['codigo_1'])
