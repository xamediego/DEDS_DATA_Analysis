import pandas as pd
import sqlalchemy as sa
import pyodbc


def save_to_sql_server(df, table_name, server_name, database_name, username, password):
    conn_str = f"mssql+pymssql://{username}:{password}@{server_name}/{database_name}"
    engine = sa.create_engine(conn_str)

    df.to_sql(table_name, engine, if_exists='append', index=False)


def save_to_sql_server_tr(df, table_name, server_name, database_name, trusted_connection, primary_key):
    if trusted_connection:
        conn_str = f"DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server_name};DATABASE={database_name};Trusted_Connection=yes;"
    else:
        conn_str = f"DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server_name};DATABASE={database_name};"

    engine = sa.create_engine(f"mssql+pyodbc:///?odbc_connect={conn_str}")

    df.to_sql(table_name, engine, if_exists='append', index_label=primary_key)
