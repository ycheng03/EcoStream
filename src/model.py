import pandas as pd
import sqlite3
from sklearn.ensemble import IsolationForest
import joblib
import os

DB_PATH = os.path.join('data', 'pollution.db')
MODEL_PATH = os.path.join('data', 'model.pkl')

def train_model():
    if not os.path.exists(DB_PATH):
        print(f"Error: Database not found at {DB_PATH}. Run src/ingest.py first.")
        return

    # Load Data from SQL
    print("Loading data from SQL database...")
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql("SELECT * FROM sensors", conn)
    conn.close()
    
    # Setup features for training
    features = ['PM2.5', 'PM10', 'SO2', 'NO2', 'TEMP', 'PRES', 'DEWP']
    X = df[features]

    # Initialize Isolation Forest 
    # Assume 5% anomaly rate based on domain constraints
    print("Training Isolation Forest model (this may take a moment)...")
    model = IsolationForest(n_estimators=100, contamination=0.05, random_state=42)
    model.fit(X)

    # Save the model
    joblib.dump(model, MODEL_PATH)
    print(f"Model saved to {MODEL_PATH}")
    
    # Test
    df['anomaly'] = model.predict(X)
    anomalies = df[df['anomaly'] == -1]
    print(f"Success! Detected {len(anomalies)} anomalies in the dataset.")

if __name__ == "__main__":
    train_model()