'''
A tool on python for CRUD of mssql 
'''
import pymssql 
import pandas as pd
import gc
import traceback

class DbConnection():
    def __init__(self, server, user, pwd, db):
        self.server = server
        self.user = user
        self.pwd = pwd
        self.db = db
        
    @property
    def conn(self):
        '''
        get the connection instance of the database
        '''
        try:
            ins = pymssql.connect(
                **{
                    "server": self.server,
                    "user": self.user,
                    "password": self.pwd,
                    "database": self.db
                }
            )
            return ins
        except Exception as e:
            traceback.print_exc()
    
    def query2df(self, sql_str, params:dict=None)->pd.DataFrame:
        try:
            conn = self.conn
            cursor = conn.cursor()
            cursor.execute(sql_str, params)
            # query
            columns = [column[0] for column in cursor.description]
            df = pd.DataFrame(cursor.fetchall(),columns=columns)
            cursor.close()
            conn.close()

            # clear cache
            del conn
            del cursor
            gc.collect()
            
            return df
        except Exception as e:
            traceback.print_exc()

    def execute(self, sql_str, params)->int:
        count = -1
        try:
            conn = self.conn
            cursor = conn.cursor()
            cursor.execute(sql_str, params)
            count = cursor.rowcount
            conn.commit()
            
            # clear cache
            cursor.close()
            conn.close()
            del conn
            del cursor
            gc.collect()
        except Exception as e:
            traceback.print_exc()
        finally:
            return count
        
    