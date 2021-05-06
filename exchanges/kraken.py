"""Kraken exchange module.

https://docs.kraken.com/rest/
"""
import constants
import krakenex
from exchanges import common

KRAKEN = krakenex.API(key=constants.KRAKEN_API_KEY,
                      secret=constants.KRAKEN_API_SECRET)

class Kraken(common.ExchangeBase):
    """Kraken exchange class."""

    @property
    def prices(self):
        """Coin prices.

        https://docs.kraken.com/rest/#operation/getTickerInformation

        :returns: price dict in format {'bitcoin': {'ask': 101.0, 'bid': 100.0}}
        """
        prices = {}
        endpoint = 'Ticker'
        for coin, ticker in constants.KRAKEN_COIN_TO_TICKER.items():
            response = KRAKEN.query_public(endpoint, data={'pair': ticker})
            self.handle(endpoint, response)
            prices[coin] = {'ask': float(response.get('result').get(ticker).get('a')[0]),
                            'bid': float(response.get('result').get(ticker).get('b')[0])}
        return prices

    def buy(self, coin, amount, price):
        """Buy coins.

        https://docs.kraken.com/rest/#operation/addStandardOrder

        :param coin: name of coin
        :param amount: amount to buy
        :param price: limit price to buy at
        :raises RuntimeError: if unable to buy
        """
        super().buy(coin, amount, price)
        endpoint = 'AddOrder'
        ticker = constants.KRAKEN_COIN_TO_TICKER[coin]
        payload = {
            'pair': ticker,
            'type': 'buy',
            'ordertype': 'limit',
            'volume': amount,
            'price': price
        }
        response = KRAKEN.query_private(endpoint, data=payload)
        self.handle(endpoint, response)

    def sell(self, coin, amount, price):
        """Sell coins.

        https://docs.kraken.com/rest/#operation/addStandardOrder

        :param coin: name of coin
        :param amount: amount to sell
        :param price: limit price to sell at
        :raises RuntimeError: if unable to sell
        """
        super().sell(coin, amount, price)
        endpoint = 'AddOrder'
        ticker = constants.KRAKEN_COIN_TO_TICKER[coin]
        payload = {
            'pair': ticker,
            'type': 'sell',
            'ordertype': 'limit',
            'volume': amount,
            'price': price
        }
        response = KRAKEN.query_private(endpoint, data=payload)
        self.handle(endpoint, response)

    def handle(self, endpoint, response):
        """Common API response handling.

        :param endpoint: requested endpoint
        :param response: request response
        :raises: RuntimeError if request failed
        """
        super().handle(endpoint, response)
        if response.get('error') or 'result' not in response:
            raise RuntimeError(f'Kraken {endpoint} request failed: {response.get("error", "<unknown>")}')
