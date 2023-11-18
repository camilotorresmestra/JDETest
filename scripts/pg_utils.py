import pandas as pd
import os
import sqlalchemy
from psycopg2 import connect, sql, DatabaseError
import dotenv
from pathlib import Path

# load the environment variables
dotenv.load_dotenv('configs/db_creds.env')
# Now you can access the variables using os.getenv
db_user = os.getenv('db_user')
db_host = os.getenv('db_host')
db_name = os.getenv('db_name')
db_password = os.getenv('db_password')
db_port = os.getenv('db_port')

# create a connection string to connect to the database
CONN = connect(
                host=db_host, 
                database=db_name, 
                user=db_user,
                password=db_password, 
                port=db_port
            )
ENGINE = sqlalchemy.create_engine(f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}")

def query_to_df(query, conn = CONN):
    # execute the query using pandas
    df = pd.read_sql(query, conn)
    return df

def insert_to_db(df, table_name, schema, conn = ENGINE):
    try:
        df.to_sql(name = table_name, con= conn,schema=schema,if_exists="append")
    except DatabaseError as e:
        print(e)
        return False
    else:
        return True


