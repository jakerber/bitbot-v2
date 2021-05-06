"""BitBot runner module."""
import arbitrage
import constants
import datetime
import json
import time

def run():
    """Run BitBot."""
    while True:
        report = arbitrage.execute()
        print(datetime.datetime.now())
        print(json.dumps(report, indent=2))
        time.sleep(constants.TRADE_INTERVAL_SEC)


if __name__ == '__main__':
    run()
