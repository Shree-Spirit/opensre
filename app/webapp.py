from __future__ import annotations

from pydantic import BaseModel
from fastapi import FastAPI, Header, HTTPException
from app.integrations.telegram import send_message

app = FastAPI()


class Alert(BaseModel):
    service: str
    severity: str
    message: str


def verify_api_key(x_api_key: str):
    if x_api_key != "my-secret-key":
        raise HTTPException(status_code=401, detail="Unauthorized")


@app.post("/alert")
def send_alert(alert: Alert, x_api_key: str = Header(None)) -> dict:
    verify_api_key(x_api_key)

    text = f"""
🚨 OpenSRE ALERT 🚨

Service: {alert.service}
Severity: {alert.severity}
Message: {alert.message}
"""

    result = send_message(text)

    if not result.get("success"):
        raise HTTPException(status_code=500, detail="Failed to send alert")

    return {"status": "alert sent"}


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}