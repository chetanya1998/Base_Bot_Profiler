# data_ingestion/parse_logs.py
import pandas as pd

def load_logs(file_path):
    """
    Loads logs from a CSV file or raw access logs.
    Assumes CSV has [timestamp, ip, user_agent, path, status_code]
    """
    df = pd.read_csv(file_path)
    return df
