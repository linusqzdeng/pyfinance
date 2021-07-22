"""A program that fetches historical stock prices of
selected equities from database and generates the efficient
frontier and capital market line."""


import scipy.optimize as spo
import pandas as pd
import numpy as np
import yfinance as yf
import matplotlib.pyplot as plt
from datetime import datetime as dt

plt.style.use("ggplot")


# selected equities and time frame
stocks = ["AAPL", "GOOG", "TSLA", "BABA", "ETH-USD"]
start = dt(2017, 12, 31)
end = dt(2021, 1, 1)

# fetch stock prices
stock_prices = yf.download(stocks, start, end)["Adj Close"].dropna(axis=0)
stock_returns = stock_prices.pct_change().dropna(axis=0)

# fetch risk free rate (US 10-year T-bills)
risk_free = yf.download("^TNX", start, end)["Adj Close"].mean() / 100


# generate random weights for each equity
# np.random.seed(1000)
portfolio_returns = []
portfolio_volatilities = []
for _ in range(2500):
    weights = np.random.random(len(stocks))
    weights /= sum(weights)

    # construct the portfolio
    rt = np.sum(stock_returns.mean() * weights) * 252
    var = np.dot(np.dot(weights.T, stock_returns.cov() * 252), weights)
    std = np.sqrt(var)

    portfolio_returns.append(rt)
    portfolio_volatilities.append(std)

portfolio_returns = np.array(portfolio_returns)
portfolio_volatilities = np.array(portfolio_volatilities)


# visualise all possible portfolio combinations
plt.figure(figsize=(12, 9))
plt.scatter(
    portfolio_volatilities, portfolio_returns, c=(portfolio_returns - risk_free) / portfolio_volatilities, marker="o"
)
plt.xlabel("Risk")
plt.ylabel("Return")
plt.title("Market Portfolio")
plt.colorbar(label="Sharpe Ratio")

plt.show()

# optimisation
def portfolio_stats(weights, rf):
    """Returns an array of portfolio statistics, including
    portfolio return, volatility and sharpe ratio."""
    weights = np.array(weights)
    p_rt = np.sum(stock_returns.mean() * weights) * 252
    p_std = np.sqrt(np.dot(np.dot(weights.T, stock_returns.cov() * 252), weights))
    sharpe = (p_rt - rf) / p_std

    return np.array([p_rt, p_std, sharpe])


def get_sharpe(weights):
    """Returns the negative sharpe ratio."""
    return -portfolio_stats(weights, risk_free)[2]


def get_variance(weights):
    """Returns the portfolio variance."""
    return portfolio_stats(weights, risk_free)[1] ** 2


# portfolio with the highest sharpe ratio
cons = {"type": "eq", "fun": lambda x: np.sum(x) - 1}  # constraints for weights
bnds = [(0, 1) for _ in range(len(stocks))]
equal_weights = len(stocks) * [1.0 / len(stocks)]

sharpe_opt = spo.minimize(get_sharpe, equal_weights, method="SLSQP", constraints=cons, bounds=bnds)
variance_opt = spo.minimize(get_variance, equal_weights, method="SLSQP", constraints=cons, bounds=bnds)

print("Optimal portfolio with the maximum sharpe ratio")
print("=" * 50)
print(sharpe_opt)
print("\n")
print("Optimal portfolio with the minimum variance")
print("=" * 50)
print(variance_opt)

sharpe_opt_weights = sharpe_opt["x"]
variance_opt_weights = variance_opt["x"]

print(
    f"""
    Market portfolio information:
    Expected return: {portfolio_stats(sharpe_opt_weights, risk_free)[0]:2%}
    Volatility: {portfolio_stats(sharpe_opt_weights, risk_free)[1]:2%}

    Minimum variance portfolio information:
    Expected return: {portfolio_stats(variance_opt_weights, risk_free)[0]:2%}
    Volatility: {portfolio_stats(variance_opt_weights, risk_free)[1]:2%}
"""
)

# calculate the portfolios on efficient frontier
target_rt = np.linspace(0.39, 0.8, num=100)
target_std = []
for rt in target_rt:
    # 1. portfolio return equals to target
    # 2. weights sum up to 1
    cons = (
        {"type": "eq", "fun": lambda x: np.sqrt(portfolio_stats(x, risk_free)[0]) - rt},
        {"type": "eq", "fun": lambda x: np.sum(x) - 1},
    )
    ef_port = spo.minimize(get_variance, equal_weights, method="SLSQP", constraints=cons, bounds=bnds)
    target_std.append(ef_port["fun"])

target_std = np.array(target_std)

# exhibit the efficient frontier
plt.figure(figsize=(12, 9))
plt.scatter(target_std, target_rt, c=(target_rt - risk_free) / target_std, marker="o")
plt.xlabel("Risk")
plt.ylabel("Return")
plt.title("Efficient Frontier")
plt.colorbar(label="Sharpe Ratio")

plt.show()

