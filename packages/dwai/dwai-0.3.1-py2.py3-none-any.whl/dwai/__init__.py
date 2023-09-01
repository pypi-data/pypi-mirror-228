"""Top-level package for dwai."""
import os

api_key = os.environ.get("DW_API_KEY")
api_base = os.environ.get("DW_API_BASE")
api_timeout_seconds = 300


