from src.config.configuration import ConfigurationManager
from src.components.preprocess import DataPreprocess
from src import logging

logging.info('####### STAGE 3 START #######')

class DataPreprocessTrainingPipeline:
    def __init__(self):
        pass

    def main(self):
        config=ConfigurationManager()
        data_preprocess_config=config.get_data_preprocess_config()
        Data_preprocess_instance=DataPreprocess(data_preprocess_config)  
        logging.info('running Datapreprocess instance and try to run stage 2 ')    
        Data_preprocess_instance.load_file()
logging.info('########## STAGE 3 COMPLETED SUCCESSFULLY #######')

if __name__ == "__main__":
    pipeline = DataPreprocessTrainingPipeline()
    pipeline.main()