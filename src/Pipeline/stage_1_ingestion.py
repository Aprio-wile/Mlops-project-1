from src.config.configuration import ConfigurationManager
from src.components.ingestion import DataIngestion
from src import logging

logging.info('####### STAGE 1 START #######')

class DataIngestionTrainingPipeline:
    def __init__(self):
        pass

    def main(self):
        config=ConfigurationManager()
        data_ingestion_config=config.get_data_ingestion_config()
        Data_ingest_instance=DataIngestion(data_ingestion_config)
        logging.info('running DataINgestion instance and try to run stage 1 ')
        Data_ingest_instance.download_and_save_data()
logging.info('########## STAGE 1 COMPLETED SUCCESSFULLY #######')

if __name__ == "__main__":
    pipeline = DataIngestionTrainingPipeline()
    pipeline.main()