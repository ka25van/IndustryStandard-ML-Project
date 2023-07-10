from Insurance.components.data_ingestion import DataIngestion
from Insurance.logger import logging
from Insurance.exception import InsuranceException
import os, sys
from Insurance.utils import get_collection_as_dataframe
from Insurance.entity.config_entity import DataIngestionConfig
from Insurance.entity import config_entity



if __name__== "__main__":
    try:
        
        training_pipeline_config=config_entity.TrainingPipelineConfig()

    #DATA INGESTION
       
        data_ingestion_config  = config_entity.DataIngestionConfig(training_pipeline_config=training_pipeline_config)
        print(data_ingestion_config.to_dict())  #Need result in dictornary format, when run the code we can confirm it
        data_ingestion = DataIngestion(data_ingestion_config=data_ingestion_config)
        data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
    except Exception as e:
        print(e)
