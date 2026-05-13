from __future__ import annotations

import requests
import os
from dotenv import load_dotenv

load_dotenv()

# ✅ Load environment variables
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")


# ✅ Validate config at startup
if not TOKEN or not CHAT_ID:
    raise ValueError("Telegram TOKEN or CHAT_ID is missing in .env")


# ✅ Send message function
def send_message(text: str) -> dict:
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

    payload = {
        "chat_id": CHAT_ID,
        "text": text
    }

    try:
        response = requests.post(url, json=payload, timeout=5)
        data = response.json()

        if not data.get("ok"):
            return {
                "success": False,
                "error": data
            }

        return {
            "success": True,
            "data": data
        }

    except requests.exceptions.RequestException as e:
        return {
            "success": False,
            "error": str(e)
        }
