from src import logging
from src.Pipeline.stage_1_ingestion import DataIngestionTrainingPipeline
from src.Pipeline.stage_2_validation import DataValidationTrainingPipeline
from src.Pipeline.stage_3_preprocess import DataPreprocessTrainingPipeline
from src.Pipeline.stage_4_training import ModelTrainingPipeline
from src.Pipeline.stage_5_evaluation import EvaluationTrainingPipeline


STAGE_NAME = "Data Ingestion stage"
try:
   logging.info(f">>>>>> stage {STAGE_NAME} started <<<<<<") 
   data_ingestion = DataIngestionTrainingPipeline()
   data_ingestion.main()
   logging.info(f">>>>>> stage {STAGE_NAME} completed <<<<<<\n\nx==========x")
except Exception as e:
        logging.exception(e)
        raise e


STAGE_NAME = "Data Validation stage"
try:
   logging.info(f">>>>>> stage {STAGE_NAME} started <<<<<<") 
   data_validation = DataValidationTrainingPipeline()
   data_validation.main()
   logging.info(f">>>>>> stage {STAGE_NAME} completed <<<<<<\n\nx==========x")
except Exception as e:
        logging.exception(e)
        raise e



STAGE_NAME = "Data Preprocess stage"
try:
   logging.info(f">>>>>> stage {STAGE_NAME} started <<<<<<") 
   data_preprocess= DataPreprocessTrainingPipeline()
   data_preprocess.main()
   logging.info(f">>>>>> stage {STAGE_NAME} completed <<<<<<\n\nx==========x")
except Exception as e:
        logging.exception(e)
        raise e



STAGE_NAME = "Model Trainer stage"
try:
   logging.info(f">>>>>> stage {STAGE_NAME} started <<<<<<") 
   model_training = ModelTrainingPipeline()
   model_training.main()
   logging.info(f">>>>>> stage {STAGE_NAME} completed <<<<<<\n\nx==========x")
except Exception as e:
        logging.exception(e)
        raise e




STAGE_NAME = "Model evaluation stage"
try:
   logging.info(f">>>>>> stage {STAGE_NAME} started <<<<<<") 
   data_evaluation = EvaluationTrainingPipeline()
   data_evaluation.main()
   logging.info(f">>>>>> stage {STAGE_NAME} completed <<<<<<\n\nx==========x")
except Exception as e:
        logging.exception(e)
        raise e

