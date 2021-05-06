"""Cryptocurrency arbitrage module."""
import constants
import threading
from exchanges import gemini
from exchanges import kraken

EXCHANGES = [
    gemini.Gemini(),
    kraken.Kraken()
]
AMOUNT_PRECISION = 5
PRICE_PRECISION = 1

class Arbitrage:
    """Arbitrage trade class."""

    def __init__(self, coin, exchangeAsk, askPrice, exchangeBid, bidPrice, gain):
        self.coin = coin
        self.exchangeAsk = exchangeAsk
        self.askPrice = round(askPrice, PRICE_PRECISION)
        self.exchangeBid = exchangeBid
        self.bidPrice = round(bidPrice, PRICE_PRECISION)
        self.gain = gain

    def execute(self):
        """Execute trades in seperate threads."""
        tradeAmount = round(constants.TRADE_AMOUNT_USD / self.askPrice, AMOUNT_PRECISION)
        threading.Thread(target=self.exchangeAsk.buy,
                         args=(self.coin, tradeAmount, self.askPrice)).start()
        threading.Thread(target=self.exchangeBid.sell,
                         args=(self.coin, tradeAmount, self.bidPrice)).start()

    def __str__(self):
        """String representation of object."""
        buyName = type(self.exchangeAsk).__name__
        sellName = type(self.exchangeBid).__name__
        return f'{self.coin}: {buyName} buy @ {self.askPrice}, {sellName} sell @ {self.bidPrice}'


def execute():
    """Execute arbitrage across exchanges.

    :return: report of analysis as dict
    """
    prices = {coin: {} for coin in constants.SUPPORTED_COINS}
    for exchange in EXCHANGES:
        exchangeName = type(exchange).__name__

        # safely fetch prices
        try:
            exchangePrices = exchange.prices
        except RuntimeError as error:
            print(f'{exchangeName} failed to fetch prices: {repr(error)}')

        # collect prices by coin and exchange
        else:
            for coin, price in exchangePrices.items():
                prices[coin][exchange] = price

    # detect arbitrage opportunities (ask < bid)
    arbitrages = []
    for coin, exchanges in prices.items():
        for exchangeA, pricesA in exchanges.items():
            for exchangeB, pricesB in exchanges.items():
                if exchangeA == exchangeB:
                    continue

                # determine if trade is profitable
                unrealizedGain = round((pricesB.get('bid') - pricesA.get('ask')) / pricesA.get('ask'), 4)
                if pricesA.get('ask') < pricesB.get('bid') and unrealizedGain >= constants.TRADE_ARBITRAGE_THRESHOLD:
                    arbitrage = Arbitrage(coin,
                                          exchangeA,
                                          pricesA.get('ask'),
                                          exchangeB,
                                          pricesB.get('bid'),
                                          unrealizedGain)

                    # execute arbitrage
                    try:
                        arbitrage.execute()
                    except RuntimeError as error:
                        print(f'unable to execute trade: {repr(error)}')
                    else:
                        arbitrages.append(str(arbitrage))

    return arbitrages
