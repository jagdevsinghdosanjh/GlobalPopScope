import requests
import logging
import json
from typing import Optional
from urllib.parse import urlparse

TIMEOUT = 10  # seconds
LOCAL_JSON_PATH = "undata.json"  # Can be a file path or full URL

def load_json_source(path_or_url: str) -> Optional[dict]:
    """Loads JSON from a local file or URL."""
    try:
        parsed = urlparse(path_or_url)
        if parsed.scheme in ["http", "https"]:
            response = requests.get(path_or_url, timeout=TIMEOUT)
            response.raise_for_status()
            return response.json()
        else:
            with open(path_or_url, "r", encoding="utf-8") as f:
                return json.load(f)
    except (requests.RequestException, FileNotFoundError, json.JSONDecodeError) as e:
        logging.error(f"Failed to load data from {path_or_url}: {e}")
        return None

def fetch_indicators() -> Optional[dict]:
    """Gets indicator list from undata.json or live API."""
    return load_json_source(LOCAL_JSON_PATH)

def fetch_indicator_data(indicator_code: str) -> Optional[dict]:
    """Optional extension: load from dynamic file per indicator (if applicable)."""
    # Example logic if you have per-indicator saved data
    path = f"data/{indicator_code}.json"
    return load_json_source(path)

def fetch_goals() -> Optional[dict]:
    """Simulate goals retrieval from another static file or segment."""
    return load_json_source("goals.json")  # Or extract from undata.json if combined
