import datetime as dt
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import pandas_datareader.data as web

class Calculator:
    @staticmethod
    def get_returns(stock_prices):
        return np.log(stock_prices / stock_prices.shift(1))

    @staticmethod
    def get_expectedreturns(returns):
            return returns.mean() * 252

    @staticmethod
    def get_covariance(returns):
            return returns.cov() * 252
