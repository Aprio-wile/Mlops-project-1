import os
import requests
from src import logging
from pathlib import Path
from src.utils.common import create_directory

class DataIngestion:
    def __init__(self, config):
        self.config = config

    def download_and_save_data(self) -> None:
        """Downloads the data from the configured URL and saves it locally."""
        try:
            # Ensure the directory exists
            create_directory(Path(self.config.root_dir))
            
            logging.info(f"Sending GET request to retrieve data from: {self.config.url}")
            # Corrected timeout argument syntax
            response = requests.get(self.config.url, timeout=self.config.request_timeout)
            response.raise_for_status()
            
            logging.info("Data download request successful.")
            
            # Ensure parent directory of data path exists
            data_path = Path(self.config.data_path)
            os.makedirs(data_path.parent, exist_ok=True)
            
            with open(data_path, "wb") as f:
                f.write(response.content)
            logging.info(f"Data file saved successfully to {data_path}")
            
        except Exception as e:
            logging.exception("Exception occurred during data ingestion.")
            raise e
