import os
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from src import logging
from sklearn.preprocessing import OneHotEncoder, StandardScaler, LabelEncoder
from sklearn.compose import ColumnTransformer
from pathlib import Path
import joblib

class DataPreprocess:
    def __init__(self, config):
        self.config = config

    def load_file(self) -> pd.DataFrame:
        try: 
            logging.info('Loading CSV data...')
            df = pd.read_csv(self.config.data_path)
            logging.info('DataFrame loaded successfully.')

            logging.info('Starting preprocessing: dropping duplicates...')
            df = df.drop_duplicates()

            logging.info(f'Dropping columns: {self.config.col_to_drop}')
            df = df.drop(columns=self.config.col_to_drop, errors='ignore')

            logging.info('Splitting data into train and test sets...')
            X = df.drop(columns=[self.config.target_col])
            y = df[self.config.target_col]
            
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, 
                test_size=self.config.test_size, 
                random_state=42
            ) 
            
            cat_col = X_train.select_dtypes(include='object').columns.to_list()
            num_col = X_train.select_dtypes(include=np.number).columns.to_list()
            
            logging.info(f'Categorical columns: {cat_col}')
            logging.info(f'Numerical columns: {num_col}')

            preprocess = ColumnTransformer([
                ('cat_col', OneHotEncoder(sparse_output=False, handle_unknown='ignore'), cat_col),
                ('num_col', StandardScaler(), num_col)
            ],remainder='drop')
            
            logging.info('Fitting preprocessor on training data...')
            X_train_arr = preprocess.fit_transform(X_train)
            X_test_arr = preprocess.transform(X_test)

            logging.info('Fitting label encoder on targets...')
            lb = LabelEncoder()
            y_train_arr = lb.fit_transform(y_train)
            y_test_arr = lb.transform(y_test)

            # Ensure directories for outputs exist
            os.makedirs(os.path.dirname(self.config.label_pkl_path), exist_ok=True)
            os.makedirs(os.path.dirname(self.config.preprocess_pkl_path), exist_ok=True)
            os.makedirs(os.path.dirname(self.config.X_train_data_path), exist_ok=True)

            logging.info(f'Saving preprocessor to {self.config.preprocess_pkl_path}')
            joblib.dump(preprocess, self.config.preprocess_pkl_path)
            
            logging.info(f'Saving label encoder to {self.config.label_pkl_path}')
            joblib.dump(lb, self.config.label_pkl_path)

            # Convert processed numpy arrays back to DataFrames for CSV saving
            # We fetch feature names from column transformer if possible, or leave as default columns
            X_train_df = pd.DataFrame(X_train_arr)
            X_test_df = pd.DataFrame(X_test_arr)

            y_train_df = pd.DataFrame(y_train_arr, columns=[self.config.target_col])
            y_test_df = pd.DataFrame(y_test_arr, columns=[self.config.target_col])
            
            logging.info("Saving preprocessed datasets to disk...")
            X_train_df.to_csv(Path(self.config.X_train_data_path), index=False)
            X_test_df.to_csv(Path(self.config.X_test_data_path), index=False)
            y_train_df.to_csv(Path(self.config.y_train_data_path), index=False)
            y_test_df.to_csv(Path(self.config.y_test_data_path), index=False)
            
            logging.info('Preprocessing completed successfully.')
            return df
            
        except Exception as e:
            logging.exception("Exception occurred during preprocessing.")
            raise e