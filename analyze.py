"""BitBot core price analysis module."""
import constants
import ema
import gemini

ROUND_DECIMALS = 5

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

    # buy if ask is some SD multiplier below EMA
    if currentAsk <= currentEma - (currentEmsd * constants.TRADE_SD_THRESHOLD):
        amount = round(constants.TRADE_AMOUNT_USD / currentAsk, ROUND_DECIMALS)
        gemini.buy(amount, currentAsk)  # execute trade
        summary['action'] = f'buy {amount} @ {currentAsk}'

    # sell if bid is some SD multiplier above EMA
    if currentBid >= currentEma + (currentEmsd * constants.TRADE_SD_THRESHOLD):
        amount = round(constants.TRADE_AMOUNT_USD / currentBid, ROUND_DECIMALS)
        gemini.sell(amount, currentBid)  # execute trade
        summary['action'] = f'sell {amount} @ {currentBid}'

    return summary
