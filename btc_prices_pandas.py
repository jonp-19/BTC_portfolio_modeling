#%%
import pandas as pd
import matplotlib.pyplot as plt

#TODO docstring needs work.  Formatting is wrong.
def model_btc_portfolio(start_date, end_date, initial_invest, bank, high_mark, low_mark):
    """Inputs:
        start_date must be "YYYY-MM-DD"
        end_date must be "YYYY_MM_DD"
        initial_invest is the funds used for initial investment
        bank is amount of funds set aside for additional purchases
        high mark is the highest portfolio value will go before selling
        low mark is the lowest portfolio value will go before buying
        Returns:
        dataframe with dates, close_prices, current_holdings_list, shares, balance
        final total holdings amount
        """
    # create a dataframe of BTC price information
    df = pd.read_csv('data/BTC-USD.csv', parse_dates=['Date'])

    # create dataframe limited to between dates
    dated_frame = df[df.Date.between(start_date, end_date)]

    # create date and close price series
    close_prices = (dated_frame.loc[:, 'Close'])
    dates = (dated_frame.loc[:, 'Date'])

    # set initial lists
    shares, balance, = [], []
    current_holdings_list = []

    # Run though dates that were set earlier.  Purchase, set, or hold based on 
    # value of portfolio.  Try/except sets up initial purchase.
    for x,y in zip(dates, close_prices):
        try:
            current_holdings = shares[-1] * y
            current_holdings_list.append(float(current_holdings))
        except IndexError:
            initial_purchase = float(initial_invest/close_prices[:1])
            shares.append(initial_purchase)
            current_holdings = shares[-1] * y
            current_holdings_list.append(float(current_holdings))
            balance.append(bank)
        else:
            if current_holdings > high_mark:
                sell_btc = (current_holdings - high_mark)/y
                realized_profit = sell_btc * y
                shares.append(shares[-1] - sell_btc)
                balance.append((balance[-1]) + (realized_profit))
            elif current_holdings < low_mark and balance[-1] > 0:
                buy_btc = (low_mark - current_holdings)/y
                spent_now = buy_btc * y
                shares.append(shares[-1] + buy_btc)
                balance.append((balance[-1]) - (spent_now))
            else:
                shares.append(shares[-1])
                balance.append(balance[-1])

    new_df = pd.DataFrame(list(zip(dates, close_prices, current_holdings_list, shares, balance)))
    print(new_df)

    total_balance = list((a + b for a,b in zip(current_holdings_list, balance)))
    print(total_balance[-1])

#TODO need to fix plotting.  can't seem to use lists created by first function
def plot_balance(dates, total_balance):
    # Plot the BTC close prices
    plt.style.use('seaborn')
    fig, ax = plt.subplots()
    ax.plot(dates, total_balance, c='red', alpha=0.5)
    #ax.fill_between(sitka_dates, sitka_highs, sitka_lows, facecolor='blue', alpha=0.1)

    # Format plot.
    ax.set_title(f"BTC Balance Retention", fontsize=24)
    ax.set_xlabel('', fontsize=16)
    fig.autofmt_xdate()
    ax.set_ylabel("USD", fontsize=16)
    ax.tick_params(axis='both', which='major', labelsize=16)
    #plt.ylim([(min(sitka_lows+death_lows)-5), (max(sitka_highs+death_highs)+5)])

    plt.show()

model_btc_portfolio("2021-04-24", "2021-04-28", 5000, 5000, 5200, 5000)

# %%
