"""Gemini API wrapper module."""
import base64
import datetime
import constants
import hashlib
import hmac
import json
import requests
import time

API_KEY = constants.GEMINI_API_KEY
API_SECRET = constants.GEMINI_API_SECRET.encode()
BASE_URL = 'https://api.gemini.com/'

def getPrice():
    """Get Bitcoin price information.

    https://docs.gemini.com/rest-api/#ticker-v2

    :returns: price information as json
    """
    response = requests.get(BASE_URL + 'v2/ticker/BTCUSD')
    return response.json()

def buy(amount, price):
    """Buy Bitcoin.

    :param amount: amount to buy
    :param price: price to buy at
    :raises: NotImplementedError
    """
    endpoint = '/v1/order/new'
    payload = {
        'request': endpoint,
        'nonce': _getNonce(),
        'symbol': 'BTCUSD',
        'price': price,
        'amount': amount,
        'side': 'buy',
        'type': 'exchange limit',
        'options': ['immediate-or-cancel']
    }
    raise NotImplementedError('buy not implemented')
    response = requests.post(BASE_URL + endpoint,
                             data=None,
                             headers=_getHeaders(payload))
    _raiseIfFailed(endpoint, response)

def sell(amount, price):
    """Sell Bitcoin.

    :param param amount: amount to sell
    :param param price: price to sell at
    :raises: NotImplementedError
    """
    endpoint = '/v1/order/new'
    payload = {
        'request': endpoint,
        'nonce': _getNonce(),
        'symbol': 'BTCUSD',
        'price': price,
        'amount': amount,
        'side': 'sell',
        'type': 'exchange limit',
        'options': ['immediate-or-cancel']
    }
    raise NotImplementedError('sell not implemented')
    response = requests.post(BASE_URL + endpoint,
                             data=None,
                             headers=_getHeaders(payload))
    _raiseIfFailed(endpoint, response)

def _getHeaders(payload):
    """Generate API request headers.

    :param payload: request payload
    :returns: request headers as dict
    """
    encodedPayload = json.dumps(payload).encode()
    b64Payload = base64.b64encode(encodedPayload)
    signature = hmac.new(API_SECRET, b64Payload, hashlib.sha384).hexdigest()
    return {
        'Content-Type': 'text/plain',
        'Content-Length': '0',
        'X-GEMINI-APIKEY': API_KEY,
        'X-GEMINI-PAYLOAD': b64Payload,
        'X-GEMINI-SIGNATURE': signature,
        'Cache-Control': 'no-cache'
    }

def _getNonce():
    """Generate API request nonce based on current time.

    :returns: nonce value
    """
    return str(int(time.mktime(datetime.datetime.now().timetuple()) * 1000))

def _raiseIfFailed(endpoint, response):
    """Raise exception if request failed.

    :param endpoint: requested endpoint
    :param response: request response
    :raises: RuntimeError if request failed
    """
    if response.status_code != 200:  # 200 OK status
        reason = response.json().get('reason', '<None>')
        message = response.json().get('message', '<None>')
        raise RuntimeError(f'Gemini {endpoint} request failed with {reason}: {message} ({response.status_code})')
