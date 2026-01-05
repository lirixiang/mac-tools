from typing import List

def calculate_sharpe_ratio(returns: List[float], risk_free_rate: float = 0.0) -> float:
    excess_returns = [r - risk_free_rate for r in returns]
    return sum(excess_returns) / (len(excess_returns) ** 0.5)

def calculate_max_drawdown(equity_curve: List[float]) -> float:
    max_drawdown = 0.0
    peak = equity_curve[0]
    
    for value in equity_curve:
        if value > peak:
            peak = value
        drawdown = (peak - value) / peak
        max_drawdown = max(max_drawdown, drawdown)
    
    return max_drawdown

def calculate_cumulative_return(returns: List[float]) -> float:
    cumulative_return = 1.0
    for r in returns:
        cumulative_return *= (1 + r)
    return cumulative_return - 1

def calculate_win_rate(trades: List[float]) -> float:
    if not trades:
        return 0.0
    wins = sum(1 for trade in trades if trade > 0)
    return wins / len(trades)

def calculate_average_trade(trades: List[float]) -> float:
    if not trades:
        return 0.0
    return sum(trades) / len(trades)