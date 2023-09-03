def map_type(var):
    numpy_to_psql = {
        'int64' :'INT',
        'object':'TEXT',
        'float64':'NUMERIC',
        'bool': 'BOOLEAN',
        'datetime64[ns]':'DATETIME',
        '<M8[ns]':'DATETIME',
        'timedelta[ns]':'NUMERIC',
        }
    if var.name in numpy_to_psql.keys():
        return numpy_to_psql[var.name]
    else:
        return 'TEXT'

def map_column_types(data_types: dict,column_type={}):
    result=[]
    for key,value in data_types.items():
        if key=='Unnamed: 0':
            pass
        else:
            if key in list(column_type.keys()):
                result.append(f'{key}  {column_type[key]}')
            else:
                result.append(f'{key}  {map_type(value)}')

    return result


###########################################################################################################

# import os
# from os.path import join, dirname
# from dotenv import load_dotenv
# import logging
# from .sql_server import clientSql as SqlClient

# def get_credentials(env_file:str='db.env'):
#     """
#     """

#     dotenv_path = join(dirname(__file__), env_file)
#     load_dotenv(dotenv_path)
    
#     return {
#         'HOST_DB' : os.environ.get('SQL_HOST'),
#         'NAME_DB' : os.environ.get('SQL_DATABASE'),
#         'USER_DB' : os.environ.get("SQL_USERNAME"),
#         'PASSWORD_DB' : os.environ.get("SQL_PASSWORD"),
#     }



# def init_sql()->SqlClient:
#     logging.info("Init sql client")
#     keys_sql = get_credentials()
#     return SqlClient(
#                 host=keys_sql['HOST_DB'],
#                 db_name=keys_sql['NAME_DB'],
#                 user=keys_sql['USER_DB'],
#                 password=keys_sql['PASSWORD_DB']
#                 )