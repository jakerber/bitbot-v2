"""BitBot runner module."""
import analyze
import constants
import time

def run():
    """Run BitBot."""
    while True:
        report = analyze.analyze()
        print(report)
        time.sleep(constants.TRADE_INTERVAL_SEC)


if __name__ == '__main__':
    run()
