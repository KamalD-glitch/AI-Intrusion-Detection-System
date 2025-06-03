from flask import Flask, render_template, jsonify
import pandas as pd
from sqlalchemy import create_engine
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import LabelEncoder
import numpy as np

# Flask app initialization
app = Flask(__name__)

# Create SQLAlchemy engine
DB_URL = "postgresql://postgres:Kamal123!@localhost:5432/nids_db"
engine = create_engine(DB_URL)

# Fix: Remove duplicate route definition for "/"
# The first index() function is correct; remove the second one
@app.route('/')
def index():
    """Render dashboard with initial data for the chart."""
    query = "SELECT src_ip, src_bytes, label FROM logs LIMIT 1000"
    df = pd.read_sql(query, engine)
    print("Initial chart data:", df.to_dict('records')[:5])  # Debug: Print first 5 records
    return render_template('index.html', chart_data=df.to_dict('records'))

# Load and train model
def train_model():
    """Train Isolation Forest model on NSL-KDD data."""
    try:
        # Use SQLAlchemy engine instead of psycopg2
        query = "SELECT src_bytes, protocol FROM logs"
        df = pd.read_sql(query, engine)
        
        # Debug: Check if data is retrieved
        print("Training data shape:", df.shape)
        print("Training data sample:", df.head().to_dict('records'))
        
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

@app.route("/predict")
def predict():
    """Fetch recent logs and predict anomalies."""
    try:
        query = "SELECT src_bytes, protocol, src_ip FROM logs ORDER BY timestamp DESC LIMIT 100"
        df = pd.read_sql(query, engine)
        
        # Debug: Check if data is retrieved
        print("Predict data shape:", df.shape)
        print("Predict data sample:", df.head().to_dict('records'))
        
        # Preprocess
        df["protocol"] = LE.transform(df["protocol"])
        X = df[["src_bytes", "protocol"]]
        
        # Predict (-1 for anomaly, 1 for normal)
        predictions = MODEL.predict(X)
        results = [
            {"src_ip": row.src_ip, "src_bytes": row.src_bytes, "is_anomaly": str(pred == -1).lower()}
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
        
        # Debug: Check the chart data being sent
        print("Chart data sent to frontend:", chart_data)
        
        return jsonify({"results": results, "chart_data": chart_data})
    except Exception as e:
        print(f"Error in predict endpoint: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)