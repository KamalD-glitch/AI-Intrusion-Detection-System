from flask import Flask, render_template, jsonify
import pandas as pd
import psycopg2
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import LabelEncoder
import numpy as np

# Flask app initialization
app = Flask(__name__)

# Database connection parameters
DB_PARAMS = {
    "dbname": "nids_db",
    "user": "postgres",
    "password": "K1am2tf4214!",
    "host": "localhost",
    "port": "5432"
}

# Load and train model
def train_model():
    """Train Isolation Forest model on NSL-KDD data."""
    try:
        conn = psycopg2.connect(**DB_PARAMS)
        query = "SELECT src_bytes, protocol FROM logs"
        df = pd.read_sql(query, conn)
        conn.close()
        
        # Preprocess: Encode protocol
        le = LabelEncoder()
        df["protocol"] = le.fit_transform(df["protocol"])
        
        # Train Isolation Forest
        model = IsolationForest(contamination=0.1, random_state=42)
        X = df[["src_bytes", "protocol"]]
        model.fit(X)
        return model, le
    except Exception as e:
        print(f"Error training model: {e}")
        return None, None

MODEL, LE = train_model()

@app.route("/")
def index():
    """Render dashboard."""
    return render_template("index.html")

@app.route("/predict")
def predict():
    """Fetch recent logs and predict anomalies."""
    try:
        conn = psycopg2.connect(**DB_PARAMS)
        query = "SELECT src_bytes, protocol, src_ip FROM logs ORDER BY timestamp DESC LIMIT 100"
        df = pd.read_sql(query, conn)
        conn.close()
        
        # Preprocess
        df["protocol"] = LE.transform(df["protocol"])
        X = df[["src_bytes", "protocol"]]
        
        # Predict (-1 for anomaly, 1 for normal)
        predictions = MODEL.predict(X)
        results = [
            {"src_ip": row["src_ip"], "src_bytes": row["src_bytes"], "is_anomaly": pred == -1}
            for _, row, pred in zip(range(len(df)), df.itertuples(), predictions)
        ]
        
        # Prepare data for Chart.js
        chart_data = {
            "labels": df["src_ip"].tolist(),
            "datasets": [
                {
                    "label": "Source Bytes",
                    "data": [
                        {"x": row["src_ip"], "y": row["src_bytes"]}
                        for _, row in df.iterrows()
                    ],
                    "backgroundColor": [
                        "#FF6384" if pred == -1 else "#36A2EB"
                        for pred in predictions
                    ]
                }
            ]
        }
        
        return jsonify({"results": results, "chart_data": chart_data})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)