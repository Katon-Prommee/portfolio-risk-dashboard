import yfinance as yf
import pandas as pd

def data():
    stocks = ['QQQ','SPY','GLD']
    data = yf.download(
        stocks,
        start="2005-01-01",
        end="2024-12-31",
        progress = False,
        auto_adjust = False
    )
    adj_close = data["Adj Close"]
    returns = data["Adj Close"].pct_change()
    #Clean the NaN 
    returns = returns.dropna()
    return returns, adj_close