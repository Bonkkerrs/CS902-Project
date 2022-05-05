import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

class ChartPlotter:
    def plot_prices(self, closing_prices):
        ax = plt.gca()
        columns = [c for c in closing_prices.columns if c not in 'Date']
        closing_prices.plot(kind='line',use_index=True,y=columns,ax=ax, title='Asset (Stock) Prices')
        plt.show()

    def plot_returns(self, returns):
        ax = plt.gca()
        columns = [c for c in returns.columns if c not in 'Date']
        returns.plot(kind='line', use_index=True, y=columns, ax=ax, title='Asset (Stock) Returns')
        plt.show()

    def plot_correlation_matrix(self, df):
        sns.heatmap(df,cmap='Blues', annot=True)
        plt.show()