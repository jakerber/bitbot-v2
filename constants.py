"""BitBot application constants module."""
import os

# global variables
PROD_ENV = os.getenv('PROD_ENV') == 'True'
SUPPORTED_COINS = [
    'bitcoin',
    # TODO: re-enable once balance sufficient
    # 'ethereum',
    # 'litecoin'
]
ALLOW_TRADING = os.getenv('ALLOW_TRADING') == 'True'
API_DELAY_SEC = 1.0
EMAIL_ADDRESS = os.getenv('EMAIL_ADDRESS')

# trading parameters
TRADE_AMOUNT_USD = float(os.getenv('TRADE_AMOUNT_USD'))
TRADE_ARBITRAGE_THRESHOLD = float(os.getenv('TRADE_ARBITRAGE_THRESHOLD'))
TRADE_INTERVAL_SEC = int(os.getenv('TRADE_INTERVAL_SEC'))

# Mailgun email alerts
MAILGUN_API_KEY = os.getenv('MAILGUN_API_KEY')
MAILGUN_DOMAIN = os.getenv('MAILGUN_DOMAIN')

# Gemini API
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
GEMINI_API_SECRET = os.getenv('GEMINI_API_SECRET')
GEMINI_COIN_TO_PAIR = {
    'bitcoin': 'BTCUSD',
    'ethereum': 'ETHUSD',
    'litecoin': 'LTCUSD'
}
GEMINI_TICKER_TO_COIN = {
    'USD': 'dollar',
    'BTC': 'bitcoin',
    'ETH': 'ethereum',
    'LTC': 'litecoin'
}

# Kraken API
KRAKEN_API_KEY = os.getenv('KRAKEN_API_KEY')
KRAKEN_API_SECRET = os.getenv('KRAKEN_API_SECRET')
KRAKEN_COIN_TO_PAIR = {
    'bitcoin': 'XXBTZUSD',
    'ethereum': 'XETHZUSD',
    'litecoin': 'XLTCZUSD'
}
KRAKEN_TICKER_TO_COIN = {
    'ZUSD': 'dollar',
    'XXBT': 'bitcoin',
    'XETH': 'ethereum',
    'XLTC': 'litecoin'
}
