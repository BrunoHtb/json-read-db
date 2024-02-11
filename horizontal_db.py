from psycopg2 import sql

def select_query(dicionario):
    query = sql.SQL('SELECT * FROM public.retro_horizontal WHERE "AUDITORIA" = %s AND "RODOVIA" = %s AND "KM"=%s AND "METROS"=%s AND "DATA"= %s' )
    values = (dicionario['AUDITORIA'], dicionario['RODOVIA'], str(dicionario['KM']), str(dicionario['METROS']), str(dicionario['DATA']))
    return query, values

def insert_query(dicionario):
    colunas = ', '.join([f'"{coluna}"' for coluna in dicionario.keys() if coluna != 'ID'])
    placeholders = ', '.join(['%s' for coluna in range(len(dicionario.keys())) if coluna != 'ID'])
    
    insert_query = f"INSERT INTO public.retro_horizontal ({colunas}) VALUES ({placeholders}) RETURNING chave;"
    return insert_query, tuple([valor for coluna, valor in dicionario.items() if coluna != 'ID'])

def update_query(dicionario):
    set_clause = ', '.join([f'"{coluna}" = %s' for coluna in dicionario.keys() if coluna != 'ID'])
    
    update_query = f"UPDATE public.retro_horizontal SET {set_clause} WHERE \"ID\" = %s;"
    return update_query, tuple([valor for coluna, valor in dicionario.items()] + [dicionario['ID']])