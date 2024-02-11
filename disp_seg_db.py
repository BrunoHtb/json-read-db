from psycopg2 import sql

def select_query(dicionario):
    query = sql.SQL("SELECT * FROM public.tb_dispositivosdeseguranca WHERE auditoria = %s AND codigo = %s")
    values = (dicionario['auditoria'], dicionario['codigo'])
    return query, values

def insert_query(dicionario):
    colunas = ', '.join([coluna for coluna in dicionario.keys() if coluna != 'chave'])
    valores = ', '.join(['%s' for chave in dicionario.keys() if chave != 'chave'])
    
    insert_query = f"INSERT INTO public.tb_dispositivosdeseguranca ({colunas}) VALUES ({valores}) RETURNING chave;"
    return insert_query, tuple(valor for chave, valor in dicionario.items() if chave != 'chave')

def update_query(dicionario):
    set_clause = ', '.join([f"{chave} = %s" for chave in dicionario.keys()])
    
    update_query = f"UPDATE public.tb_dispositivosdeseguranca SET {set_clause} WHERE chave = %s;"
    return update_query, tuple(dicionario.values()) + (dicionario['chave'],)
