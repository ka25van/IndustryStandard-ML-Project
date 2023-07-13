from datetime import datetime
import os,sys

from Insurance.exception import InsuranceException
from Insurance.logger import logging


FILE_NAME="insurance.csv"
TEST_FILE="test.csv"
TRAIN_FILE="train.csv"



#Creating a Training Pipeline to self
class TrainingPipelineConfig:
    def __init__(self):
        try:
            self.artifact_dir=os.path.join(os.getcwd(),"artifact",f"{datetime.now().strftime('%m%d%Y__%H%M%S')}")
        except Exception as e:
            raise InsuranceException(e, sys)

#We need the data from the database, so the first step is data ingestion, then have a directory for it, split the data into train and test
class DataIngestionConfig:
    def __init__(self, training_pipeline_config:TrainingPipelineConfig):
        try:
           self.database_name="Insurance"
           self.collection_name="Insurance_Info"
           self.data_ingestion_dir=os.path.join(training_pipeline_config.artifact_dir, "data_ingestion")  #data_ingestion folder is inside  artifact folder
           self.feature_store_file_path=os.path.join(self.data_ingestion_dir, "feature_store",FILE_NAME)   #File_Name file is inside feature_store folder which is insidedata_ingestion folder
           self.train_file_path=os.path.join(self.data_ingestion_dir, "train_data", TRAIN_FILE)
           self.test_file_path=os.path.join(self.data_ingestion_dir, "test_data", TEST_FILE)
           self.test_size=0.2
        except Exception as e:
            raise InsuranceException(e,sys)


# Convert data into dictonary
    def to_dict(self,)->dict:
        try:
            return self.__dict__
        except Exception  as e:
            raise InsuranceException(e,sys)   

class DataValidationConfig:
    def __init__(self,training_pipeline_config:TrainingPipelineConfig):
        self.data_validation_dir=os.path.join(training_pipeline_config.artifact_dir, "data_validation")
#since this is for validation, we need to create a report file where we can see the validated data
        self.report_file_path=os.path.join(self.data_validation_dir, "report.yaml")  #yaml/json/csv any format can be used
        self.missing_threshold:float=0.2 #for 20% of data to be dropped
        self.base_file_path=os.path.join("insurance.csv")
        