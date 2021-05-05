"""BitBot core price analysis module."""
import constants
import ema
import gemini

def analyze():
    """Analyze Bitcoin price to determine trades.

    :return: dict summary of analysis
    """
    # fetch price info from Gemini
    priceInfo = gemini.getPrice()
    prices = priceInfo['changes']

    # calculate exponential moving average and SD
    _ema = ema.ema(prices)
    currentEma = _ema['ema'].values[-1]
    currentEmsd = _ema['emsd'].values[-1]
    currentAsk = float(priceInfo.get('ask'))
    currentBid = float(priceInfo.get('bid'))

    # init analysis summary report
    summary = {
        'ema': currentEma,
        'emsd': currentEmsd,
        'ask': currentAsk,
        'bid': currentBid,
        'action': None,
        'amount': None
    }

    # buy if ask is at least 1 SD below EMA
    if currentAsk <= currentEma - currentEmsd:
        amount = constants.TRADE_AMOUNT_USD / currentAsk
        gemini.buy(amount)  # execute trade
        summary['action'] = 'buy'
        summary['amount'] = amount

    # sell if bid is at least 1 SD above EMA
    if currentBid >= currentEma + currentEmsd:
        amount = constants.TRADE_AMOUNT_USD / currentBid
        gemini.sell(amount)  # execute trade
        summary['action'] = 'sell'
        summary['amount'] = amount

    return summary
