"""Cryptocurrency arbitrage module."""
import constants
import datetime
import threading
import time
from exchanges import gemini
from exchanges import kraken

EXCHANGES = [
    gemini.Gemini(),
    kraken.Kraken()
]
AMOUNT_PRECISION = 5
PRICE_PRECISION = 1
GAIN_PRECISION = 4


class Arbitrage:
    """Arbitrage trade class."""

    def __init__(self,
                 coin,
                 exchangeAsk,
                 askPrice,
                 exchangeBid,
                 bidPrice,
                 gain):
        self.coin = coin
        self.exchangeAsk = exchangeAsk
        self.askPrice = round(askPrice, PRICE_PRECISION)
        self.exchangeBid = exchangeBid
        self.bidPrice = round(bidPrice, PRICE_PRECISION)
        self.gain = gain

    def execute(self):
        """Execute trades in seperate threads."""
        tradeAmount = round(constants.TRADE_AMOUNT_USD / self.askPrice,
                            AMOUNT_PRECISION)
        threading.Thread(target=self.exchangeAsk.buy,
                         args=(self.coin, tradeAmount, self.askPrice)).start()
        threading.Thread(target=self.exchangeBid.sell,
                         args=(self.coin, tradeAmount, self.bidPrice)).start()

    def __str__(self):
        """String representation of object."""
        buyName = type(self.exchangeAsk).__name__
        sellName = type(self.exchangeBid).__name__
        return (f'{buyName} buy @ {self.askPrice}, {sellName} sell @ '
                f'{self.bidPrice} (+{round(self.gain*100, GAIN_PRECISION)}%)')


def execute():
    """Execute arbitrage across exchanges.

    :return: report of analysis as dict
    """
    prices = {}
    balances = {'dollar': 0.0}
    priceReport = {}
    arbitrageReport = {}

    # collect prices by coin and exchange
    for coin in constants.SUPPORTED_COINS:
        prices[coin] = {}
        balances[coin] = 0.0
        priceReport[coin] = []
        arbitrageReport[coin] = []
        for exchange in EXCHANGES:

            # safely fetch price
            try:
                price = exchange.price(coin)
            except RuntimeError as error:
                print(f'{type(exchange).__name__} failed to fetch '
                      f'{coin} price: {repr(error)}')
            else:
                prices[coin][exchange] = price
                priceReport[coin].append({type(exchange).__name__: price})

        # detect arbitrage opportunities (ask < bid)
        bestOp = None
        for exchangeA, pricesA in prices[coin].items():
            for exchangeB, pricesB in prices[coin].items():
                if exchangeA == exchangeB:
                    continue

                # determine profitability
                diff = pricesB.get('bid') - pricesA.get('ask')
                unrealizedGain = round(diff / pricesA.get('ask'), 4)
                if pricesA.get('ask') < pricesB.get('bid') and \
                   unrealizedGain >= constants.TRADE_ARBITRAGE_THRESHOLD and \
                   (not bestOp or unrealizedGain > bestOp.gain):
                    bestOp = Arbitrage(coin,
                                       exchangeA,
                                       pricesA.get('ask'),
                                       exchangeB,
                                       pricesB.get('bid'),
                                       unrealizedGain)

        # execute best arbitrage opportunity
        if bestOp:
            try:
                bestOp.execute()
            except RuntimeError as error:
                print(f'unable to execute {coin} trade: {repr(error)}')
            else:
                arbitrageReport[coin].append(str(bestOp))

        # pause before moving to next coin
        time.sleep(constants.API_DELAY_SEC)

    # fetch balances across exchanges
    for exchange in EXCHANGES:
        for coin, balance in exchange.balances.items():
            balances[coin] += balance

    return {'arbitrages': arbitrageReport,
            'balances': balances,
            'prices': priceReport,
            'datetime': str(datetime.datetime.utcnow())}
