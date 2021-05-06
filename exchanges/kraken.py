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
        for coin in constants.SUPPORTED_COINS:
            prices[coin] = self.price(coin)
            self.throttle()
        return prices

    @property
    def balances(self):
        """Coin account balances.

        https://docs.kraken.com/rest/#operation/getAccountBalance

        :returns: balances dict in format {'usd': 50.0, 'bitcoin': 2.0}
        """
        balances = {}
        endpoint = 'Balance'
        response = KRAKEN.query_private(endpoint)
        self.handle(endpoint, response)
        for ticker, coin in constants.KRAKEN_TICKER_TO_COIN.items():
            if coin in constants.SUPPORTED_COINS or coin == 'dollar':
                balances[coin] = float(response.get('result').get(ticker, 0.0))
                self.throttle()
        return balances

    def price(self, coin):
        """Get price of individual coin.

        https://docs.kraken.com/rest/#operation/getTickerInformation

        :param coin: name of coins
        :returns: price dict in format {'ask': 101.0, 'bid': 100.0}
        """
        endpoint = 'Ticker'
        pair = constants.KRAKEN_COIN_TO_PAIR[coin]
        response = KRAKEN.query_public(endpoint, data={'pair': pair})
        self.handle(endpoint, response)
        return {'ask': float(response.get('result').get(pair).get('a')[0]),
                'bid': float(response.get('result').get(pair).get('b')[0])}

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
        ticker = constants.KRAKEN_COIN_TO_PAIR[coin]
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
        ticker = constants.KRAKEN_COIN_TO_PAIR[coin]
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
        if response.get('error') or 'result' not in response:
            raise RuntimeError(f'Kraken {endpoint} request failed: {response.get("error", "<unknown>")}')
