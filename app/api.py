import os
import numpy as np
import pandas as pd
from src import logging
from fastapi import FastAPI
from src.Pipeline.prediction import PredictionPipeline
from  pydantic import BaseModel, Field
from typing import Literal



logging.info("log_start for app.py")

app = FastAPI()

pipeline = PredictionPipeline()

class InputData(BaseModel):
    ssc_p:float=Field(description="the  secondary_school (10th) percentage",ge=0,le=100,examples=['83.5'])
    ssc_b:Literal['Central','Others']=Field(description='the secondary school (10th) board')
    hsc_p:float=Field(description=' the higher secondary school (12th) percentage',ge=0,le=100,examples=['83.5'])
    hsc_b:Literal['Central','Others']=Field(description='the higher secondary school (12th) board')
    hsc_s:Literal['Commerce','Science','Arts']=Field(description=' 12th stream')
    degree_p:float=Field(description='degree percentage')
    degree_t: Literal["Sci&Tech", "Comm&Mgmt", "Others"]=Field(description='degree type')
    workex:Literal['Yes','No']=Field(description="previous work experience")
    etest_p:float=Field(descriptin='employability test percentage',ge=0,le=100)
    specialisation: Literal["Mkt&HR", "Mkt&Fin"]=Field(description='mba specialisation')
    mba_p:float=Field(description='mba score percentage',ge=0,le=100)

@app.get('/home')
def home():
    return 'hello welcome to home page.'

@app.post("/predict")
async def predict(data:InputData):
    input_data = data.model_dump()  # model_dump convert pydantic model to dictionary
                                    # i added other preprocessing step in prediciction.py itself
    logging.info('try to run api predict call')
    prediction = pipeline.predict(input_data)
    return {"status": prediction[0]}
    logging.info(' api call successful')







