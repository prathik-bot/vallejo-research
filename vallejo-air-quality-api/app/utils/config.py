import os
from dotenv import load_dotenv

load_dotenv()

PURPLEAIR_API_KEY = os.getenv("PURPLEAIR_API_KEY")
if not PURPLEAIR_API_KEY:
    raise ValueError("Missing PURPLEAIR_API_KEY in .env file")

print("[CONFIG] PurpleAir API Key loaded successfully")