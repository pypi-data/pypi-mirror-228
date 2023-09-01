"""Top-level package for dwai."""
import os

api_key = os.environ.get("DW_API_KEY")
api_base = os.environ.get("DW_API_BASE")

api_key_singapore = os.environ.get("DW_API_SINGAPORE_KEY")
api_base_singapore = os.environ.get("DW_API_SINGAPORE_BASE")

api_timeout_seconds = 300


