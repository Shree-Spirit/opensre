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
def send_message(text: str):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

    payload = {
        "chat_id": CHAT_ID,
        "text": text
    }

    try:
        response = requests.post(url, json=payload, timeout=5)

        # ✅ Only log safe info
        print("Telegram status:", response.status_code)

        # ✅ Handle error response
        if response.status_code != 200:
            return {
                "error": "Failed to send message",
                "status_code": response.status_code
            }

        return response.json()

    except requests.exceptions.RequestException as e:
        # ✅ Handle network errors safely
        return {
            "error": "Request failed",
            "details": str(e)
        }
