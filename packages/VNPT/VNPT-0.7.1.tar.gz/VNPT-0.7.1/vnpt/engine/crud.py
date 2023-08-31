from engine.__init__ import engine, Session
from sqlalchemy.sql.selectable import Select
from sqlalchemy.sql.dml import Insert,Update,Delete
import pandas as pd
import traceback
from typing import List,Union
import json

def query2df(stmt:Select)->pd.DataFrame:
    try:
        with engine.connect() as conn:
            result = conn.execute(stmt)
            rows = result.fetchall()
            df = pd.DataFrame(rows, columns=result.keys())
            return df
    except:
        traceback.print_exc()
        
def query_fisrt(stmt:Select):
    try:
        return query2list(stmt)[0]
    except:
        traceback.print_exc()
        
def query2list(stmt:Select):
    try:
        df = query2df(stmt)
        return json.loads(df.to_json(orient='records', force_ascii=False))
    except:
        traceback.print_exc()
        
def query2tuples(stmt:Select)->List:
    try:
        with Session() as session:
            result = session.execute(stmt)
            rows = result.fetchall()
            return rows
    except:
        traceback.print_exc()
        
def execute(stmt:Union[Insert,Update,Delete], commit:bool=False)->int:
    try:
        with engine.connect() as conn:
            result = conn.execute(stmt)
            if commit:
                conn.commit()
            return result.rowcount
    except:
        traceback.print_exc()
        return -1
    