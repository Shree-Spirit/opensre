from pydantic import BaseModel
from fastapi import FastAPI
from app.telegram_bot import send_message

app = FastAPI()


class Alert(BaseModel):
    service: str
    severity: str
    message: str


@app.post("/alert")
def send_alert(alert: Alert):
    text = f"""
🚨 OpenSRE ALERT 🚨

Service: {alert.service}
Severity: {alert.severity}
Message: {alert.message}
"""
    send_message(text)
    return {"status": "alert sent"}


@app.get("/test-telegram")
def test():
    send_message("🔥 Alert from OpenSRE!")
    return {"status": "sent"}
