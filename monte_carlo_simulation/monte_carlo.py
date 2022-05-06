import datetime as dt
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import pandas_datareader.data as web
from chart_plotter import ChartPlotter
from calculator import Calculator
import warnings
warnings.filterwarnings('ignore')

class MonteCarloEstimator:
    def __init__(self, stockList, mc_sims, T, initial_portfolio, days_back):
        self.stockList = stockList
        self.mc_sims = mc_sims
        self.T = T
        self.initial_portfolio = initial_portfolio
        self.days_back = days_back
        self.get_time()
        self.__numberOfPortfolios = T
        # self.get_data()
        # self.simulate()
        # self.plot_simulation()

    def get_data(self):
        self.stockData = web.get_data_stooq(self.stockList,self.startDate,self.endDate)
        self.stockData = self.stockData['Close']
        self.returns = self.stockData.pct_change()
        self.meanReturns = self.returns.mean()
        self.covMatrix = self.returns.cov()

    def new_get_data(self):
        prices = pd.DataFrame()
        tmp = {}
        for i in self.stockList:
            try:
                tmp = web.DataReader(i, 'stooq', self.startDate, self.endDate)
                print('Fetched prices for: ' + i)
            except:
                print('Issue getting prices for: ' + i)
            else:
                prices[i] = tmp['Close']
        self.prices = prices
        return prices

    def get_time(self):
        self.endDate = dt.datetime.now()
        self.startDate = self.endDate - dt.timedelta(days=self.days_back)

    def plot_simulation(self):
        fig = plt.figure()
        plt.plot(self.portfolio_sims)
        plt.ylabel('Portfolio Value($)')
        plt.xlabel('Days')
        plt.title("Monte Carlo Simulation of a stock portfolio")
        plt.show()
        return fig

    def simulate(self):
        self.weights = np.random.random(len(self.meanReturns))
        self.weights /= np.sum(self.weights)

        self.meanM = np.full(shape=(self.T, len(self.weights)), fill_value=self.meanReturns)
        self.meanM = self.meanM.T

        self.portfolio_sims = np.full(shape=(self.T, self.mc_sims), fill_value=0.0)

        for m in range(0, self.mc_sims):
            Z = np.random.normal(size=(self.T, len(self.weights)))
            L = np.linalg.cholesky(self.covMatrix)
            self.dailyReturns = self.meanM + np.inner(L, Z)
            self.portfolio_sims[:, m] = np.cumprod(np.inner(self.weights, self.dailyReturns.T) + 1) * self.initial_portfolio

    def generate_portfolios(self, returns, covariance, risk_free_rate):
        portfolios_allocations_df = pd.DataFrame({'Symbol': returns.index, 'MeanReturn': returns.values})
        extra_data = pd.DataFrame({'Symbol': ['Return', 'Risk', 'SharpeRatio'], 'MeanReturn': [0, 0, 0]})
        portfolios_allocations_df = portfolios_allocations_df.append(extra_data, ignore_index=True)

        portfolio_size = len(returns.index)
        np.random.seed(0)

        equal_allocations = self.get_equal_allocations(portfolio_size)
        portfolio_id = 'EqualAllocationPortfolio'
        self.compute_portfolio_risk_return_sharpe_ratio(portfolio_id, equal_allocations, portfolios_allocations_df,
                                                        returns, covariance, risk_free_rate)

        # Generating portfolios
        counter_to_print = int(self.mc_sims / 10)
        for i in range(self.mc_sims):
            portfolio_id = 'Portfolio_' + str(i)
            allocations = self.get_random_allocations(portfolio_size)
            self.compute_portfolio_risk_return_sharpe_ratio(portfolio_id, allocations, portfolios_allocations_df,
                                                            returns, covariance, risk_free_rate)

            # printing approx 10x
            if (i % counter_to_print == 0):
                print('Completed Generating ' + str(i) + 'Portfolios')

        return portfolios_allocations_df

    def compute_portfolio_risk_return_sharpe_ratio(self, portfolio_id, allocations, portfolios_allocations_df, returns,
                                                   covariance, risk_free_rate):

        # Calculate expected returns of portfolio
        expected_returns = Calculator.calculate_portfolio_expectedreturns(returns, allocations)
        # Calculate risk of portfolio
        risk = Calculator.calculate_portfolio_risk(allocations, covariance)
        # Calculate Sharpe ratio of portfolio
        sharpe_ratio = Calculator.calculate_sharpe_ratio(risk, expected_returns, risk_free_rate)


        portfolio_data = allocations
        portfolio_data = np.append(portfolio_data, expected_returns)
        portfolio_data = np.append(portfolio_data, risk)
        portfolio_data = np.append(portfolio_data, sharpe_ratio)
        # add data to the dataframe
        portfolios_allocations_df[portfolio_id] = portfolio_data

    def get_equal_allocations(self, portfolio_size):
        n = float(1 / portfolio_size)
        allocations = np.repeat(n, portfolio_size)
        return allocations

    def get_random_allocations(self, portfolio_size):

        allocations = np.random.rand(portfolio_size)
        allocations /= sum(allocations)
        return allocations


if __name__ == '__main__':
    stockList = ['BABA.US','NIO.US','TWTR.US','GDX.US','700.HK','3799.HK']
    # stockList = ['BABA.US', 'NIO.US']
    mc_sims = 100
    T = 100
    initial_portfolio = 10000
    days_back = 365*3
    m = MonteCarloEstimator(stockList, mc_sims, T, initial_portfolio, days_back)


    data = m.new_get_data()
    returns = Calculator.get_returns(data)
    expected_returns = Calculator.get_expectedreturns(returns)
    covariance = Calculator.get_covariance(returns)

    cp = ChartPlotter()
    cp.plot_prices(data)
    cp.plot_returns(returns)
    cp.plot_correlation_matrix(covariance)

    portfolios_allocations_df = m.generate_portfolios(expected_returns, covariance, 0)
    portfolio_risk_return_ratio_df = Calculator.map_to_risk_return_ratios(portfolios_allocations_df)
    cp.plot_portfolios(portfolio_risk_return_ratio_df)


    plt.show()
    print('Okay')
