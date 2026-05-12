"""Minimal test to check if FastAPI starts correctly on Render."""
import os
import sys

print(f"DEBUG: Python {sys.version}", flush=True)
print(f"DEBUG: CWD {os.getcwd()}", flush=True)
print(f"DEBUG: PORT {os.getenv('PORT', 'NOT SET')}", flush=True)
print(f"DEBUG: Files in CWD: {os.listdir('.')}", flush=True)

from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {"status": "ok", "debug": True}

@app.get("/api/health")
async def health():
    return {"status": "healthy"}

print(f"DEBUG: App created with {len(app.routes)} routes", flush=True)
