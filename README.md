# AI-Intrusion-Detection-System

An AI-powered Network Intrusion Detection System (NIDS) built using the NSL-KDD dataset, featuring a Flask-based web dashboard for anomaly detection and visualization.

## Overview

This project provides a Network Intrusion Detection System (NIDS) that leverages machine learning to identify anomalies in network traffic. Key functionalities include:

- Loading the NSL-KDD dataset into a PostgreSQL database for efficient storage and querying.
- Detecting anomalies using an Isolation Forest model trained on network features.
- Visualizing results through an interactive web dashboard with a scatter chart.
- Displaying recent predictions in a user-friendly list format.

## Features

- **Anomaly Detection**: Utilizes an Isolation Forest model to identify unusual network patterns based on features like `src_bytes` and `protocol`.
- **Interactive Visualization**: Displays a scatter chart where:
  - X-axis represents the last octet of source IPs.
  - Y-axis represents source bytes.
  - Blue dots indicate normal traffic, while red dots highlight anomalies.
- **Database Integration**: Stores network logs in PostgreSQL for efficient data management.
- **Recent Predictions**: Shows the latest 100 log entries with their anomaly status in a list.

## Prerequisites

To run this project, ensure you have the following installed:

- Python 3.9 or higher
- PostgreSQL (create a database named `nids_db` with user `postgres` and a password of your choice)
- Required Python libraries: `pandas`, `psycopg2-binary`, `scikit-learn`, `flask`, `sqlalchemy`
  - Install them using:
```cmd
pip install pandas psycopg2-binary scikit-learn flask sqlalchemy
```
- NSL-KDD dataset (`KDDTrain+.csv`), available on [Kaggle](https://www.kaggle.com/datasets/hassan06/nslkdd)

### Notes on Prerequisites

- **Use of `sqlalchemy`**:
- The project uses `SQLAlchemy` for database interactions instead of `psycopg2` alone. This choice was made to ensure better compatibility with `pandas` (avoiding warnings when using `pandas.read_sql`), provide a more modern database interaction approach, and maintain consistent engine usage throughout the application.

## Setup Instructions

Follow these steps to set up and run the project on your local machine:

1. **Clone the Repository**
```cmd
git clone https://github.com/your-username/AI-Intrusion-Detection-System.git
cd AI-Intrusion-Detection-System
```
2. **Set Up a Virtual Environment and Install Dependencies**:
```cmd
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```
Note: Ensure you have a `requirements.txt` file with the following content:
pandas
psycopg2-binary
scikit-learn
flask
sqlalchemy

3. **Configure PostgreSQL**:
- Create a database named `nids_db`:
```cmd
CREATE DATABASE nids_db;
```
- Update the database connection in `app.py` and `load_nslkdd_to_postgres.py` with your PostgreSQL credentials (e.g., username `postgres`, password).
4. **Load the NSL-KDD Dataset**:
- Download `KDDTrain+.csv` from Kaggle and place it in the `data/` directory (create the directory if it doesn’t exist).
- Update `load_nslkdd_to_postgres.py` with the path to `KDDTrain+.csv`.
- Run the script to load the data into PostgreSQL:
```cmd
python load_nslkdd_to_postgres.py
```
- Verify the data load by checking the row count:
```cmd
SELECT COUNT(*) FROM logs;
```
(Expected: 125,973 rows)
5. **Run the Flask Application**:
```cmd
python app.py
```
6. **Access the Dashboard**:
- Open your browser and navigate to `http://127.0.0.1:5000/` to view the dashboard.

## Usage

Once the application is running, you can interact with the NIDS through the web dashboard:

- **Scatter Chart**:
- The chart visualizes network traffic:
 - **X-axis**: Last octet of the source IP (e.g., 0 to 254).
 - **Y-axis**: Source bytes (e.g., 151, 2231).
 - **Blue Dots**: Represent normal traffic.
 - **Red Dots**: Indicate detected anomalies.
- **Recent Predictions**:
- Below the chart, a list displays the latest 100 log entries, showing:
 - Source IP (e.g., `192.168.1.2`).
 - Source bytes (e.g., `151`).
 - Anomaly status (e.g., `true` for anomalies, `false` for normal traffic).

## Project Structure

- `app.py`: Main Flask application with the `/predict` endpoint and Isolation Forest model for anomaly detection.
- `load_nslkdd_to_postgres.py`: Script to load the NSL-KDD dataset into the PostgreSQL database.
- `templates/index.html`: HTML template for the dashboard, using Chart.js for visualization.
- `instructions.txt`: Original setup instructions (for reference).
- `requirements.txt`: List of required Python dependencies.

## Contributions

Contributions are welcome! Feel free to:

- Fork the repository.
- Submit pull requests with improvements or bug fixes.
- Report issues or suggest new features via the GitHub Issues tab.

## License

See the MIT License file for details.

## Acknowledgements

- The NSL-KDD dataset is sourced from [Kaggle](https://www.kaggle.com/datasets/hassan06/nslkdd).
- Project inspired by a plan dated May 22, 2025.
