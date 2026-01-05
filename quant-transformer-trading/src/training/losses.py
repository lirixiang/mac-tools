from typing import Any
import torch
import torch.nn as nn

class MeanSquaredErrorLoss(nn.Module):
    def __init__(self):
        super(MeanSquaredErrorLoss, self).__init__()

    def forward(self, predictions: torch.Tensor, targets: torch.Tensor) -> torch.Tensor:
        return nn.functional.mse_loss(predictions, targets)

class CustomLoss(nn.Module):
    def __init__(self, alpha: float = 0.5):
        super(CustomLoss, self).__init__()
        self.alpha = alpha
        self.mse_loss = MeanSquaredErrorLoss()

    def forward(self, predictions: torch.Tensor, targets: torch.Tensor) -> torch.Tensor:
        mse = self.mse_loss(predictions, targets)
        # Example of adding a custom penalty term
        penalty = self.alpha * torch.mean(torch.abs(predictions - targets))
        return mse + penalty

def get_loss_function(loss_name: str, **kwargs: Any) -> nn.Module:
    if loss_name == "mse":
        return MeanSquaredErrorLoss()
    elif loss_name == "custom":
        return CustomLoss(**kwargs)
    else:
        raise ValueError(f"Unknown loss function: {loss_name}")