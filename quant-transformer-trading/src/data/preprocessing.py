from typing import Optional
import pandas as pd
from sklearn.preprocessing import MinMaxScaler

def normalize_data(df: pd.DataFrame, columns: Optional[list[str]] = None) -> pd.DataFrame:
    if columns is None:
        columns = df.columns.tolist()
    
    scaler = MinMaxScaler()
    df[columns] = scaler.fit_transform(df[columns])
    return df

def handle_missing_values(df: pd.DataFrame, method: str = 'ffill') -> pd.DataFrame:
    if method == 'ffill':
        return df.fillna(method='ffill')
    elif method == 'bfill':
        return df.fillna(method='bfill')
    elif method == 'drop':
        return df.dropna()
    else:
        raise ValueError("Unsupported method for handling missing values. Use 'ffill', 'bfill', or 'drop'.")

def feature_engineering(df: pd.DataFrame) -> pd.DataFrame:
    df['returns'] = df['close'].pct_change()
    df['volatility'] = df['returns'].rolling(window=21).std()
    df['moving_average'] = df['close'].rolling(window=21).mean()
    df.dropna(inplace=True)
    return df

def preprocess_data(df: pd.DataFrame) -> pd.DataFrame:
    df = handle_missing_values(df)
    df = normalize_data(df)
    df = feature_engineering(df)
    return df