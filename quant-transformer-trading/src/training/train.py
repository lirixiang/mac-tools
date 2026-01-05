from __future__ import annotations

import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader
from datasets.timeseries_dataset import TimeSeriesDataset
from models.transformer import TransformerModel
from training.losses import CustomLoss
from utils.logging import setup_logging

def train_model(config: dict) -> None:
    setup_logging(config['logging'])

    # Load dataset
    train_dataset = TimeSeriesDataset(config['data']['train'])
    train_loader = DataLoader(train_dataset, batch_size=config['training']['batch_size'], shuffle=True)

    # Initialize model, loss function, and optimizer
    model = TransformerModel(config['model'])
    criterion = CustomLoss()
    optimizer = optim.Adam(model.parameters(), lr=config['training']['learning_rate'])

    model.train()
    for epoch in range(config['training']['num_epochs']):
        total_loss = 0
        for batch in train_loader:
            optimizer.zero_grad()
            outputs = model(batch['input'])
            loss = criterion(outputs, batch['target'])
            loss.backward()
            optimizer.step()
            total_loss += loss.item()

        avg_loss = total_loss / len(train_loader)
        print(f'Epoch [{epoch + 1}/{config["training"]["num_epochs"]}], Loss: {avg_loss:.4f}')

    # Save the trained model
    torch.save(model.state_dict(), config['model']['save_path'])

if __name__ == "__main__":
    import yaml

    with open('config/default.yaml', 'r') as file:
        config = yaml.safe_load(file)

    train_model(config)