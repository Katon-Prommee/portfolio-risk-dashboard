import yfinance as yf
import pandas as pd
import numpy as np

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

#Calculate daily return according to asset's weight
portfolio_returns = 0.5*returns["SPY"] + 0.3*returns["QQQ"] + 0.2*returns["GLD"]

#Calculate volatility
QQQ_volatility = returns["QQQ"].std() #daily
SPY_volatility = returns["SPY"].std() #daily
GLD_volatility = returns["GLD"].std() #daily
daily_portfolio_volatility = portfolio_returns.std()
annualize_portfolio_volatility = daily_portfolio_volatility*np.sqrt(252)
print(f"Portfolio Volatility :{daily_portfolio_volatility*100:.2f}, GLD Volatility :{GLD_volatility*100:.2f}, SPY Volatility :{SPY_volatility*100:.2f}, QQQ Volatility :{QQQ_volatility*100:.2f}")

#Calculate Value at Risk (VaR) with 99% level of confidence
confidence_level_99 = 0.99
confidence_level_95 = 0.95
alpha_99 = 1 - confidence_level_99
alpha_95 = 1 - confidence_level_95

#Historical VaR
VaR_99 = portfolio_returns.quantile(alpha_99)
VaR_95 = portfolio_returns.quantile(alpha_95)
print(f"Historical 1-day 99% VaR: {VaR_99*100:.2f}%") #-2.94%
print(f"Historical 1-day 95% VaR: {VaR_95*100:.2f}%") #-1.55%

#Calculate CVaR
CVaR_99 = portfolio_returns[portfolio_returns <= VaR_99].mean()
CVaR_95 = portfolio_returns[portfolio_returns <= VaR_95].mean()
print(f"Historical 1-day 99% CVaR: {CVaR_99*100:.2f}%") #-4.06%
print(f"Historical 1-day 95% CVaR: {CVaR_95*100:.2f}%") #-2.44%

#Calculate skewness and kurtosis
skew = portfolio_returns.skew()
kurt = portfolio_returns.kurtosis()
print(f"Skew: {skew:.3f}, Kurtosis: {kurt:.3f}")

#Find maximum drawdown
cumulative_returns = (1+portfolio_returns).cumprod()
cumulative_max = cumulative_returns.cummax()
drawdown = (cumulative_returns - cumulative_max)/cumulative_max
max_drawdown = drawdown.min()
print(f"Maximum Drawdown: {max_drawdown*100:.2f}%")

print("-------------------------------------------------------------------")

def stress_test(returns):

    print("available data : 2005-01-01 to 2024-12-31")
    print("For COVID Stress Test :")
    print("Start : 2020-02-15, End : 2020-04-15")
    print("For 2008 Financial Crisis Stress Test :")
    print("Start : 2008-09-01, End : 2008-12-31")

    while True :
        start = input("Enter start date (YYYY-MM-DD) :")
        end = input("Enter end date (YYYY-MM-DD) :")
        #Check if the date is availale or not
        try:
            start_date = pd.to_datetime(start)
            end_date = pd.to_datetime(end)
            if start_date > end_date :
                print("Please enter the correct date")
                continue
        
            period_returns = returns[start:end]

            if period_returns.empty:
                raise ValueError("No data in the selected date range")
            else :
                break
        except ValueError:
            print("Invalid date.")

    #Enter confidence level
    while True:
        try :
            n = float(input("Enter confidence level (ex. 99 for 99%) :"))
            if 0 < n < 100 :
                confidence_level = n/100
                break
            else:
                print("Please enter numer between 0 and 100")
        except ValueError :
            print("Please enter a number.")
    
    alpha = 1 - confidence_level
    period_returns = returns[start:end]
    volatility = float(period_returns.std()) #daily volatility

    #VaR / CVaR
    VaR = float(period_returns.quantile(alpha))
    CVaR = float(period_returns[period_returns <= VaR].mean())

    #max_dd
    cumulative_returns = (1+period_returns).cumprod()
    cumulative_max = cumulative_returns.cummax()
    drawdown = (cumulative_returns - cumulative_max)/cumulative_max
    max_dd = float(drawdown.min())

    print(f"Volatility = {volatility*100:.4f}%, VaR = {VaR*100:.4f}%, CVaR = {CVaR*100:.4f}%, Max Drawdown = {max_dd*100:.4f}%")

    return volatility, VaR, CVaR, max_dd

stress_test(portfolio_returns)