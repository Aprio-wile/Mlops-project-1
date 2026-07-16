from src.config.configuration import ConfigurationManager
from src.components.validation import DataValidation
from src import logging

logging.info('####### STAGE 2 START #######')

class DataValidationTrainingPipeline:
    def __init__(self):
        pass

    def main(self):
        config=ConfigurationManager()
        data_validation_config=config.get_data_validation_config()
        Data_validate_instance=DataValidation(data_validation_config)
        logging.info('running Datavalidation instance and try to run stage 2 ')
        Data_validate_instance.validate()
logging.info('########## STAGE 2 COMPLETED SUCCESSFULLY #######')

if __name__ == "__main__":
    pipeline = DataValidationTrainingPipeline()
    pipeline.main()