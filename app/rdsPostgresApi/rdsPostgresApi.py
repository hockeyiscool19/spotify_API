import pandas as pd
from sqlalchemy import create_engine, text
import os

# Database connection parameters
# Replace with your RDS endpoint
host = 'spotify.coacb9cwipmh.us-east-1.rds.amazonaws.com'
port = '5432'              # Replace with your RDS port
database = 'postgres'  # Replace with your database name
user = 'postgres'     # Replace with your database username
password = '4Hockeyiscold*'  # Replace with your database password


class RdsConnect:
    def __init__(self, host=host, database=database, user=user, password=password):
        self.host = host
        self.database = database
        self.user = user

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
