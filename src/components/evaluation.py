import os
import pandas as pd
import json
from src import logging
import pickle
from pathlib import Path
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

class ModelEvaluation:
    def __init__(self, config):
        self.config = config

    def evaluate(self):
        try:
            logging.info("Loading test datasets for evaluation...")
            X_test = pd.read_csv(Path(self.config.X_test_data_path))
            y_test = pd.read_csv(Path(self.config.y_test_data_path))

            logging.info(f"Loading trained model from {self.config.model_path}...")
            with open(Path(self.config.model_path), 'rb') as f:
                model = pickle.load(f)

            logging.info("Generating predictions on test data...")
            y_pred = model.predict(X_test)

            logging.info("Calculating performance metrics...")
            # Using binary classification metrics as target is binary ('status' - placed vs not placed)
            accuracy = accuracy_score(y_test, y_pred)
            # average='binary' works since we have a binary classification task
            precision = precision_score(y_test, y_pred, average='binary', zero_division=0)
            recall = recall_score(y_test, y_pred, average='binary', zero_division=0)
            f1 = f1_score(y_test, y_pred, average='binary', zero_division=0)

            metrics_dict = {
                "accuracy": float(accuracy),
                "precision": float(precision),
                "recall": float(recall),
                "f1_score": float(f1)
            }

            logging.info(f"Evaluation Metrics: {metrics_dict}")

            # Ensure directory for metrics exists
            metric_path = Path(self.config.metric_path)
            os.makedirs(metric_path.parent, exist_ok=True)

            logging.info(f"Saving evaluation metrics to {metric_path}...")
            with open(metric_path, 'w') as f:
                json.dump(metrics_dict, f, indent=4)
                
            logging.info("Model evaluation completed successfully.")
            return metrics_dict

        except Exception as e:
            logging.exception("Exception occurred during model evaluation.")
            raise e
