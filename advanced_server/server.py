from fastapi import FastAPI, Request
import os
import logging
from datetime import datetime
import joblib
import pandas as pd
from sklearn.preprocessing import StandardScaler
import numpy as np

app = FastAPI()

# === Log Setup ===
LOG_DIR = os.path.join("advanced_server", "logs")
LOG_FILE = os.path.join(LOG_DIR, "access.log")
os.makedirs(LOG_DIR, exist_ok=True)

if not os.path.exists(LOG_FILE):
    open(LOG_FILE, "w").close()

logging.basicConfig(filename=LOG_FILE, level=logging.INFO, format="%(message)s")

# === ML Model Load ===
try:
    clustering_model = joblib.load("/models/clustering_model.pkl")
    feature_scaler = joblib.load("/models/feature_scaler.pkl")
    print("✅ ML model and scaler loaded.")
except Exception as e:
    print(f"❌ Failed to load model or scaler: {e}")
    clustering_model = None
    feature_scaler = None

# === Logging Middleware ===
@app.middleware("http")
async def log_requests(request: Request, call_next):
    response = await call_next(request)
    log_line = f"{datetime.now()} | {request.client.host} | {request.headers.get('user-agent')} | {request.url.path} | {response.status_code} | {request.method}"
    logging.info(log_line)
    return response

# === Dummy Endpoints ===
@app.get("/")
async def root():
    return {"message": "Advanced Dummy Server"}

@app.get("/login")
async def login():
    return {"message": "Login page"}

@app.get("/admin")
async def admin():
    return {"message": "Admin Panel"}

@app.get("/search")
async def search(q: str = ""):
    return {"query": q}

@app.get("/cart")
async def cart():
    return {"message": "Cart content"}

@app.get("/wp-login")
async def wp_login():
    return {"error": "Unauthorized access"}, 403

# === API: Profile Session (Example) ===
@app.post("/profile")
async def profile(session: dict):
    """
    Accepts a JSON with session-level features:
    {
        "total_hits": 12,
        "unique_paths": 5,
        "avg_interval": 1.4,
        "status_4xx": 1,
        "ua_entropy": 6.8
    }
    """
    if clustering_model is None or feature_scaler is None:
        return {"error": "Model not loaded"}

    try:
        X = pd.DataFrame([session])
        X_scaled = feature_scaler.transform(X)
        cluster = clustering_model.fit_predict(X_scaled)[0]
        return {"cluster": int(cluster)}
    except Exception as e:
        return {"error": str(e)}
