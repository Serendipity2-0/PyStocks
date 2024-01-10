import os
import sqlite3
import pandas as pd

def create_sqlite_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(f'Successfully connected to SQLite database: {db_file}')
        return conn
    except sqlite3.Error as e:
        print(f"Error connecting to SQLite database: {e}")
    return conn

def create_table(conn, symbol):
    try:
        c = conn.cursor()
        c.execute(f'''
            CREATE TABLE IF NOT EXISTS {symbol} (
                Date TEXT PRIMARY KEY,
                Open REAL,
                High REAL,
                Low REAL,
                Close REAL,
                Volume INTEGER
            )
        ''')
        print(f'Table created for symbol: {symbol}')
    except sqlite3.Error as e:
        print(f"Error creating table: {e}")

def insert_data_to_table(conn, symbol, csv_file):
    try:
        df = pd.read_csv(csv_file)
        df['Date'] = pd.to_datetime(df['Date'])
        df.set_index('Date', inplace=True)
        df.to_sql(symbol, conn, if_exists='replace')
        print(f'Data inserted into table: {symbol}')
    except sqlite3.Error as e:
        print(f"Error inserting data into table: {e}")

def main():
    # Directory containing the CSV files
    csv_directory = 'C:\\Users\\phchi\\Desktop\\python mine\\Backtesting\\PyStocks'


    # SQLite database file
    sqlite_db = 'stock_data.db'

    # Connect to SQLite database
    connection = create_sqlite_connection(sqlite_db)

    if connection:
        # List all CSV files in the directory
        csv_files = os.listdir(csv_directory)

        for file in csv_files:
            if file.endswith('.csv'):
                symbol = os.path.splitext(file)[0]  # Extract symbol from file name without extension
                create_table(connection, symbol)
                insert_data_to_table(connection, symbol, os.path.join(csv_directory, file))

        connection.close()
