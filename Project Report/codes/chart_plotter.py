import matplotlib.pyplot as plt
import seaborn as sns
from calculator import Calculator


class ChartPlotter:
    def plot_prices(self, closing_prices):
        ax = plt.gca()
        columns = [c for c in closing_prices.columns if c not in 'Date']
        closing_prices.plot(kind='line',use_index=True,y=columns,ax=ax, title='Asset (Stock) Prices')
        plt.show()
        return ax

    def plot_returns(self, returns):
        ax = plt.gca()
        columns = [c for c in returns.columns if c not in 'Date']
        returns.plot(kind='line', use_index=True, y=columns, ax=ax, title='Asset (Stock) Returns')
        plt.show()
        return ax

    def plot_correlation_matrix(self, df):
        sns.heatmap(df,cmap='Blues', annot=True)
        plt.show()

    def plot_portfolios(self, df):
        fig = plt.figure()
        max_sharpe_ratio = Calculator.get_max_sharpe_ratio(df)
        min_risk = Calculator.get_min_risk(df)

        plt.scatter(df['Risk'], df['Return'], c=df['SharpeRatio'], cmap='viridis', edgecolors='red')
        x = max_sharpe_ratio['Risk']
        y = max_sharpe_ratio['Return']
        name = max_sharpe_ratio['Portfolio']

        plt.title(str(len(df)) + " Portfolios Risk-Return")
        plt.xlabel("Risk")
        plt.ylabel("Return")

        self.plot_single_point(x, y, 'Max Sharpe Ratio: ' + name, 'green')
        x = min_risk['Risk']
        y = min_risk['Return']
        name = min_risk['Portfolio']
        self.plot_single_point(x, y, 'Min Risk: ' + name, 'red')

        equal_allocations_portfolio = df.iloc[0,:]
        x = equal_allocations_portfolio['Risk']
        y = equal_allocations_portfolio['Return']
        name = 'EqualAllocationPortfolio'
        self.plot_single_point(x, y, 'Portfolio: ' + name, 'black')
        return fig

    def plot_single_point(self, x, y, title, colour):
        plt.scatter(x=x, y=y, c=colour, marker='D', s=200)
        plt.annotate(title,
                     (x, y),
                     textcoords="offset points",
                     xytext=(0, 10),
                     ha='center')

    def plot_efficient_frontier(self, data):
        plt.plot(data['Risk'], data['Return'], 'r-x')
