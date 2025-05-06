# 🛡️ Base Bot Profiler 🤖  
A modular, end-to-end lab for **simulating, logging, classifying, and visualising web-traffic bots** in real time.  
The project ships with a dummy FastAPI server, a traffic-simulator that generates diverse bot & human requests, a feature-extraction / ML pipeline, and an optional Streamlit (or CLI) dashboard.

---

## Table of Contents
1. [Why Bot Profiling Matters](#why-bot-profiling-matters)
2. [Project Highlights](#project-highlights)
3. [Folder Structure](#folder-structure)
4. [Quick Start](#quick-start)
5. [Detailed Step-by-Step Guide](#detailed-step-by-step-guide)
6. [How the Pipeline Works](#how-the-pipeline-works)
7. [Significance Across Sectors](#significance-across-sectors)
8. [Roadmap](#roadmap)
9. [Contributing](#contributing) & [License](#license)

---

## Why Bot Profiling Matters
Bad bots inflate ad spend, scrape competitive data, skew analytics, and execute credential-stuffing attacks. **Accurate, real-time detection** preserves revenue, trust, and security across digital assets.

---

## Project Highlights
| Layer | Tech | What It Does |
|-------|------|--------------|
| **Server** | FastAPI | Dummy endpoint that **logs every hit** (IP, UA, path, timestamp) to `advanced_server/logs/access.log`. |
| **Simulator** | Python (async / aiohttp) | Generates configurable mixes of *organic*, *spam*, and *advanced bot* traffic (randomised IP geos, user-agents, crawl pace). |
| **Feature Engine** | pandas, scikit-learn | Parses logs → session-level features (`total_hits`, `avg_interval`, `ua_entropy`, …). |
| **Models** | Logistic Regression, Random Forest, Isolation Forest (default) + plug-in interface for any ML/DL model. |
| **Dashboard** | Streamlit (or CLI fallback) | Live charts: traffic counters, bot-vs-human trend line, heat-map of cluster IDs, table of blocked IPs. |

---

## Folder Structure
base_bot_profiler/
│
├─ advanced_server/ # FastAPI app + logging middleware
│ ├─ app.py
│ └─ logs/access.log
│
├─ traffic_simulator/
│ └─ traffic_simulator.py
│
├─ parser/
│ ├─ parse_logs.py
│ └─ extract_features.py
│
├─ models/
│ ├─ clustering.pkl # unsupervised UMAP+HDBSCAN pipeline
│ ├─ logistic_model.pkl
│ ├─ rf_model.pkl
│ └─ isolation_forest.pkl
│
├─ dashboard/
│ ├─ live_log_monitor.py # Streamlit UI
│ └─ live_log_cli.py # CLI-only alternative
│
├─ requirements.txt
└─ README.md ← (you are here)


---

## Quick Start
```bash
# 0.  Clone & enter repo
git clone https://github.com/<you>/base_bot_profiler.git
cd base_bot_profiler

# 1.  Create & activate virtual-env
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate

# 2.  Install dependencies
pip install -r requirements.txt

# 3.  ⚡ Launch FastAPI server
uvicorn advanced_server.app:app --reload --port 8000

# 4.  🚦 Start traffic simulator in a new shell
python traffic_simulator/traffic_simulator.py --rate 50 --bots 0.4 --humans 0.6

# 5.  🏗️  Build / retrain models (optional)
python parser/extract_features.py --train-all

# 6.  👁️  Visualise (pick one)
streamlit run dashboard/live_log_monitor.py               # full GUI
python dashboard/live_log_cli.py --tail --interval 5      # lightweight CLI
