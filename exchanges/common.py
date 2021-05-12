"""Common exchange module."""
import constants
import datetime
import time


class ExchangeBase:
    """Base class for exchanges."""

    @property
    def prices(self):
        """Coin prices.

        :returns: price dict in format {'bitcoin': {'ask': 11.0, 'bid': 10.0}}
        """
        raise NotImplementedError

    @property
    def balances(self):
        """Coin account balances.

        :returns: balances dict in format {'usd': 50.0, 'bitcoin': 2.0}
        """
        raise NotImplementedError

    def price(self, coin):
        """Get price of individual coin.

        :param coin: name of coins
        :returns: price dict in format {'ask': 101.0, 'bid': 100.0}
        """
        if coin not in constants.SUPPORTED_COINS:
            raise RuntimeError(f'coin {coin} not supported')

    def buy(self, coin, amount, price):
        """Buy coins.

        :param coin: name of coin
        :param amount: amount to buy
        :param price: limit price to buy at
        :raises RuntimeError: if unable to buy
        """
        if coin not in constants.SUPPORTED_COINS:
            raise RuntimeError(f'coin {coin} not supported')
        if not constants.ALLOW_TRADING:
            raise RuntimeError('trading not allowed')
        print(f'{type(self).__name__} executing buy of '
              f'{amount} {coin} @ {price}')

    def sell(self, coin, amount, price):
        """Sell coins.

        :param coin: name of coin
        :param amount: amount to sell
        :param price: limit price to sell at
        :raises RuntimeError: if unable to sell
        """
        if coin not in constants.SUPPORTED_COINS:
            raise RuntimeError(f'coin {coin} not supported')
        if not constants.ALLOW_TRADING:
            raise RuntimeError('trading not allowed')
        print(f'{type(self).__name__} executing sell of '
              f'{amount} {coin} @ {price}')

    def handle(self, endpoint, response):
        """Common API response handling.

        :param endpoint: requested endpoint
        :param response: request response
        :raises: RuntimeError if request failed
        """
        if not constants.PROD_ENV:
            print(f'{str(datetime.datetime.utcnow())}: {type(self).__name__} '
                  f'executed {endpoint}')

    def throttle(self):
        """Pause to avoid getting throttled."""
        time.sleep(constants.API_DELAY_SEC)
