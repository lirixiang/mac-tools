from src.backtesting.engine import BacktestEngine
from src.data.loaders import load_data
from src.strategies.signals import generate_signals
from src.models.transformer import TransformerModel
import argparse
import pandas as pd

def run_backtest(data_path: str, model_path: str, strategy: str, start_date: str, end_date: str) -> None:
    data = load_data(data_path)
    data = data[(data['date'] >= start_date) & (data['date'] <= end_date)]

    model = TransformerModel.load(model_path)
    signals = generate_signals(model, data)

    backtest_engine = BacktestEngine(data, signals)
    results = backtest_engine.run()

    print("Backtest Results:")
    print(results)

def main():
    parser = argparse.ArgumentParser(description="Run backtest for trading strategies")
    parser.add_argument("--data", required=True, help="Path to the historical data CSV file")
    parser.add_argument("--model", required=True, help="Path to the trained model file")
    parser.add_argument("--strategy", required=True, help="Trading strategy to use")
    parser.add_argument("--start", required=True, help="Start date for backtesting (YYYY-MM-DD)")
    parser.add_argument("--end", required=True, help="End date for backtesting (YYYY-MM-DD)")

    args = parser.parse_args()

    run_backtest(args.data, args.model, args.strategy, args.start, args.end)

if __name__ == "__main__":
    main()