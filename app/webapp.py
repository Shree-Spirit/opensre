from __future__ import annotations

import os
from pydantic import BaseModel
from fastapi import FastAPI, Header, HTTPException
from app.integrations.telegram import send_message

app = FastAPI()


class Alert(BaseModel):
    service: str
    severity: str
    message: str


def verify_api_key(x_api_key: str | None):
    api_key = os.getenv("ALERT_API_KEY")

    if not api_key:
        raise HTTPException(
            status_code=500,
            detail="Server misconfigured: ALERT_API_KEY not set",
        )

    if not x_api_key or x_api_key != api_key:
        raise HTTPException(status_code=401, detail="Unauthorized")


@app.post("/alert")
def send_alert(alert: Alert, x_api_key: str | None = Header(None)) -> dict:
    verify_api_key(x_api_key)

    text = f"""
🚨 OpenSRE ALERT 🚨

Service: {alert.service}
Severity: {alert.severity}
Message: {alert.message}
"""

    result = send_message(text)

    if not result.get("success"):
        raise HTTPException(
            status_code=500,
            detail=result.get("error", "Failed to send alert"),
        )

    return {"status": "alert sent"}


@app.get("/health")
def health() -> dict:
    """
    Basic health check.
    Can be extended later without breaking compatibility.
    """
    return {
        "status": "ok",
        "service": "opensre",
    }
