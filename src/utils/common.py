import os
import yaml
import json
from src import logging
import pickle as pkl
from pathlib import Path
from box.exceptions import BoxValueError
from box import ConfigBox

# Define ensure_annotations as a no-op decorator to avoid compatibility issues on Python 3.14+
def ensure_annotations(func):
    return func

@ensure_annotations
def read_yaml(path_to_yaml: Path) -> ConfigBox:
    """Reads a YAML file and returns its content as a ConfigBox for dot-notation access."""
    try:
        with open(path_to_yaml) as yaml_file:
            content = yaml.safe_load(yaml_file)
            logging.info(f"YAML file: {path_to_yaml} loaded successfully")
            if content is None:
                return ConfigBox({})
            return ConfigBox(content)
    except BoxValueError:
        raise ValueError("YAML file is empty")
    except Exception as e:
        raise e

@ensure_annotations
def create_directory(dir_path: Path) -> None:
    """Creates a directory at the specified path if it doesn't already exist."""
    try:
        os.makedirs(dir_path, exist_ok=True)
        logging.info(f"Directory created or already exists at: {dir_path}")
    except Exception as e:
        logging.error(f"Failed to create directory at {dir_path}: {e}")
        raise e

class PortableBox(dict):
    """A pure-Python dictionary wrapper that allows dot notation access."""
    def __getattr__(self, key):
        try:
            value = self[key]
            # If the inner value is a nested dictionary, wrap it too!
            if isinstance(value, dict):
                return PortableBox(value)
            return value
        except KeyError:
            raise AttributeError(f"'PortableBox' object has no attribute '{key}'")

    def __setattr__(self, key, value):
        self[key] = value

def get_model_params_dict(model) -> dict:
    """Extracts hyperparameters as a clean dictionary from any of the standard frameworks."""
    model_class_name = model.__class__.__name__

    # 1. CatBoost
    if "CatBoost" in model_class_name:
        return model.get_all_params()

    # 2. XGBoost
    elif "XGB" in model_class_name:
        return model.get_params()

    # 3. LightGBM
    elif "LGBM" in model_class_name:
        return model.get_params()

    else:
        raise ValueError(f"Unsupported model type: {model_class_name}")

def save_model_params_json(model_path: Path, json_path: Path) -> None:
    """Loads a pickled model, extracts its hyperparameters, and saves them to a JSON file."""
    try:
        with open(model_path, 'r') as f:
            model = pkl.load(f)

        params = get_model_params_dict(model)

        os.makedirs(os.path.dirname(json_path), exist_ok=True)
        with open(json_path, 'w') as f:
            json.dump(params, f, indent=4)
        logging.info(f"Model parameters successfully saved to {json_path}")
    except Exception as e:
        logging.error(f"Error saving model parameters to JSON: {e}")
        raise e