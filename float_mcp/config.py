import os
from dotenv import load_dotenv

load_dotenv()


def _env_str(name: str, default: str = "") -> str:
    v = os.getenv(name, default) or ""
    return v.strip().strip('"').strip("'")


FLOAT_API_KEY: str = _env_str("FLOAT_API_KEY")
FLOAT_BASE_URL: str = _env_str("FLOAT_BASE_URL", "https://api.floatfinancial.com")
if not FLOAT_BASE_URL:
    FLOAT_BASE_URL = "https://api.floatfinancial.com"

if not FLOAT_API_KEY:
    raise ValueError("FLOAT_API_KEY is not set. Add it to your .env file.")
