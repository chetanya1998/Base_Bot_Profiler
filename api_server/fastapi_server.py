from fastapi import FastAPI, Request
import os
import logging
from datetime import datetime

app = FastAPI()

# === Setup log directory and file ===
LOG_DIR = os.path.join("advanced_server", "logs")
LOG_FILE = os.path.join(LOG_DIR, "access.log")
os.makedirs(LOG_DIR, exist_ok=True)

# === Configure logging ===
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(message)s"
)

# === Middleware to log all requests ===
@app.middleware("http")
async def log_requests(request: Request, call_next):
    response = await call_next(request)
    
    log_line = f"{datetime.now()} | {request.client.host} | {request.headers.get('user-agent')} | {request.url.path} | {response.status_code} | {request.method}"
    logging.info(log_line)
    
    return response

# === Example Routes ===
@app.get("/")
async def root():
    return {"message": "Welcome to the Bot Profiler FastAPI Server"}

@app.get("/admin")
async def admin():
    return {"message": "Admin Page"}

@app.get("/dashboard")
async def dashboard():
    return {"message": "Dashboard"}

@app.get("/cms")
async def cms():
    return {"message": "CMS Page"}

@app.get("/search")
async def search(q: str = ""):
    return {"message": f"Search for: {q}"}
