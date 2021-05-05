"""BitBot application constants module."""
import os

# trading parameters
TRADE_AMOUNT_USD = float(os.getenv("TRADE_AMOUNT_USD"))
TRADE_INTERVAL_SEC = int(os.getenv("TRADE_INTERVAL_SEC"))
TRADE_SD_THRESHOLD = float(os.getenv("TRADE_SD_THRESHOLD"))

# Gemini API
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_API_SECRET = os.getenv("GEMINI_API_SECRET")
