"""Gemini exchange module.

https://docs.gemini.com/rest-api/
"""
import base64
import datetime
import constants
import hashlib
import hmac
import json
import requests
import time
from exchanges import common

API_KEY = constants.GEMINI_API_KEY
API_SECRET = constants.GEMINI_API_SECRET
BASE_URL = 'https://api.gemini.com/'

class Gemini(common.ExchangeBase):
    """Gemini exchange class."""

    @property
    def prices(self):
        """Coin prices.

        https://docs.gemini.com/rest-api/#ticker-v2

        :returns: price dict in format {'bitcoin': {'ask': 101.0, 'bid': 100.0}}
        """
        prices = {}
        endpoint = 'v2/ticker/'
        for coin, ticker in constants.GEMINI_COIN_TO_TICKER.items():
            response = requests.get(BASE_URL + endpoint + ticker)
            self.handle(endpoint, response)
            prices[coin] = {'ask': float(response.json().get('ask')),
                            'bid': float(response.json().get('bid'))}
        return prices

    def buy(self, coin, amount, price):
        """Buy coins.

        https://docs.gemini.com/rest-api/#new-order

        :param coin: name of coin
        :param amount: amount to buy
        :param price: limit price to buy at
        :raises RuntimeError: if unable to buy
        """
        super().buy(coin, amount, price)
        endpoint = '/v1/order/new'
        payload = {
            'request': endpoint,
            'nonce': self._getNonce(),
            'symbol': constants.GEMINI_COIN_TO_TICKER[coin],
            'price': price,
            'amount': amount,
            'side': 'buy',
            'type': 'exchange limit',
            'options': ['fill-or-kill']
        }
        response = requests.post(BASE_URL + endpoint,
                                 data=None,
                                 headers=self._getHeaders(payload))
        self.handle(endpoint, response)

    def sell(self, coin, amount, price):
        """Sell coins.

        https://docs.gemini.com/rest-api/#new-order

        :param coin: name of coin
        :param amount: amount to sell
        :param price: limit price to sell at
        :raises RuntimeError: if unable to sell
        """
        super().sell(coin, amount, price)
        endpoint = '/v1/order/new'
        payload = {
            'request': endpoint,
            'nonce': self._getNonce(),
            'symbol': constants.GEMINI_COIN_TO_TICKER[coin],
            'price': price,
            'amount': amount,
            'side': 'sell',
            'type': 'exchange limit',
            'options': ['fill-or-kill']
        }
        response = requests.post(BASE_URL + endpoint,
                                 data=None,
                                 headers=self._getHeaders(payload))
        self.handle(endpoint, response)

    def handle(self, endpoint, response):
        """Common API response handling.

        :param endpoint: requested endpoint
        :param response: request response
        :raises: RuntimeError if request failed
        """
        super().handle(endpoint, response)
        if response.status_code != 200:  # 200 OK status
            reason = response.json().get('reason', '<None>')
            message = response.json().get('message', '<None>')
            raise RuntimeError(f'Gemini {endpoint} request failed with {reason}: {message} ({response.status_code})')
        elif response.json().get('is_cancelled', False):
            raise RuntimeError(f'Gemini {endpoint} request failed: order cancelled (unable to fill?)')

    def _getHeaders(self, payload):
        """Generate API request headers.

        :param payload: request payload
        :returns: request headers as dict
        """
        encodedPayload = json.dumps(payload).encode()
        b64Payload = base64.b64encode(encodedPayload)
        signature = hmac.new(API_SECRET.encode(), b64Payload, hashlib.sha384).hexdigest()
        return {
            'Content-Type': 'text/plain',
            'Content-Length': '0',
            'X-GEMINI-APIKEY': API_KEY,
            'X-GEMINI-PAYLOAD': b64Payload,
            'X-GEMINI-SIGNATURE': signature,
            'Cache-Control': 'no-cache'
        }

    def _getNonce(self):
        """Generate API request nonce based on current time.

        :returns: nonce value
        """
        return str(int(time.mktime(datetime.datetime.now().timetuple()) * 1000))
