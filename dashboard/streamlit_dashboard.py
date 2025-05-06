import streamlit as st
import pandas as pd
import numpy as np
import joblib
import matplotlib.pyplot as plt
import seaborn as sns
import os

from sklearn.preprocessing import StandardScaler

# === Page setup ===
st.set_page_config(page_title="Bot Behavior Profiler Dashboard", layout="wide")
st.title("🛡️ Bot Behavior Profiler Dashboard")
st.caption("Analyze bot and user sessions using unsupervised clustering")

# === Load model and scaler ===
model_path = "models/clustering_model.pkl"
scaler_path = "models/feature_scaler.pkl"

if not os.path.exists(model_path) or not os.path.exists(scaler_path):
    st.error("❌ Clustering model or scaler not found. Run generate_clustering_model.py first.")
    st.stop()

model = joblib.load(model_path)
scaler = joblib.load(scaler_path)

# === Feature extraction if raw logs uploaded ===
def extract_features_from_logs(df):
    df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')
    df = df.dropna(subset=['timestamp'])

    session_features = []
    for ip, group in df.groupby("ip"):
        group = group.sort_values("timestamp")
        feature = {
            "ip": ip,
            "total_hits": len(group),
            "unique_paths": group['path'].nunique(),
            "avg_interval": group['timestamp'].diff().dt.total_seconds().mean() or 0,
            "status_4xx": group['status'].astype(str).str.startswith("4").sum(),
            "ua_entropy": group['user_agent'].apply(lambda ua: len(set(ua))).mean()
        }
        session_features.append(feature)
    return pd.DataFrame(session_features)

# === Upload area ===
st.subheader("📂 Upload Session Data")
uploaded_file = st.file_uploader("Upload either `parsed_logs.csv` or `session_features.csv`", type="csv")

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    if "timestamp" in df.columns:
        st.info("🧠 Detected raw logs. Extracting session-level features...")
        df = extract_features_from_logs(df)
    else:
        st.success("🎯 Session-level features loaded successfully!")

    if df.empty:
        st.warning("Parsed session data is empty. Cannot continue.")
        st.stop()

    # Save IPs and scale numeric features
    ips = df["ip"]
    features = df.drop(columns=["ip"], errors="ignore").fillna(0)
    X_scaled = scaler.transform(features)

    # Predict clusters
    df["cluster"] = model.fit_predict(X_scaled)

    st.success(f"✅ Clustered {len(df)} sessions into {df['cluster'].nunique()} groups.")
    st.dataframe(df.head(10), use_container_width=True)

    # === Layout with columns ===
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 📊 Cluster Distribution")
        fig, ax = plt.subplots(figsize=(6, 4))
        sns.countplot(data=df, x="cluster", palette="Set2", ax=ax)
        ax.set_title("Session Count per Cluster")
        st.pyplot(fig, use_container_width=True)

    with col2:
        st.markdown("### 🌡️ Avg Features per Cluster")
        avg = df.drop(columns=["ip"], errors="ignore").groupby("cluster").mean(numeric_only=True)
        fig2, ax2 = plt.subplots(figsize=(6, 4))
        sns.heatmap(avg, cmap="YlGnBu", annot=True, fmt=".1f", linewidths=0.3, ax=ax2)
        ax2.set_title("Cluster Behavior Summary")
        st.pyplot(fig2, use_container_width=True)

    # === Expandable raw data section ===
    with st.expander("📎 Full Clustered Dataset"):
        st.dataframe(df, use_container_width=True)

    # === Download option ===
    st.download_button("📥 Download Labeled CSV", data=df.to_csv(index=False), file_name="labeled_sessions.csv", mime="text/csv")
