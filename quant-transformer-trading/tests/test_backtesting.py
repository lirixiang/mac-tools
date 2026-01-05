import pytest
from src.backtesting.engine import BacktestEngine
from src.backtesting.metrics import calculate_sharpe_ratio, calculate_max_drawdown

def test_backtest_engine_initialization():
    engine = BacktestEngine()
    assert engine is not None

def test_backtest_execution():
    engine = BacktestEngine()
    results = engine.run_backtest(strategy='dummy_strategy', data='dummy_data')
    assert results is not None
    assert 'returns' in results

def test_calculate_sharpe_ratio():
    returns = [0.01, 0.02, -0.01, 0.03]
    sharpe_ratio = calculate_sharpe_ratio(returns)
    assert isinstance(sharpe_ratio, float)

def test_calculate_max_drawdown():
    returns = [0.1, 0.2, -0.1, 0.05, -0.2]
    max_drawdown = calculate_max_drawdown(returns)
    assert isinstance(max_drawdown, float)