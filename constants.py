"""BitBot application constants module."""
import os

INTERVAL_SEC = int(os.getenv("INTERVAL_SEC"))

TRADE_AMOUNT_USD = float(os.getenv("TRADE_AMOUNT_USD"))
