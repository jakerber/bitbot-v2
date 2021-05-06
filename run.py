"""BitBot runner module."""
import arbitrage
import constants
import json
import notifications
import time

def run():
    """Run BitBot."""
    while True:
        report = arbitrage.execute()
        reportJson = json.dumps(report, indent=2)
        if not constants.PROD_ENV:
            print(f'report {reportJson}')
        if any(trades for coin, trades in report.get('arbitrages').items()):
            notifications.email('Alert: Arbitrage Trade', reportJson)

        # Zzzz
        time.sleep(constants.TRADE_INTERVAL_SEC)


if __name__ == '__main__':
    run()
