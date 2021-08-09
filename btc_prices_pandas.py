#%%
import pandas as pd
import matplotlib.pyplot as plt

# create a dataframe of BTC price information
df = pd.read_csv('data/BTC-USD.csv', parse_dates=['Date'])

# create dataframe limited to between dates
dated_frame = df[df.Date.between('2015-01-01', '2021-04-28')]

# create date and close price series
close_prices = (dated_frame.loc[:, 'Close'])
dates = (dated_frame.loc[:, 'Date'])

# set initial parameters
initial_invest = 5000
bank = 10000

# set buy and sell limits
high_mark = 5000
low_mark = 4000

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

# %%
