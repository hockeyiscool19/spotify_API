import pandas as pd
from sqlalchemy import create_engine, text
import os


class RdsConnect:
    def __init__(self):
        conn_string = os.system("POSTGRES_URI")
        self.engine = create_engine(conn_string)
        self.conn = self.engine.connect()

    def execute(self, query):
        return pd.read_sql_query(text(query), con=self.conn)

    def write_df(self, df: pd.DataFrame, schema, name, if_exists):
        """if_exists: ['fail', 'replace', 'append']"""
        df.to_sql(name, self.conn, schema, index=True, if_exists=if_exists)
        print(f"Wrote {name} to {self.database}.{schema}")

    def end(self):
        self.conn.close()

