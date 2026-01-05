import pytest
from src.data.loaders import load_data
from src.data.preprocessing import preprocess_data

def test_load_data():
    data = load_data('path/to/data.csv')
    assert data is not None
    assert len(data) > 0

def test_preprocess_data():
    raw_data = load_data('path/to/data.csv')
    processed_data = preprocess_data(raw_data)
    assert processed_data is not None
    assert 'feature_column' in processed_data.columns
    assert processed_data['feature_column'].isnull().sum() == 0  # Check for missing values