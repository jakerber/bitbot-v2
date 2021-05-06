"""BitBot application constants module."""
import os

# global variables
ALLOW_TRADING = os.getenv('ALLOW_TRADING') == 'True'
API_DELAY_SEC = 0.5
SUPPORTED_COINS = [
    'bitcoin',
    # 'ethereum',
    # 'litecoin'
]

# trading parameters
TRADE_AMOUNT_USD = float(os.getenv('TRADE_AMOUNT_USD'))
TRADE_ARBITRAGE_THRESHOLD = float(os.getenv('TRADE_ARBITRAGE_THRESHOLD'))
TRADE_INTERVAL_SEC = int(os.getenv('TRADE_INTERVAL_SEC'))

# Gemini API
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
GEMINI_API_SECRET = os.getenv('GEMINI_API_SECRET')
GEMINI_COIN_TO_TICKER = {
    'bitcoin': 'BTCUSD',
    # 'ethereum': 'ETHUSD',
    # 'litecoin': 'LTCUSD'
}

# Kraken API
KRAKEN_API_KEY = os.getenv('KRAKEN_API_KEY')
KRAKEN_API_SECRET = os.getenv('KRAKEN_API_SECRET')
KRAKEN_COIN_TO_TICKER = {
    'bitcoin': 'XXBTZUSD',
    # 'ethereum': 'XETHZUSD',
    # 'litecoin': 'XLTCZUSD'
}
