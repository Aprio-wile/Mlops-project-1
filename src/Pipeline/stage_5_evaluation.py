from src.config.configuration import ConfigurationManager
from src.components.evaluation import ModelEvaluation
from src import logging

logging.info('##### STAGE 5 START ######')
class EvaluationTrainingPipeline:
    def __init__(self):
        pass
    
    def main(self):
        config=ConfigurationManager()
        model_evaluation_config=config.get_model_evaluation_config()
        model_evaluation_instance=ModelEvaluation(model_evaluation_config)
        model_evaluation_instance.evaluate()
logging.info('############## STAGE 5 COMPLETED ##############')

if __name__ == "__main__":
    pipeline = EvaluationTrainingPipeline()
    pipeline.main()