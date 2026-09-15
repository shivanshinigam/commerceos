"""
Launcher Script for Google UCP Backend Server
"""

import sys
import uvicorn
from seed_data import seed_catalog

if __name__ == "__main__":
    print("Seeding catalog database...")
    seed_catalog()
    print("\nStarting Google UCP 2026 Server on http://127.0.0.1:8000 ...")
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=False)
