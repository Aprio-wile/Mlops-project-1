import os
import pandas as pd
from src import logging
import xgboost
import catboost
import lightgbm
from sklearn.model_selection import cross_val_score
from pathlib import Path
import pickle
import optuna


# Set optuna logging to warning to avoid cluttering the logs

optuna.logging.set_verbosity(optuna.logging.WARNING)

class model_trainer:

    def __init__(self, config):
        self.config = config
    
    def run_optuna(self):

        logging.info("Loading X_train and y_train datasets...")

        # Load datasets once outside the objective function to improve speed

        X_train = pd.read_csv(Path(self.config.X_train_data_path))
        y_train = pd.read_csv(Path(self.config.y_train_data_path))
        
        # Ensure y_train is a 1D array/series for sklearn/classifiers

        if isinstance(y_train, pd.DataFrame):
            y_train = y_train.iloc[:, 0]

        def objective(trial):
            classifier_name = trial.suggest_categorical('classifier', list(self.config.methods))
               
            if classifier_name == 'xgboost':

                params = {
                    'n_estimators': trial.suggest_int('xgb_n_estimators', 100, 1000, step=100),
                    'max_depth': trial.suggest_int('xgb_max_depth', 3, 10),
                    'learning_rate': trial.suggest_float('xgb_learning_rate', 0.001, 0.1, log=True),
                    'subsample': trial.suggest_float('xgb_subsample', 0.5, 1.0),
                    'colsample_bytree': trial.suggest_float('xgb_colsample_bytree', 0.5, 1.0),
                    'eval_metric': 'logloss'
                }
                model = xgboost.XGBClassifier(**params)

            elif classifier_name == 'lightgbm':

                params = {
                    'n_estimators': trial.suggest_int('lgbm_n_estimators', 100, 1000, step=100),
                    'max_depth': trial.suggest_int('lgbm_max_depth', 3, 10),
                    'learning_rate': trial.suggest_float('lgbm_learning_rate', 0.001, 0.1, log=True),
                    'subsample': trial.suggest_float('lgbm_subsample', 0.5, 1.0),
                    'colsample_bytree': trial.suggest_float('lgbm_colsample_bytree', 0.5, 1.0),
                    'num_leaves': trial.suggest_int('lgbm_num_leaves', 2, 256),
                    'objective': 'binary',
                    'metric': 'binary_logloss',
                    'verbose': -1
                }
                model = lightgbm.LGBMClassifier(**params)
                
            elif classifier_name == 'catboost':  

                params = {
                    'iterations': trial.suggest_int('cb_iterations', 100, 1000, step=100),
                    'depth': trial.suggest_int('cb_depth', 3, 10),
                    'learning_rate': trial.suggest_float('cb_learning_rate', 0.001, 0.1, log=True),
                    'l2_leaf_reg': trial.suggest_float('cb_l2_leaf_reg', 1e-8, 10.0, log=True),
                    'loss_function': 'Logloss',
                    'verbose': 0
                }
                model = catboost.CatBoostClassifier(**params)

            else:

                logging.error(f"Unknown method {classifier_name} suggested by Optuna.")
                raise ValueError(f"Method {classifier_name} is not supported.")

            score = cross_val_score(
                model,
                X_train,
                y_train,
                cv=self.config.cv,
                scoring=f"{self.config.score}"
            ).mean()

            return score

        logging.info("Starting Optuna hyperparameter optimization...")


        # MLFLOW logging

        with mlflow.start_run()
            study = optuna.create_study(direction="maximize")
            study.optimize(objective, n_trials=self.config.n_trials, timeout=self.config.timeout)    

            mlflow.log_params(study.best_params)
            mlflow.log_metric('best_score',study.best_value)
            mlflow.log_param('model_name',best_model_name)

            classifier_name = best_params['classifier']

            if classifier_name == "catboost":
                mlflow.catboost.log_model(model, "model")

            elif classifier_name == "lightgbm":
                mlflow.lightgbm.log_model(model, "model")

            
            elif classifier_name == "xgboost":
                mlflow.xgboost.log_model(model, "model")

            else:
                mlflow.sklearn.log_model(model, "model")

        logging.info(f"Optimization finished. Best accuracy score: {study.best_value:.4f}")

        best_params = study.best_trial.params
        classifier_name = best_params['classifier']

        logging.info(f"Best classifier: {classifier_name}")

        if classifier_name == 'xgboost':

            model_class = xgboost.XGBClassifier
            prefix = 'xgb_'

        elif classifier_name == 'lightgbm':

            model_class = lightgbm.LGBMClassifier
            prefix = 'lgbm_'

        elif classifier_name == 'catboost':

            model_class = catboost.CatBoostClassifier
            prefix = 'cb_'

        else:

            logging.exception(f"Classifier name {classifier_name} does not exist in mapping.")
            raise ValueError(f"Classifier {classifier_name} is invalid.")

        # Filter parameters relevant to the best classifier and remove the prefix

        logging.info('Filtering best parameters...')
        filtered_params = {k.replace(prefix, ''): v for k, v in best_params.items() if k.startswith(prefix)}
        
        # Add objective/metric defaults for lightgbm/catboost to make it clean

        if classifier_name == 'lightgbm':
            filtered_params.update({'objective': 'binary', 'metric': 'binary_logloss', 'verbose': -1})

        elif classifier_name == 'catboost':
            filtered_params.update({'loss_function': 'Logloss', 'verbose': 0})

        elif classifier_name == 'xgboost':
            filtered_params.update({'eval_metric': 'logloss'})
            
        logging.info(f"Filtered parameters: {filtered_params}")

        # Instantiate and train the final model on full training set

        logging.info("Training final model with best hyperparameters...")
        final_model = model_class(**filtered_params)
        final_model.fit(X_train, y_train)


        # Ensure directory for model saving exists

        model_path = Path(self.config.model_path)
        os.makedirs(model_path.parent, exist_ok=True)

        logging.info(f"Saving final model to {model_path}...")

        with open(model_path, 'wb') as f:
            pickle.dump(final_model, f)

        logging.info("Model saved successfully.")
