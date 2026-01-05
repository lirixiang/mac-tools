from typing import List
import numpy as np
import pandas as pd

class SignalGenerator:
    def __init__(self, model_predictions: pd.Series):
        self.model_predictions = model_predictions

    def generate_signals(self) -> pd.Series:
        signals = pd.Series(index=self.model_predictions.index, data=0)

        # Generate buy signals (1) when the prediction is positive
        signals[self.model_predictions > 0] = 1

        # Generate sell signals (-1) when the prediction is negative
        signals[self.model_predictions < 0] = -1

        return signals

def backtest_signals(signals: pd.Series, prices: pd.Series) -> List[float]:
    returns = (prices.pct_change() * signals.shift()).dropna()
    cumulative_returns = (1 + returns).cumprod() - 1
    return cumulative_returns.tolist()