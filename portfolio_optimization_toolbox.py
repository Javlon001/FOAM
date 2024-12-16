import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import newton


# Define function to plot efficient frontier
def plot_efficient_frontier(df, stocks, portfolio_returns, portfolio_stds, minimum_variance_portfolio_return,
                            minimum_variance_portfolio_std, label_curve, label_portfolio):
    # Compute standard deviations of stocks
    stock_stds = df[stocks].std()
    stock_returns = df[stocks].mean()

    # Create figure 
    plt.figure(figsize=(10, 6), dpi=200)

    # Visualize stocks
    plt.scatter(stock_stds, stock_returns, alpha=0.5)

    # Visualize minimum variance curve
    plt.gca().plot(portfolio_stds,
                   portfolio_returns,
                   'o-', color='gray', alpha=0.2,
                   linewidth=5, label=label_curve)

    # Visualize efficient frontier
    portfolio_returns = np.array(portfolio_returns)
    portfolio_stds = np.array(portfolio_stds)
    idx = portfolio_returns >= minimum_variance_portfolio_return
    plt.gca().plot(portfolio_stds[idx],
                   portfolio_returns[idx],
                   'b-', markersize=5, alpha=0.4, label='Efficient frontier')

    # Visualize index
    plt.gca().plot(df['.SSMI'].std(),
                   df['.SSMI'].mean(),
                   'ro', label='SMI')

    # Visualize minimum variance portfolio
    plt.gca().plot(minimum_variance_portfolio_std,
                   minimum_variance_portfolio_return,
                   'go', label=label_portfolio)

    # Add axis labels
    plt.xlabel('Standard deviation')
    plt.ylabel('Expected return')

    # Add names of stocks
    x_offset = pd.Series(0.0003, index=stocks, dtype=float)
    y_offset = pd.Series(0, index=stocks, dtype=float)

    # Adjust offests of specific stocks
    y_offset['NOVN.S'] = 0.00015
    y_offset['ZURN.S'] = -0.00015

    for name in stocks:
        plt.gca().annotate(name.split('.')[0], (stock_stds[name] + x_offset[name],
                                                stock_returns[name] + y_offset[name]),
                           alpha=0.8, ha='left', va='center')

    plt.xlim(minimum_variance_portfolio_std * 0.9, stock_stds.max() * 1.1)
    min_return = portfolio_returns.min()
    abs_min_return = np.abs(min_return)
    plt.ylim(min_return - abs_min_return * 0.5, stock_returns.max() * 1.3)

    # Add legend
    plt.legend(loc='upper left')


# Define function to compute forward rate
def get_forward_rate(r_t, r_tau, t, tau):
    return ((1 + r_tau) ** tau / (1 + r_t) ** t) ** (1 / (tau - t)) - 1


# Define function to compute price of a bond from spot rates
def get_price(spot_rates, cashflows):
    periods = cashflows.index
    denominator = np.power(1 + spot_rates[periods], periods)
    return (cashflows / denominator).sum()


# Define function to compute price difference (assuming flat term structure)
def get_price_difference(rate, cashflows, bond_price):
    rates = pd.Series(rate, index=cashflows.index)
    return bond_price - get_price(rates, cashflows)


# Define function to compute yield-to-maturity
def get_ytm(cashflows, bond_price):
    ytm = newton(get_price_difference, 0.01,
                 args=(cashflows, bond_price))
    return ytm


# Define function that generates cashflows of coupon bond
def get_cashflows(face_value, time_to_maturity, coupon, num_periods):
    cashflows = pd.Series(0, index=np.arange(1, num_periods + 1))
    cashflows.loc[:time_to_maturity] = face_value * coupon
    cashflows.loc[time_to_maturity] += face_value
    return cashflows


# Define function that computes duration of a bond
def get_dollar_duration(rate, cashflows):
    periods = cashflows.index
    denominator = (1 + rate) ** (periods + 1)
    return -(periods * cashflows / denominator).sum()


def get_modified_duration(rate, cashflows):
    rates = pd.Series(rate, index=cashflows.index)
    price = get_price(rates, cashflows)
    dollar_duration = get_dollar_duration(rate, cashflows)
    return -dollar_duration / price


# Define function that computes duration of a bond
def get_fisher_weil_duration(spot_rates, cashflows):
    price = get_price(spot_rates, cashflows)
    periods = cashflows.index
    denominator = (1 + spot_rates[periods]) ** (periods + 1)
    return (periods * cashflows / denominator).sum() / price


# Define function that computes convexity of a bond
def get_convexity(spot_rates, cashflows):
    price = get_price(spot_rates, cashflows)
    periods = cashflows.index
    denominator = (1 + spot_rates[periods]) ** (periods + 2)
    discounted_cashflows = (periods * (periods + 1) * cashflows) / denominator
    return discounted_cashflows.sum() / price


# Define function that estimates price change
def get_price_change(price, duration, delta, convexity=0):
    term_1 = -duration * price * delta
    term_2 = (convexity * price * delta ** 2) / 2
    return term_1 + term_2


# Define function that estimates price
def get_price_estimate(price, duration, delta, convexity=0):
    return price + get_price_change(price, duration, delta, convexity)
