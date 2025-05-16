import pandas as pd
from db_connection import DatabaseConnection

def get_information_df():
    with DatabaseConnection('jeju.db') as (conn, cursor):
        df = pd.read_sql_query("SELECT * FROM Information", conn)
        return df

if __name__ == "__main__":
    df = get_information_df()
    print(df.head())
    print(df.columns.tolist())
