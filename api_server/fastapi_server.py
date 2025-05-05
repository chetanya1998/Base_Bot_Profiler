# api_server/fastapi_server.py
from fastapi import FastAPI
import joblib
import pandas as pd
from scoring.threat_score import calculate_threat_score

app = FastAPI()
model = joblib.load('models/clustering_model.pkl')

@app.post("/detect_bot/")
async def detect_bot(hit_rate: float, unique_paths: int, avg_interval: float, ua_entropy: float):
    data = pd.DataFrame([{
        'hit_rate': hit_rate,
        'unique_paths': unique_paths,
        'avg_interval': avg_interval,
        'ua_entropy': ua_entropy
    }])
    
    cluster = model.fit_predict(data)
    threat = calculate_threat_score(data.iloc[0])
    
    return {"cluster": int(cluster[0]), "threat_score": float(threat)}
