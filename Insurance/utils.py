#To read database in the local we are doing this here in utils
import pandas as pd
import numpy as np
import os, sys
from Insurance.exception import InsuranceException
from Insurance.config import mongo_client
from Insurance.logger import logging
import yaml

def get_collection_as_dataframe(database_name:str, collection_name:str)->pd.DataFrame:
    #fetching data from the mongodb database
    try:
        logging.info(f"Reading data from database: {database_name}, Collection: {collection_name}")
        df=pd.DataFrame(list(mongo_client[database_name][collection_name].find()))
        logging.info(f"Finding columns: {df.columns}")
        if "_id" in df.columns: #Dropping column id from the dataframe
            logging.info(f"Drop columns: _id")
            df=df.drop("_id", axis=1)
            logging.info(f"Rows and columns after dropping :{df.shape}")
        return df


    except Exception as e:
        raise InsuranceException(e, sys)

def write_yaml_file(file_path,data:dict):
    try:
        file_dir = os.path.dirname(file_path)
        os.makedirs(file_dir,exist_ok=True)
        with open(file_path,"w") as file_writer:  #w means write
            yaml.dump(data,file_writer)
    except Exception as e:
        raise InsuranceException(e, sys)


def convert_columns_float(df:pd.DataFrame,exclude_columns:list)->pd.DataFrame:
    try:
        for column in df.columns:
            if column not in exclude_columns:
                if df[column].dtypes != 'O': #not object type
                    df[column]=df[column].astype('float') #change it to float 
        return df
    except Exception as e:
        raise e