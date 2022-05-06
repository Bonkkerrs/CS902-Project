import numpy as np
import pandas as pd
from functools import reduce


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

    @staticmethod
    def calculate_sharpe_ratio(risk, returns, risk_free_rate):
        return (returns - risk_free_rate) / risk

    @staticmethod
    def get_max_sharpe_ratio(df):
        return df.iloc[df['SharpeRatio'].astype(float).idxmax(), :]

    @staticmethod
    def get_min_risk(df):
        return df.iloc[df['Risk'].astype(float).idxmin(), :]

    @staticmethod
    def calculate_portfolio_risk(allocations, cov):
        return np.sqrt(reduce(np.dot, [allocations, cov, allocations.T]))

    @staticmethod
    def calculate_portfolio_expectedreturns(returns, allocations):
        return sum(returns * allocations)

    @staticmethod
    def map_to_risk_return_ratios(input):
        portfolios = input.columns.values[2:]
        returns = input.loc[input['Symbol'] == 'Return'].values[0][2:]
        risks = input.loc[input['Symbol'] == 'Risk'].values[0][2:]
        sharpe_ratios = input.loc[input['Symbol'] == 'SharpeRatio'].values[0][2:]
        df = pd.DataFrame(
            {'Portfolio': portfolios,
             'Return': returns,
             'Risk': risks,
             'SharpeRatio': sharpe_ratios})
        return df
