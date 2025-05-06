import os
import pandas as pd
import numpy as np

# === Setup paths ===
PARSED_LOGS = "../data_ingestion/outputs/parsed_logs.csv"
OUTPUT_CSV = "../data_ingestion/outputs/session_features.csv"
os.makedirs("outputs", exist_ok=True)

def extract_features(df):
    df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')
    df = df.dropna(subset=['timestamp', 'ip'])

    features = []
    for ip, group in df.groupby('ip'):
        group = group.sort_values('timestamp')
        session = {
            "ip": ip,
            "total_hits": len(group),
            "unique_paths": group['path'].nunique(),
            "avg_interval": group['timestamp'].diff().dt.total_seconds().mean() or 0,
            "status_4xx": group['status'].astype(str).str.startswith("4").sum(),
            "ua_entropy": group['user_agent'].apply(lambda ua: len(set(ua))).mean(),
        }
        features.append(session)

    return pd.DataFrame(features)

def main():
    if not os.path.exists(PARSED_LOGS):
        print(f"❌ Missing parsed logs file: {PARSED_LOGS}")
        return

    df_logs = pd.read_csv(PARSED_LOGS)
    if df_logs.empty:
        print("⚠️ Parsed logs file is empty.")
        return

    df_features = extract_features(df_logs)

    if df_features.empty:
        print("⚠️ No features extracted. Possibly no IP groupings available.")
        return

    df_features.to_csv(OUTPUT_CSV, index=False)
    print(f"✅ Session features saved to: {OUTPUT_CSV}")

if __name__ == "__main__":
    main()
