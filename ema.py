"""Exponential moving average calculator module."""
import pandas

def ema(prices):
    """Calculate EMA price.

    :param prices: descending list of historical price points
    :return: pandas DataFrame containing EMA price
    """
    prices = prices[::-1]  # reverse list to make it ascending
    dataframe = pandas.DataFrame(data={'price': prices})
    dataframe['ema'] = dataframe.ewm(span=len(prices), adjust=False).mean()
    dataframe['emsd'] = dataframe['price'].ewm(span=len(prices), adjust=False).std()
    return dataframe
