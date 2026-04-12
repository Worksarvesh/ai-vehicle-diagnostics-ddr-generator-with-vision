import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY", "demo-key")


def api_key_auth(key: str) -> bool:
    return key == API_KEY
