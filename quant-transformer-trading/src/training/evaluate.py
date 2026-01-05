from typing import Any, Dict
import numpy as np
import pandas as pd
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

def evaluate_model(model: Any, X: pd.DataFrame, y: pd.Series) -> Dict[str, float]:
    """
    Evaluate the performance of the trained model on the given dataset.

    Parameters:
    - model: The trained model to evaluate.
    - X: Features of the dataset (input).
    - y: True labels of the dataset (output).

    Returns:
    A dictionary containing evaluation metrics.
    """
    predictions = model.predict(X)
    
    accuracy = accuracy_score(y, predictions)
    precision = precision_score(y, predictions, average='weighted')
    recall = recall_score(y, predictions, average='weighted')
    f1 = f1_score(y, predictions, average='weighted')

    return {
        "accuracy": accuracy,
        "precision": precision,
        "recall": recall,
        "f1_score": f1
    }