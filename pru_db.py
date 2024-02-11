from psycopg2 import sql

def select_query(dicionario):
    query = sql.SQL("SELECT * FROM public.tb_restricaodeultrapassagem WHERE auditoria = %s AND codigo_1 = %s")
    values = (dicionario['auditoria'], dicionario['codigo_1'])
    return query, values

def insert_query(dicionario):
    colunas = ', '.join(dicionario.keys())
    valores = ', '.join(['%s' for _ in dicionario.values()])
    
    insert_query = f"INSERT INTO public.tb_restricaodeultrapassagem ({colunas}) VALUES ({valores});"
    return insert_query, tuple(dicionario.values())

def update_query(dicionario):
    set_clause = ', '.join([f"{chave} = %s" for chave in dicionario.keys()])
    
    update_query = f"UPDATE public.tb_restricaodeultrapassagem SET {set_clause} WHERE ru_id = %s;"
    return update_query, tuple(dicionario.values()) + (dicionario['ru_id'],)
