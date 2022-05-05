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
        plt.plot(self.portfolio_sims)
        plt.ylabel('Portfolio Value($)')
        plt.xlabel('Days')
        plt.title("Monte Carlo Simulation of a stock portfolio")
        plt.show()

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
    expected_returns = Calculator.get_returns(returns)
    covariance = Calculator.get_covariance(expected_returns)
    print(covariance)
    cp = ChartPlotter()
    # cp.plot_prices(data)
    # cp.plot_returns(returns)
    # cp.plot_correlation_matrix(covariance)


    print('Okay')
"""
    print('5. Use Monte Carlo Simulation')
    # Generate portfolios with allocations
    portfolios_allocations_df = mcs.generate_portfolios(expected_returns, covariance, settings.RiskFreeRate)
    portfolio_risk_return_ratio_df = portfolios_allocation_mapper.map_to_risk_return_ratios(portfolios_allocations_df)

    # Plot portfolios, print max sharpe portfolio & save data
    cp.plot_portfolios(portfolio_risk_return_ratio_df)
    max_sharpe_portfolio = mc.get_max_sharpe_ratio(portfolio_risk_return_ratio_df)['Portfolio']
    max_shape_ratio_allocations = portfolios_allocations_df[['Symbol', max_sharpe_portfolio]]
    print(max_shape_ratio_allocations)
    fr.save_to_file(portfolios_allocations_df, 'MonteCarloPortfolios')
    fr.save_to_file(portfolio_risk_return_ratio_df, 'MonteCarloPortfolioRatios')

    print('6. Use an optimiser')
    # Generate portfolios
    targets = settings.get_my_targets()
    optimiser = obj_factory.get_optimiser(targets, len(expected_returns.index))
    portfolios_allocations_df = optimiser.generate_portfolios(expected_returns, covariance, settings.RiskFreeRate)
    portfolio_risk_return_ratio_df = portfolios_allocation_mapper.map_to_risk_return_ratios(portfolios_allocations_df)

    # plot efficient frontiers
    cp.plot_efficient_frontier(portfolio_risk_return_ratio_df)
    cp.show_plots()
"""