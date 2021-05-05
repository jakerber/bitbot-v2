"""BitBot Bitcoin trading simulation module."""
import constants
import gemini
import run
import sys
import time

# override constants
constants.TRADE_AMOUNT_USD = 100.0
constants.TRADE_INTERVAL_SEC = 0
constants.TRADE_SD_THRESHOLD = 2.0

# simulation constants
STARTING_ACCOUNT_USD = 1000
STARTING_ACCOUNT_BTC = 0.05
STARTING_HOUR = 24  # begin 24 hours into the simulation
ASK_BID_DIFF = 0.00004
GIMINI_FEES = 0.00450

# override starting hour if user provided a value
STARTING_HOUR = int(sys.argv[1]) if len(sys.argv) > 1 else STARTING_HOUR

# initialize simulation
ACCOUNT_USD = STARTING_ACCOUNT_USD
ACCOUNT_BTC = STARTING_ACCOUNT_BTC
CURRENT_HOUR = STARTING_HOUR

# load historical price data
PRICE_HISTORY_BTC = []
with open('datasets/btc_history.csv') as file:
    for line in file.readlines()[1:]:
        _, price = line.strip().split(',')
        PRICE_HISTORY_BTC.append(float(price.strip()))
PRICE_HISTORY_BTC = PRICE_HISTORY_BTC
STARTING_BTC_PRICE = PRICE_HISTORY_BTC[STARTING_HOUR]

# mock trading methods
def mockBuy(amount):
    """Simulate buying Bitcoin.

    :amount: amount to buy
    """
    global ACCOUNT_USD
    global ACCOUNT_BTC
    if ACCOUNT_USD > constants.TRADE_AMOUNT_USD:
        ACCOUNT_USD -= constants.TRADE_AMOUNT_USD * (1 + GIMINI_FEES)
        ACCOUNT_BTC += amount

def mockSell(amount):
    """Simulate selling Bitcoin.

    :amount: amount to sell
    """
    global ACCOUNT_USD
    global ACCOUNT_BTC
    if ACCOUNT_BTC > amount:
        ACCOUNT_USD += constants.TRADE_AMOUNT_USD * (1 - GIMINI_FEES)
        ACCOUNT_BTC -= amount

gemini.buy = mockBuy
gemini.sell = mockSell

# mock gemini price API
def mockGetPrice():
    """Get simulated Bitcoin price information.

    https://docs.gemini.com/rest-api/#ticker-v2

    :returns: price information as json
    """
    # calculate simulated prices
    currentPrice = PRICE_HISTORY_BTC[CURRENT_HOUR]
    currentAsk = currentPrice + (currentPrice * ASK_BID_DIFF)
    currentBid = currentPrice - (currentPrice * ASK_BID_DIFF)
    last24Prices = PRICE_HISTORY_BTC[CURRENT_HOUR - 24:CURRENT_HOUR]

    # simulated Bitcoin price information
    return {
        'ask': currentAsk,
        'bid': currentBid,
        'changes': last24Prices,
    }

gemini.getPrice = mockGetPrice

# mock time passing.
def mockSleep(_):
    """Simulate the passage of time."""
    global CURRENT_HOUR

    # increment simulated time
    CURRENT_HOUR += 1

    # end simulation if max time exceeded
    # display results and exit
    if CURRENT_HOUR == len(PRICE_HISTORY_BTC):
        endingBTCPrice = PRICE_HISTORY_BTC[CURRENT_HOUR - 1]
        print()
        print(f'starting btc: {STARTING_ACCOUNT_BTC} (${round(STARTING_ACCOUNT_BTC * STARTING_BTC_PRICE, 2)})')
        print(f'starting usd: {STARTING_ACCOUNT_USD}')
        print(f'ending btc: {ACCOUNT_BTC} (${round(ACCOUNT_BTC * endingBTCPrice, 2)})')
        print(f'ending usd: {ACCOUNT_USD}')
        sys.exit(0)

    # display simulated time
    sys.stdout.write(f'hour {CURRENT_HOUR}/{len(PRICE_HISTORY_BTC)}: ')

time.sleep = mockSleep

# run simulation
run.run()
