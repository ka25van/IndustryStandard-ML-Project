from datetime import datetime
from Insurance.exception import InsuranceException
from Insurance.logger import logging
import numpy as np
import pandas as pd
from Insurance.predictor import ModelResolver
import os
import sys
from Insurance.utils import load_object

PREDICTION_DIR="prediction"  #Making a file name 


def start_batch_prediction(input_file_path):
    try:
        os.makedirs(PREDICTION_DIR, exist_ok=True)    #creating a dir for prediction_dir, if it exists then fine
        model_resolver=ModelResolver(model_registry="saved_model")   #selects best from saved_models

        #Data loading
        df=pd.read_csv(input_file_path)    
        df.replace({"na":np.NAN}, inplace=True )   #to replace if any null values are present

        #Data Validation 
        #By looking into the save_models folder we consider transformer and targetencoder files
        transformer= load_object(
            file_path=model_resolver.get_latest_transformer_path())  
        target_encoder=load_object(file_path=model_resolver.get_latest_target_encoder_pat())

        
        
        input_feature_names = list(transformer.feature_names_in_)
        for i in input_feature_names:       
            if df[i].dtypes =='object':   #if i is of only object in trransformer
                df[i] =target_encoder.fit_transform(df[i])  #Similarly for i object in target_encoder

        #Now we need to add the simplified input _feature_names  into anew object        
        input_arr = transformer.transform(df[input_feature_names])

        #For prediction we need to call the model 
        model = load_object(file_path=model_resolver.get_latest_model_path()) #call
        prediction = model.predict(input_arr)     #prediction

        #Adding a column named prediction in the dataset with the prediction values from above
        df["prediction"]=prediction

        prediction_file_name = os.path.basename(input_file_path).replace(".csv",f"{datetime.now().strftime('%m%d%Y__%H%M%S')}.csv")  #converting the file to .csv + date_time
        prediction_file_path = os.path.join(PREDICTION_DIR,prediction_file_name)
        df.to_csv(prediction_file_path,index=False,header=True)

        return prediction_file_path

    except Exception as e:
        raise(InsuranceException(e,sys))