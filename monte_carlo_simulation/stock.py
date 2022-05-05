import datetime as dt
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import pandas_datareader.data as web

class Stock:
    def __init__(self, ticker, days_back):
        self.ticker = ticker
        self.days_back = days_back

