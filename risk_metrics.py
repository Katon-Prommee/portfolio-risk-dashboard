import numpy as np
def risk_return_metrics(returns):
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

    return portfolio_returns, daily_portfolio_volatility, annualize_portfolio_volatility, VaR_99, VaR_95, CVaR_99, CVaR_95, skew, kurt, max_drawdown