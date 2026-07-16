import os
from pathlib import Path
from datetime import datetime
from src import logging

class DataValidation:
    def __init__(self, config):
        self.config = config

    def file_validation(self):
        data_path = Path(self.config.data_path)
        if not data_path.exists():
            raise FileNotFoundError(
                f"File at {data_path} was not found."
            )
        logging.info(f"{data_path} file checked successfully.")
    
    def validate(self):
        try:
            self.file_validation()
        except Exception as e:
            logging.exception("Exception occurred during data validation.")
            # Write a failed status to status_file
            try:
                os.makedirs(os.path.dirname(self.config.status_file), exist_ok=True)
                with open(Path(self.config.status_file), 'w') as f:
                    f.write(f"status: FAILED\n")
                    f.write(f"timestamp: {datetime.now()}\n")
                    f.write(f"error: {str(e)}\n")
            except Exception:
                pass
                raise e
        else:
            time = datetime.now()
            logging.info('Generating status file...')
            with open(Path(self.config.status_file), 'w') as f:
                f.write("status: OK\n")
                f.write(f"timestamp: {time}\n")
            logging.info("Status file generated successfully.")