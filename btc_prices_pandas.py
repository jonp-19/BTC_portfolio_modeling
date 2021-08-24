#%%
#TODO is datetime import still necessary
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt
from pandas.core.frame import DataFrame

#TODO docstring needs work.  Formatting is wrong.
class BTCModel(object):
    """Class for modeling portfolio balances of BTC"""
    def __init__(self, start_date: datetime, end_date: datetime, initial_invest: int, bank: int, high_mark: int, low_mark: int):
        self.start_date = start_date
        self.end_date = end_date
        self.initial_invest = initial_invest
        self.bank = bank
        self.high_mark = high_mark
        self.low_mark = low_mark
        
        # create a dataframe of BTC price information
        self.df = pd.read_csv('data/BTC-USD.csv', parse_dates=['Date'])

        # create dataframe limited to between dates
        self.dated_frame = self.df[self.df.Date.between(self.start_date, self.end_date)]

        # create date and close price series
        self.close_prices = (self.dated_frame.loc[:, 'Close'])
        self.dates = (self.dated_frame.loc[:, 'Date'])

        # set initial lists
        self.shares, self.balance, self.current_holdings_list = [], [], []

    # Get current holdings
    def getCurrentHoldings(self, shares, y):
            self.current_holdings = self.shares[-1] * y
            self.current_holdings_list.append(float(self.current_holdings))
            return self.current_holdings
    
    # Make initial purchase.  Trying without arguments.
    def makeInitialPurchase(self):
        self.initial_purchase = float(self.initial_invest/self.close_prices[:1])
        self.shares.append(self.initial_purchase)
        self.current_holdings = self.shares[-1] * self.y
        self.current_holdings_list.append(float(self.current_holdings))
        self.balance.append(self.bank)

    def holdBTC(self):
        self.shares.append(self.shares[-1])
        self.balance.append(self.balance[-1])

    def sellBTC(self):
        self.sell_btc = (self.current_holdings - self.high_mark)/self.y
        self.realized_profit = self.sell_btc * self.y
        self.shares.append(self.shares[-1] - self.sell_btc)
        self.balance.append((self.balance[-1]) + (self.realized_profit))

    def buyBTC(self):
        self.buy_btc = (self.low_mark - self.current_holdings)/self.y
        self.spent_now = self.buy_btc * self.y
        self.shares.append(self.shares[-1] + self.buy_btc)
        self.balance.append((self.balance[-1]) - (self.spent_now))
    
    # Run though dates that were set earlier.  Purchase, set, or hold based on 
    # value of portfolio.  Try/except sets up initial purchase.
    def createBalance(self):
        for self.x, self.y in zip(self.dates, self.close_prices):
            try:
                self.getCurrentHoldings(self.shares, self.y)
            except IndexError:
                self.makeInitialPurchase()
            else:
                if self.current_holdings > self.high_mark:
                    self.sellBTC()
                elif self.current_holdings < self.low_mark and self.balance[-1] > 0:
                    self.buyBTC()
                else:
                    self.holdBTC()

        self.getTotalBalance(self.dates, self.close_prices, self.current_holdings_list, self.shares, self.balance)

    def getTotalBalance(self, dates, close_prices, current_holdings_list, shares, balance):
        self.new_df = pd.DataFrame(list(zip(self.dates, self.close_prices, self.current_holdings_list, self.shares, self.balance)))
        print(self.new_df)
        self.new_df.to_csv(f'{self}BTC_growth.csv')

        self.total_balance = list((a + b for a,b in zip(self.current_holdings_list, self.balance)))
        print(self.total_balance[-1])

#model_btc_portfolio("2015-04-24", "2021-04-28", 5000, 5000, 5200, 5000)
# %%
