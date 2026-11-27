import subprocess
import time
import os
import sys
import urllib.request

CHROME_PATH = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
FRONTEND_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "frontend"))
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SCREENSHOTS_DIR = os.path.join(BASE_DIR, "docs", "screenshots")

PAGES = [
    ("/", "dashboard_overview.png"),
    ("/startups", "startups_directory.png"),
    ("/products", "products_comparison.png"),
    ("/research", "research_intelligence.png"),
    ("/jobs", "jobs_opportunities.png"),
    ("/news", "news_signals.png"),
    ("/entities", "entity_graph.png"),
    ("/trends", "trend_signals.png"),
    ("/quality", "data_quality.png"),
    ("/ingestion", "ingestion_monitor.png"),
    ("/reports", "reports_exports.png"),
]

def wait_for_url(url, timeout=30):
    start = time.time()
    while time.time() - start < timeout:
        try:
            with urllib.request.urlopen(url, timeout=2) as response:
                if response.status == 200:
                    return True
        except Exception:
            pass
        time.sleep(1)
    return False

def main():
    os.makedirs(SCREENSHOTS_DIR, exist_ok=True)
    print("Starting FastAPI backend on port 8000...")
    backend = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "src.main:app", "--host", "127.0.0.1", "--port", "8000"],
        cwd=BASE_DIR,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    print("Starting Next.js frontend on port 3000...")
    frontend = subprocess.Popen(
        "npm run start",
        cwd=FRONTEND_DIR,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    try:
        print("Waiting for backend (http://127.0.0.1:8000/api/v1/health)...")
        if not wait_for_url("http://127.0.0.1:8000/api/v1/health", 25):
            raise RuntimeError("Backend failed to start in time.")
        print("Backend ready.")

        print("Waiting for frontend (http://localhost:3000)...")
        if not wait_for_url("http://localhost:3000", 30):
            raise RuntimeError("Frontend failed to start in time.")
        print("Frontend ready.")

        # Let the frontend settle
        time.sleep(2)

        for route, filename in PAGES:
            target_url = f"http://localhost:3000{route}"
            out_path = os.path.join(SCREENSHOTS_DIR, filename)
            print(f"Capturing screenshot: {target_url} -> {filename}")
            
            cmd = [
                CHROME_PATH,
                "--headless=new",
                "--window-size=1920,1080",
                "--virtual-time-budget=6000",
                "--hide-scrollbars",
                f"--screenshot={out_path}",
                target_url
            ]
            res = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            if os.path.exists(out_path) and os.path.getsize(out_path) > 1000:
                print(f"  [OK] Saved {filename} ({os.path.getsize(out_path):,} bytes)")
            else:
                print(f"  [WARN] Failed to capture {filename} or empty. Output: {res.stderr}")

    finally:
        print("Stopping servers...")
        try:
            backend.terminate()
            backend.wait(timeout=3)
        except Exception:
            backend.kill()

        try:
            # Kill frontend process tree
            subprocess.run(["taskkill", "/F", "/T", "/PID", str(frontend.pid)], capture_output=True)
        except Exception:
            pass
        print("Cleanup complete.")

if __name__ == "__main__":
    main()
