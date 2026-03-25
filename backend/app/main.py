from __future__ import annotations

import os
from typing import Any

from fastapi import FastAPI

APP_NAME = os.getenv("APP_NAME", "backend")
APP_ENV = os.getenv("APP_ENV", "local")
APP_VERSION = os.getenv("APP_VERSION", "0.1.0")
GREETING = os.getenv("GREETING", "Hello from backend")
API_TOKEN = os.getenv("API_TOKEN")

app = FastAPI(title=APP_NAME, version=APP_VERSION)


@app.get("/")
def root() -> dict[str, Any]:
    return {
        "name": APP_NAME,
        "env": APP_ENV,
        "version": APP_VERSION,
        "message": GREETING,
        "has_api_token": API_TOKEN is not None,
    }


@app.get("/healthz")
def healthz() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/readyz")
def readyz() -> dict[str, str]:
    return {"status": "ready"}


@app.get("/startupz")
def startupz() -> dict[str, str]:
    return {"status": "started"}
