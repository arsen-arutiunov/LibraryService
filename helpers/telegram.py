import os
import requests
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
TELEGRAM_API_URL = (f"https://api.telegram.org/bot"
                    f"{TELEGRAM_BOT_TOKEN}/sendMessage")


def send_telegram_message(message: str):
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        raise ValueError("No bot token or Chat ID is configured.")

    response = requests.post(TELEGRAM_API_URL, json={
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "HTML",
    })

    if not response.ok:
        raise Exception(f"Message sending error: {response.content}")
