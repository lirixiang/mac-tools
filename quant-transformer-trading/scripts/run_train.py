import argparse
import yaml
from src.training.train import train_model

def load_config(config_path: str):
    with open(config_path, 'r') as file:
        config = yaml.safe_load(file)
    return config

def main():
    parser = argparse.ArgumentParser(description="Run training for the quantitative trading model.")
    parser.add_argument('--config', type=str, default='src/config/default.yaml', help='Path to the configuration file.')
    args = parser.parse_args()

    config = load_config(args.config)
    train_model(config)

if __name__ == "__main__":
    main()