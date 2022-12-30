# loading in modules
import sqlite3
import pandas as pd
import os


def to_csv(database: str):
    db = sqlite3.connect(database=database)
    cursor = db.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    if not os.path.exists('./tables/'):
        os.makedirs('./tables/')
    for table_name in tables:
        table_name = table_name[0]
        table = pd.read_sql_query("SELECT * from %s" % table_name, db)
        table.to_csv(f'./tables/{table_name}.csv')
    cursor.close()
    db.close()


def to_parquet(database: str):
    db = sqlite3.connect(database=database)
    cursor = db.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    if not os.path.exists('./parquet/'):
        os.makedirs('./parquet/')
    for table_name in tables:
        table_name = table_name[0]
        table = pd.read_sql_query("SELECT * from %s" % table_name, db)
        table.to_parquet(f'./parquet/{table_name}.parq')
    cursor.close()
    db.close()


def main(database: str):
    to_csv(database=database)
    to_parquet(database=database)


if __name__ == "__main__":
    main(database="./latest.db")
