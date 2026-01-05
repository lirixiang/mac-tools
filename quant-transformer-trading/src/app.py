from flask import Flask
import yaml
import os

def load_config(config_path: str):
    with open(config_path, 'r') as file:
        config = yaml.safe_load(file)
    return config

def create_app():
    app = Flask(__name__)
    
    # Load configuration
    config_path = os.path.join(os.path.dirname(__file__), 'config', 'default.yaml')
    config = load_config(config_path)
    app.config.update(config)

    # Initialize components (e.g., models, data loaders) here
    # Example: app.model = YourModelClass(config['model'])

    @app.route('/')
    def home():
        return "Welcome to the Quantitative Trading Model API!"

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)