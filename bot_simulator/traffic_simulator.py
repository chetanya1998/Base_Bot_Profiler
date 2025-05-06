import requests
import random
import time
from faker import Faker

fake = Faker()

# === Server Target ===
BASE_URL = "http://localhost:8000"

# === Endpoint Variants ===
NORMAL_PATHS = [
    "/",
    "/admin",
    "/login",
    "/cart",
    "/search?q=laptop",
    "/product/101"
]

TRAP_PATHS = [
    "/hidden",
    "/secret-api",
    "/wp-login",
    "/cms-admin"
]

# === User-Agent Pool ===
USER_AGENTS = [
    # Normal browsers
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)",
    # Crawlers and tools
    "Googlebot/2.1 (+http://www.google.com/bot.html)",
    "curl/7.68.0",
    "python-requests/2.25.1",
    "Bingbot/2.0 (+http://www.bing.com/bingbot.htm)"
]

def simulate_request():
    is_trap = random.random() < 0.25  # 25% trap traffic
    path = random.choice(TRAP_PATHS if is_trap else NORMAL_PATHS)
    full_url = f"{BASE_URL}{path}"

    headers = {
        "User-Agent": random.choice(USER_AGENTS),
        "X-Forwarded-For": fake.ipv4()
    }

    try:
        response = requests.get(full_url, headers=headers, timeout=2)
        print(f"[{response.status_code}] {headers['X-Forwarded-For']} -> {full_url}")
    except Exception as e:
        print(f"[ERROR] Request failed: {e}")

if __name__ == "__main__":
    print("🚀 Sending traffic to Advanced Dummy Server...")
    for _ in range(150):
        simulate_request()
        time.sleep(random.uniform(0.2, 0.5))  # adjustable delay
