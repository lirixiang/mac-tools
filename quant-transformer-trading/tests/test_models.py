import pytest
import pandas as pd
from src.models.transformer import TransformerModel
from src.data.loaders import load_data

@pytest.fixture
def sample_data():
    data = {
        'feature1': [1.0, 2.0, 3.0, 4.0],
        'feature2': [5.0, 6.0, 7.0, 8.0],
        'target': [0, 1, 0, 1]
    }
    return pd.DataFrame(data)

def test_transformer_model_initialization():
    model = TransformerModel(input_dim=2, output_dim=1, num_heads=2, num_layers=2)
    assert model is not None
    assert model.input_dim == 2
    assert model.output_dim == 1
    assert model.num_heads == 2
    assert model.num_layers == 2

def test_model_forward(sample_data):
    model = TransformerModel(input_dim=2, output_dim=1, num_heads=2, num_layers=2)
    inputs = sample_data[['feature1', 'feature2']].values
    outputs = model(inputs)
    assert outputs.shape == (4, 1)

def test_load_data():
    data = load_data('path/to/data.csv')
    assert isinstance(data, pd.DataFrame)
    assert not data.empty

def test_data_shape(sample_data):
    assert sample_data.shape == (4, 3)  # 4 rows, 3 columns (2 features + target)