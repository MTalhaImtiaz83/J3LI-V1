"""
J3LI Desktop Application Launcher
===================================
Double-click to start the J3LI Quranic Research System.
Serves both the API and the frontend on http://localhost:8000
"""

import os
import sys
import webbrowser
import threading
import time
from pathlib import Path

# Set up paths relative to this script
APP_DIR = Path(__file__).parent.resolve()
os.environ["PYTHONPATH"] = str(APP_DIR)
os.environ["J3LI_DATA_DIR"] = str(APP_DIR / "data")
sys.path.insert(0, str(APP_DIR))

# Now import after path is set
import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from j3li.api.main import app as api_app, lifespan

STATIC_DIR = APP_DIR / "frontend" / "out"
PORT = 8000


def create_app():
    """Create the combined app that serves API + static frontend."""
    # Mount the API routes on the existing app
    app = api_app

    # Serve static frontend files
    if STATIC_DIR.exists():
        # Serve Next.js static export
        @app.get("/graph")
        @app.get("/graph/")
        async def graph_page():
            return FileResponse(str(STATIC_DIR / "graph" / "index.html"))

        @app.get("/explorer")
        @app.get("/explorer/")
        async def explorer_page():
            return FileResponse(str(STATIC_DIR / "explorer" / "index.html"))

        # Mount static assets (JS, CSS, images)
        app.mount("/_next", StaticFiles(directory=str(STATIC_DIR / "_next")), name="next-static")

        # Serve index.html for the root (must be last to not override API routes)
        @app.get("/app")
        @app.get("/app/")
        async def home_page():
            return FileResponse(str(STATIC_DIR / "index.html"))

    return app


def open_browser():
    """Open the browser after a short delay to let the server start."""
    time.sleep(2)
    webbrowser.open(f"http://localhost:{PORT}/app")


def main():
    print()
    print("=" * 60)
    print("  J3LI — Just Three Like It")
    print("  Quranic Research System")
    print("=" * 60)
    print()
    print(f"  Data directory: {APP_DIR / 'data'}")
    print(f"  Frontend:       {STATIC_DIR}")
    print(f"  Server:         http://localhost:{PORT}")
    print(f"  App:            http://localhost:{PORT}/app")
    print(f"  API Docs:       http://localhost:{PORT}/docs")
    print()
    print("  Press Ctrl+C to stop the server.")
    print("=" * 60)
    print()

    app = create_app()

    # Open browser in background thread
    threading.Thread(target=open_browser, daemon=True).start()

    # Start uvicorn
    uvicorn.run(app, host="127.0.0.1", port=PORT, log_level="info")


if __name__ == "__main__":
    main()
