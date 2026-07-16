import os
from pathlib import Path
from src.utils.common import read_yaml, create_directory
from src.constants import schema_yaml_path, config_yaml_path, params_yaml_path
from src.entity.config_entity import (
    DataingestionConfig,
    DatapreprocessConfig,
    DatavalidationConfig,
    modeltrainerConfig,
    modelevaluationConfig,
    predictionpipelineConfig
)

class ConfigurationManager:
    def __init__(
        self,
        config_filepath = config_yaml_path,
        params_filepath = params_yaml_path,
        schema_filepath = schema_yaml_path
    ):
        self.config = read_yaml(config_filepath)
        self.params = read_yaml(params_filepath)
        self.schema = read_yaml(schema_filepath)

        create_directory(Path(self.config.artifacts_root))

    def get_data_ingestion_config(self) -> DataingestionConfig:
        config = self.config.data_ingestion
        params = self.params.data_ingestion

        create_directory(Path(config.root_dir))

        return DataingestionConfig(
            root_dir=Path(config.root_dir),
            url=str(config.url),
            data_path=Path(config.data_path),
            request_timeout=int(params.request_timeout)
        )

    def get_data_validation_config(self) -> DatavalidationConfig:
        config=self.config.data_validation
        return DatavalidationConfig(
                root_dir=Path(config.root_dir),
                data_path=Path(config.data_path),
                status_file=Path(config.status_file)
             
        )

    def get_data_preprocess_config(self) -> DatapreprocessConfig:
        config = self.config.data_preprocess
        schema = self.schema.preprocess
        params = self.params.data_preprocess

        create_directory(Path(config.root_dir))

        return DatapreprocessConfig(
            root_dir=Path(config.root_dir),
            data_path=Path(self.config.data_ingestion.data_path),
            test_size=float(params.test_size),
            X_train_data_path=Path(config.X_train_data_path),
            X_test_data_path=Path(config.X_test_data_path),
            y_train_data_path=Path(config.y_train_data_path),
            y_test_data_path=Path(config.y_test_data_path),
            target_col=str(schema.target_col),
            col_to_drop=list(schema.col_to_drop),
            label_pkl_path=Path(config.label_pkl_path),
            preprocess_pkl_path=Path(config.preprocess_pkl_path)
        )

    def get_model_trainer_config(self) -> modeltrainerConfig:
        config = self.config.model_trainer
        preprocess_config = self.config.data_preprocess
        params = self.params.optuna

        create_directory(Path(config.root_dir))

        return modeltrainerConfig(
            root_dir=Path(config.root_dir),
            train_data_path=Path(config.train_data_path),
            test_data_path=Path(config.test_data_path),
            model_path=Path(config.model_path),
            methods=list(params.methods),
            X_train_data_path=Path(preprocess_config.X_train_data_path),
            X_test_data_path=Path(preprocess_config.X_test_data_path),
            y_train_data_path=Path(preprocess_config.y_train_data_path),
            y_test_data_path=Path(preprocess_config.y_test_data_path),
            timeout=int(params.timeout),
            n_trials=int(params.n_trials),
            cv=int(params.cv),
            score=str(params.score)
        )

    def get_model_evaluation_config(self) -> modelevaluationConfig:
        config = self.config.model_evaluation
        preprocess_config = self.config.data_preprocess

        create_directory(Path(config.root_dir))

        return modelevaluationConfig(
            root_dir=Path(config.root_dir),
            X_test_data_path=Path(preprocess_config.X_test_data_path),
            y_test_data_path=Path(preprocess_config.y_test_data_path),
            model_path=Path(config.model_path),
            metric_path=Path(config.metric_path)
        )


    def get_prediction_pipeline_config(self)-> predictionpipelineConfig:
        config=self.config.prediction_pipeline

        return predictionpipelineConfig(
            model_path=Path(config.model_path),
            label_pkl_path=Path(config.label_pkl_path),
            preprocess_pkl_path=Path(config.preprocess_pkl_path)           

        )