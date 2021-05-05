"""BitBot runner module."""
import analyze
import constants
import time

def run():
    """Run BitBot."""
    while True:
        report = analyze.analyze()
        print(report)
        time.sleep(constants.INTERVAL_SEC)


if __name__ == '__main__':
    run()
