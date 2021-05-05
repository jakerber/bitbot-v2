"""Gemini API wrapper module."""
import constants
import json
import requests

BASE_URL = 'https://api.gemini.com/v2'

def getPrice():
    """Get Bitcoin price information.

    https://docs.gemini.com/rest-api/#ticker-v2

    :returns: price information as json
    """
    response = requests.get(BASE_URL + f'/ticker/BTCUSD')
    return response.json()

def buy(amount):
    """Buy Bitcoin.

    :amount: amount to buy
    :raises: NotImplementedError
    """
    raise NotImplementedError('buy not implemented')

def sell(amount):
    """Sell Bitcoin.

    :amount: amount to sell
    :raises: NotImplementedError
    """
    raise NotImplementedError('sell not implemented')
