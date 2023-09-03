import pyodbc
import pandas as pd
import numpy as np 
import sqlalchemy
import logging 
from .utils import map_column_types 

class clientSql():
    def __init__(
        self,
        host:str,
        user:str,
        password:str,
        db_name:str
        ) -> None:

        logging.debug("Init MsSQL server instance")
        #credentials
        self.__host = host
        self.__user = user
        self.__password = password
        self.__database = db_name

    def get_engine(self):
        conn_string = 'DRIVER={SQL Server};SERVER='+self.__host+';DATABASE='+self.__database+';ENCRYPT=yes;UID='+self.__user+';PWD='+ self.__password
        logging.debug(f"pyodbc: {conn_string}")
        return pyodbc.connect('DRIVER={SQL Server};SERVER='+self.__host+';DATABASE='+self.__database+';ENCRYPT=yes;UID='+self.__user+';PWD='+ self.__password)
    
    def append_data_from_df(
        self,
        df:pd.DataFrame,
        table_name:str,
        schema:str,
        column_name_datetime:str='Fecha',
        chunk_size:int = 20
        ):

        # if hasattr(self,'sql_server') == False:
        #     self.__init_sql()
        
        logging.info(f">> Append data into {schema}.{table_name}")

        df.to_sql(
            con = self.get_pandas_engine(),
            name = table_name,
            schema = schema,
            if_exists = 'append',
            chunksize = chunk_size,
            index = False,
            method = 'multi'
            )

        logging.info(f">> Delete duplicated values {schema}.{table_name}")
        self.delete_duplicate_values_sql(
            schema=schema,
            table_name=table_name,
            column_name=column_name_datetime
        )

    def delete_duplicate_values_sql(
        self,
        schema:str,
        table_name:str,
        column_name:str or list,
        ):

        # if hasattr(self,'sql_server') == False:
        #     self.__init_sql()

        cursor = self.get_engine()

        if isinstance(column_name,str):
            query = f"""
                WITH cte AS (
                    SELECT 
                        *, 
                        ROW_NUMBER() OVER (
                            PARTITION BY [{column_name}]
                            ORDER BY [{column_name}]
                        )  [row_num]
                    FROM [{schema}].[{table_name}])
                DELETE FROM cte
                WHERE row_num>1
            """
        elif isinstance(column_name,list):
            col_string = ','.join(['['+col+']' for col in column_name])
            query = f"""
                WITH cte AS (
                    SELECT 
                        *, 
                        ROW_NUMBER() OVER (
                            PARTITION BY {col_string}
                            ORDER BY {col_string}
                        )  [row_num]
                    FROM [{schema}].[{table_name}])
                DELETE FROM cte
                WHERE row_num>1
            """
        cursor.execute(query)
        cursor.commit()
        cursor.close() 

    def get_pandas_engine(self):
        constring = f"mssql+pyodbc://{self.__user}:{self.__password}@{self.__host}/{self.__database}?driver=SQL+Server"
        logging.debug(f'get pandas connection {constring}')
        dbEngine = sqlalchemy.create_engine(constring, connect_args={'connect_timeout': 10}, echo=False)
        return dbEngine

    def read_with_pandas(self,query,**kwargs):
        return pd.read_sql(query,self.get_pandas_engine(),**kwargs)

    def execute_query(
        self,query:str
        ):
        cursor = self.get_engine()
        cursor.execute(query)
        cursor.commit()
        cursor.close() 

    #--- Feature on deploy ---#
    def exec_query(
        self,
        query,
        chunksize=1000
        ):
        """
        NO USE (on development)
        """
        column_name = None
        response = None
        try:
            conn = self.get_engine()
            with conn.cursor() as cur:
                #cur.itersize = chunksize
                cur.execute(query)
                if cur.description:
                    column_name = [desc[0] for desc in cur.description]
                    response = cur.fetchall()
                conn.commit()

        except (Exception) as e:
            print ('Error executing query: ',e)
            conn = None
        finally:
            if conn is not None:
                conn.close()
            if column_name is not None:
                try:
                    return pd.DataFrame(np.array(response),columns=column_name)
                except: 
                    return pd.DataFrame(columns=column_name)
    
    def create_staging_table(
        self,
        cursor,
        table_name:str, 
        schema:str='dbo',
        data_types=dict,
        column_types = {}
        ) -> None:

        query = f"""CREATE TEMPORARY TABLE IF NOT EXISTS {schema}.{table_name}
        ({','.join(map_column_types(data_types,column_types))});"""
        cursor.execute(query)
    
    def __execute_values(
        self,
        cursor,
        query:str):
        cursor.execute(query)

    def __set_values(
        self,
        values:list)->str:

        s = "('"+ "','".join(value for value in map(str,values)) + "')"
        return s.replace("'nan'","null")

    def insert (
        self,
        df, 
        table_name:str, 
        schema:str='dbo', 
        column_types = {}
        )->None:

        try:
            conn = self.get_engine()
            with conn.cursor() as cur:
                self.create_staging_table(
                    cur,
                    table_name=table_name,
                    schema=schema,
                    data_types=df.dtypes.to_dict(),
                    column_types=column_types
                    )
                
                if 'Unnamed: 0' in df.columns.tolist():
                    self.__execute_values(
                        cur,
                        f"INSERT INTO {schema}.{table_name} VALUES {','.join([self.__set_values(values) for values in df.values.tolist()])};"
                        )
                else:
                    self.__execute_values(
                        cur,
                        f"INSERT INTO {schema}.{table_name} VALUES {','.join([self.__set_values(values) for values in df.values.tolist()])};"
                        )
                conn.commit()

        except (Exception) as e:
            print ('Error while insert...',e)
            conn=None
            
        finally:
            if conn is not None:
                conn.close()
if __name__ == '__main__':
    pass