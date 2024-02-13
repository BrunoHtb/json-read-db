from psycopg2 import sql

def select_query(dictionary):
    query = sql.SQL('SELECT * FROM public.retro_vertical WHERE "AUDITORIA" = %s AND "RODOVIA" = %s AND "KM"=%s AND "METROS"=%s AND "DATA"= %s' )
    values = (dictionary['AUDITORIA'], dictionary['RODOVIA'], str(dictionary['KM']), str(dictionary['METROS']), str(dictionary['DATA']))
    return query, values

def insert_query(dictionary):
    integer_columns = ["AUDITORIA", "KM_I", "METRO_I", "ID_USUARIO"]
    columns = ', '.join([f'"{column}"' for column in dictionary.keys() if column != 'ID'])
    placeholders = ', '.join(['%s' for _ in range(len(dictionary)-1)])
    values = []

    for column, value in list(dictionary.items())[1:]: 
        if column in integer_columns and value is not None:
            values.append(int(value))
        else:
            values.append('' if value is None else value)

    values = ['' if value is None else value for value in values]
    insert_query = f"INSERT INTO public.retro_vertical ({columns}) VALUES ({placeholders});" 

    return insert_query, tuple(values)

def update_query(dictionary, result):
    integer_columns = ["AUDITORIA", "KM_I", "METRO_I", "ID_USUARIO"]
    set_clause = ', '.join([f'"{column}" = %s' for column in dictionary.keys() if column != 'ID'])
    values = []

    for column, value in list(dictionary.items())[1:]:
        if column in integer_columns and value is not None:
            values.append(int(value))
        else:
            values.append('' if value is None else value)

    where_condition = '"ID"=%s'   
    update_query = f'UPDATE public.retro_vertical SET {set_clause} WHERE {where_condition}' 
    where_values = [result[0]]

    return update_query, tuple(values + where_values)
