import pandas as pd
import psycopg2
from psycopg2 import sql
from datetime import datetime

# Database connection parameters
DB_PARAMS = {
    "dbname": "nids_db",
    "user": "postgres",
    "password": "Kamal123!",
    "host": "localhost",
    "port": "5432"
}

# Path to NSL-KDD dataset (update with your local path)
DATASET_PATH = "data/KDDTrain+.csv"

def create_table():
    """Create logs table in PostgreSQL."""
    try:
        conn = psycopg2.connect(**DB_PARAMS)
        cursor = conn.cursor()
        
        create_table_query = """
        CREATE TABLE IF NOT EXISTS logs (
            id SERIAL PRIMARY KEY,
            timestamp TIMESTAMP,
            src_ip VARCHAR(15),
            dst_ip VARCHAR(15),
            protocol VARCHAR(10),
            src_bytes INTEGER,
            label VARCHAR(20)
        );
        """
        cursor.execute(create_table_query)
        conn.commit()
        print("Table 'logs' created successfully.")
    except Exception as e:
        print(f"Error creating table: {e}")
    finally:
        cursor.close()
        conn.close()

def load_data():
    """Load NSL-KDD dataset into PostgreSQL."""
    # Read NSL-KDD dataset (subset of columns for simplicity)
    # Define all column names for NSL-KDD dataset (42 columns)
    columns = [
    "duration", "protocol_type", "service", "flag", "src_bytes", "dst_bytes", "land",
    "wrong_fragment", "urgent", "hot", "num_failed_logins", "logged_in", "num_compromised",
    "root_shell", "su_attempted", "num_root", "num_file_creations", "num_shells",
    "num_access_files", "num_outbound_cmds", "is_host_login", "is_guest_login", "count",
    "srv_count", "serror_rate", "srv_serror_rate", "rerror_rate", "srv_rerror_rate",
    "same_srv_rate", "diff_srv_rate", "srv_diff_host_rate", "dst_host_count",
    "dst_host_srv_count", "dst_host_same_srv_rate", "dst_host_diff_srv_rate",
    "dst_host_same_src_port_rate", "dst_host_srv_diff_host_rate", "dst_host_serror_rate",
    "dst_host_srv_serror_rate", "dst_host_rerror_rate", "dst_host_srv_rerror_rate", "class", "difficulty"
    ]
    # Read the dataset with no header and specified columns
    df = pd.read_csv(DATASET_PATH, names=columns, usecols=["duration", "protocol_type", "src_bytes", "dst_bytes", "class"], header=None)
    
    # Preprocess: Map labels (normal/anomaly), generate dummy IPs and timestamps
    df["label"] = df["class"].apply(lambda x: "normal" if x == "normal" else "anomaly")
    df["src_ip"] = ["192.168.1." + str(i % 255) for i in range(len(df))]
    df["dst_ip"] = ["10.0.0." + str(i % 255) for i in range(len(df))]
    df["timestamp"] = [datetime(2025, 1, 1) + pd.Timedelta(seconds=i) for i in range(len(df))]
    
    # Connect to database
    try:
        conn = psycopg2.connect(**DB_PARAMS)
        cursor = conn.cursor()
        
        # Insert data into logs table
        insert_query = sql.SQL("""
        INSERT INTO logs (timestamp, src_ip, dst_ip, protocol, src_bytes, label)
        VALUES (%s, %s, %s, %s, %s, %s)
        """)
        
        for _, row in df.iterrows():
            cursor.execute(insert_query, (
                row["timestamp"],
                row["src_ip"],
                row["dst_ip"],
                row["protocol_type"],
                row["src_bytes"],
                row["label"]
            ))
        
        conn.commit()
        print(f"Loaded {len(df)} records into 'logs' table.")
    except Exception as e:
        print(f"Error loading data: {e}")
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    create_table()
    load_data()