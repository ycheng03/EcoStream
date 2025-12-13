import pandas as pd
import sqlite3
import os

# Configuration
DATA_PATH = 'data/raw_data.csv'
DB_PATH = 'data/pollution.db'

def ingest_data():
    print(f"Loading data from {DATA_PATH}...")
    df = pd.read_csv(DATA_PATH)
    
    # Data Cleaning
    df['timestamp'] = pd.to_datetime(df[['year', 'month', 'day', 'hour']])
    
    # Select relevant columns
    cols = ['timestamp', 'PM2.5', 'PM10', 'SO2', 'NO2', 'TEMP', 'PRES', 'DEWP']
    df_clean = df[cols].dropna()  # Drop rows with missing values for now
    
    print(f"Data cleaned. Rows remaining: {len(df_clean)}")

    # Persist processed data to SQLite
    conn = sqlite3.connect(DB_PATH)
    df_clean.to_sql('sensors', conn, if_exists='replace', index=False)
    conn.close()
    print(f"Data successfully saved to {DB_PATH}")

if __name__ == "__main__":
    ingest_data()