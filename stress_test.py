import pandas as pd

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