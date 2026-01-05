from typing import Any, Dict
import pandas as pd

def load_csv_data(file_path: str) -> pd.DataFrame:
    """Load financial data from a CSV file."""
    return pd.read_csv(file_path)

def load_data_from_api(api_url: str, params: Dict[str, Any]) -> pd.DataFrame:
    """Load financial data from an API."""
    import requests
    response = requests.get(api_url, params=params)
    response.raise_for_status()
    return pd.DataFrame(response.json())

def load_data(file_path: str, source: str = 'csv', api_url: str = '', params: Dict[str, Any] = None) -> pd.DataFrame:
    """Load financial data from specified source."""
    if source == 'csv':
        return load_csv_data(file_path)
    elif source == 'api':
        return load_data_from_api(api_url, params)
    else:
        raise ValueError("Unsupported data source. Use 'csv' or 'api'.")