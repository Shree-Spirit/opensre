from pydantic import BaseModel
from fastapi import FastAPI, Header, HTTPException
from app.integrations.telegram import send_message   # ✅ fixed import

app = FastAPI()


# ✅ Request model
class Alert(BaseModel):
    service: str
    severity: str
    message: str


# ✅ API key verification function (separate)
def verify_api_key(x_api_key: str):
    if x_api_key != "my-secret-key":
        raise HTTPException(status_code=401, detail="Unauthorized")


# ✅ MAIN ALERT API (FIXED)
@app.post("/alert")
def send_alert(alert: Alert, x_api_key: str = Header(None)):
    verify_api_key(x_api_key)

    text = f"""
🚨 OpenSRE ALERT 🚨

Service: {alert.service}
Severity: {alert.severity}
Message: {alert.message}
"""

    send_message(text)
    return {"status": "alert sent"}


# ✅ TEST API (also protected)
@app.get("/test-telegram")
def test(x_api_key: str = Header(None)):
    verify_api_key(x_api_key)

    send_message("🔥 Alert from OpenSRE!")
    return {"status": "sent"}


# ✅ HEALTH ROUTE (important for PR)
@app.get("/health")
def health():
    return {"status": "ok"}
