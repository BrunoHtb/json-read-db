from psycopg2 import sql

def select_query(dictionary):
    query = sql.SQL("SELECT * FROM public.tb_dispositivosdeseguranca WHERE auditoria = %s AND codigo = %s")
    values = (dictionary['auditoria'], dictionary['codigo'])
    return query, values

def insert_query(dictionary):
    columns = ', '.join([coluna for coluna in dictionary.keys() if coluna != 'chave'])
    values = ', '.join(['%s' for key in dictionary.keys() if key != 'chave'])   
    insert_query = f"INSERT INTO public.tb_dispositivosdeseguranca ({columns}) VALUES ({values}) RETURNING chave;"
    
    return insert_query, tuple(value for key, value in dictionary.items() if key != 'chave')

def update_query(dictionary, result):
    set_clause = ', '.join([f"{key} = %s" for key in dictionary.keys()])
    update_query = f"UPDATE public.tb_dispositivosdeseguranca SET {set_clause} WHERE auditoria = %s AND codigo = %s"

    return update_query, tuple(dictionary.values()) + (dictionary['auditoria'], dictionary['codigo'])
