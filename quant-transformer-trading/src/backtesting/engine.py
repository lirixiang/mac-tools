from typing import List, Dict
import pandas as pd

class BacktestingEngine:
    def __init__(self, data: pd.DataFrame, initial_capital: float = 100000.0):
        self.data = data
        self.initial_capital = initial_capital
        self.portfolio_value = initial_capital
        self.positions = pd.DataFrame(columns=['Date', 'Symbol', 'Shares', 'Price'])
        self.trades = []

    def buy(self, date: str, symbol: str, shares: int, price: float):
        self.positions = self.positions.append({'Date': date, 'Symbol': symbol, 'Shares': shares, 'Price': price}, ignore_index=True)
        self.portfolio_value -= shares * price
        self.trades.append({'Date': date, 'Symbol': symbol, 'Shares': shares, 'Price': price, 'Action': 'BUY'})

    def sell(self, date: str, symbol: str, shares: int, price: float):
        if not self.positions[(self.positions['Symbol'] == symbol) & (self.positions['Shares'] >= shares)].empty:
            self.positions.loc[(self.positions['Symbol'] == symbol) & (self.positions['Shares'] >= shares), 'Shares'] -= shares
            self.portfolio_value += shares * price
            self.trades.append({'Date': date, 'Symbol': symbol, 'Shares': shares, 'Price': price, 'Action': 'SELL'})
        else:
            raise ValueError("Not enough shares to sell")

    def get_portfolio_value(self) -> float:
        return self.portfolio_value + self.get_current_positions_value()

    def get_current_positions_value(self) -> float:
        current_value = 0.0
        for _, position in self.positions.iterrows():
            current_price = self.data.loc[self.data['Date'] == position['Date'], position['Symbol']].values[0]
            current_value += current_price * position['Shares']
        return current_value

    def run_backtest(self, strategy: callable) -> List[Dict]:
        for index, row in self.data.iterrows():
            action = strategy(row)
            if action['type'] == 'buy':
                self.buy(row['Date'], action['symbol'], action['shares'], row[action['symbol']])
            elif action['type'] == 'sell':
                self.sell(row['Date'], action['symbol'], action['shares'], row[action['symbol']])
        return self.trades

    def get_trades(self) -> List[Dict]:
        return self.trades

    def reset(self):
        self.portfolio_value = self.initial_capital
        self.positions = pd.DataFrame(columns=['Date', 'Symbol', 'Shares', 'Price'])
        self.trades = []