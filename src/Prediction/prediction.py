import joblib
import numpy as np
import pandas as pd
from pathlib import Path
from src.constants import config_yaml_path
from src import logging
from src.config.configuration import ConfigurationManager
import numpy as np




class PredictionPipeline:
    def __init__(self):
        config=ConfigurationManager()
        config=config.get_prediction_pipeline_config()        
        self.model = joblib.load(Path(config.model_path))
        self.preprocessor =joblib.load(Path(config.preprocess_pkl_path))
        self.labelencoder=joblib.load(Path(config.label_pkl_path))

    
    def predict(self, data):
        # Ensure data is properly structured into a DataFrame (handling dictionary/JSON input format)
        logging.info('try to convert input data into pd.DataFrame format')
        if isinstance(data, dict):
            data = pd.DataFrame([data])
        else:
            data = pd.DataFrame(data)

        data=data.replace(0,np.nan)
        data=self.preprocessor.transform(data)
        data=pd.DataFrame(data)
        prediction = self.labelencoder.inverse_transform(self.model.predict(data))

        return prediction
