import pandas as pd
import os
import joblib
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import DBSCAN

INPUT_CSV = "../data_ingestion/outputs/session_features.csv"
MODEL_PATH = "models/clustering_model.pkl"
SCALER_PATH = "models/feature_scaler.pkl"

os.makedirs("models", exist_ok=True)

# === Load extracted features ===
df = pd.read_csv(INPUT_CSV)

# Drop IP, use only numerical columns
X = df.drop(columns=["ip"], errors="ignore").fillna(0)

# === Normalize features ===
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# === Apply clustering ===
model = DBSCAN(eps=1.2, min_samples=2)
labels = model.fit_predict(X_scaled)

# === Attach cluster labels and save
df["cluster"] = labels
df.to_csv(INPUT_CSV, index=False)

joblib.dump(model, MODEL_PATH)
joblib.dump(scaler, SCALER_PATH)

print(f"✅ Clustering model saved to: {MODEL_PATH}")
print(f"✅ Feature scaler saved to: {SCALER_PATH}")
print(f"✅ Labeled features saved to: {INPUT_CSV}")
