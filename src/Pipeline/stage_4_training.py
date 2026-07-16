from src.config.configuration import ConfigurationManager
from src.components.training import model_trainer
from src import logging

logging.info('####### STAGE 4 START #######')

class ModelTrainingPipeline:
    def __init__(self):
        pass

    def main(self):
        config=ConfigurationManager()
        model_training_config=config.get_model_trainer_config()
        model_training_instance=model_trainer(model_training_config)
        logging.info('running model_trainer instance and try to run stage 4 ')
        model_training_instance.run_optuna()
logging.info('########## STAGE 4 COMPLETED SUCCESSFULLY #######')

if __name__ == "__main__":
    pipeline = ModelTrainingPipeline()
    pipeline.main()