import os
import pandas as pd

LOG_FILE = "../logs/access.log"
OUTPUT_CSV = os.path.join("outputs", "parsed_logs.csv")

os.makedirs("outputs", exist_ok=True)

def parse_log_line(line):
    """
    Parses a single line of the log file into a dictionary
    Format expected:
    timestamp | ip | user_agent | path | status | method
    """
    try:
        parts = [p.strip() for p in line.split(" | ")]
        if len(parts) < 6:
            return None  # malformed

        return {
            "timestamp": parts[0],
            "ip": parts[1],
            "user_agent": parts[2],
            "path": parts[3],
            "status": parts[4],
            "method": parts[5],
        }
    except Exception as e:
        print(f"[ERROR] Failed to parse line: {line.strip()}\n{e}")
        return None

def parse_log_file(path):
    parsed = []
    with open(path, "r") as f:
        for line in f:
            parsed_line = parse_log_line(line)
            if parsed_line:
                parsed.append(parsed_line)
    
    df = pd.DataFrame(parsed)
    if not df.empty:
        df["timestamp"] = pd.to_datetime(df["timestamp"], errors='coerce')
        df.dropna(subset=["timestamp"], inplace=True)
    return df

if __name__ == "__main__":
    if not os.path.exists(LOG_FILE):
        print(f"❌ Log file not found: {LOG_FILE}")
    else:
        df_logs = parse_log_file(LOG_FILE)
        df_logs.to_csv(OUTPUT_CSV, index=False)
        print(f"✅ Parsed {len(df_logs)} entries to {OUTPUT_CSV}")
