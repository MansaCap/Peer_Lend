# Supabase

import os
from pathlib import Path

from dotenv import load_dotenv
from supabase import create_client

_ROOT_DIR = Path(__file__).resolve().parents[3]
_APP_DIR = Path(__file__).resolve().parents[2]

load_dotenv(_ROOT_DIR / ".env")
load_dotenv(_APP_DIR / ".env")

url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_SERVICE_KEY")

if not url or not key:
    raise RuntimeError(
        "SUPABASE_URL and SUPABASE_SERVICE_KEY "
        "must be set before starting the API."
    )

supabase = create_client(url, key)
