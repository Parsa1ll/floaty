import os
from dotenv import load_dotenv

load_dotenv()

FLOAT_API_KEY: str = os.getenv("FLOAT_API_KEY", "")
FLOAT_BASE_URL: str = os.getenv("FLOAT_BASE_URL", "https://api.floatfinancial.com")

if not FLOAT_API_KEY:
    raise ValueError("FLOAT_API_KEY is not set. Add it to your .env file.")
