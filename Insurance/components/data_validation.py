# Here we have to find the data types
# Remove unwanted values
# data cleaning by removing null values

# So building a pipeline so that the code auto reads the data and replace the null values. This pipeline can be used for other data too.

import sys
from typing import Optional
from Insurance.config import TARGET_COLUMN
import pandas as pd
import numpy as np
from Insurance import utils
from Insurance.exception import InsuranceException
from Insurance.logger import logging
from Insurance.entity import config_entity
from Insurance.entity import artifact_entity
from scipy.stats import ks_2samp


class DataValidation:
    def __init__(self, data_validation_config: config_entity.DataValidationConfig,
                 data_ingestion_artifact: artifact_entity.DataIngestionArtifact):
        try:
            self.data_validation_config = data_validation_config
            self.data_ingestion_artifact = data_ingestion_artifact
            self.validation_error = dict()
        except Exception as e:
            raise InsuranceException(e, sys)

######################################################################################################################
 
    def drop_missing_values_columns(self, df: pd.DataFrame, report_key_name: str) -> Optional[pd.DataFrame]:
        try:
            # setting the threshold so that if there are more than 20% of missing data then drop it
            # from config_entity DataValidationConfig
            threshold = self.data_validation_config.missing_threshold
            # finding the null values
            null_report = df.isna().sum()/df.shape[0]

            logging.info(
                f"selecting column name which contains null above to {threshold}")
            # we get the null values from the null report
            drop_column_names = null_report[null_report > threshold].index

            logging.info(f"Columns to drop: {list(drop_column_names)}")
            self.validation_error[report_key_name] = list(
                drop_column_names)  # report key validates the dataframe
            # axis=1 means column wise
            df.drop(list(drop_column_names), axis=1, inplace=True)


# if there are no null values in the column
            if len(df.columns) == 0:  # columns in df
                return None
            else:
                return df

        except Exception as e:
            raise InsuranceException(e, sys)

######################################################################################################################
 

    def is_required_columns_exists(self, base_df: pd.DataFrame, current_df: pd.DataFrame, report_key_name: str) -> bool:
        try:
            # comparing the columns from base dataset(insurance.csv) and with the test/train.csv i.e(current)and removing the columns that is not required
            base_columns = base_df
            current_columns = current_df

            missing_columns = []  # creating an empty list
            for base_column in base_columns:
                if base_column not in current_columns:
                    logging.info(f"Column: [{base_column} is not available.]")
                    # if base column is not there in current column then add the base column into the missing column
                    missing_columns.append(base_column)

            # now to check ig there are any null vaues in the missing_columns
            if len(missing_columns) > 0:
                self.validation_error[report_key_name] = missing_columns
                return False  # if miss_col > 0
            else:
                return True

        except Exception as e:
            raise InsuranceException(e, sys)


######################################################################################################################
 


# Data drift is unexpected and undocumented changes to data structure that is a result of modern data architectures.


    def data_drift(self, base_df: pd.DataFrame, current_df: pd.DataFrame, report_key_name: str):
        try:
            drift_report = dict()

            base_columns = base_df.columns
            current_columns = current_df.columns

            for base_column in base_columns:
                base_data, current_data = base_df[base_column], current_df[base_column]

        # to check hypothesis, so to do the distribution we need to import the scipy library
        # ks_2samp for goodness of fit.
                same_distribution = ks_2samp(base_data, current_data)

            if same_distribution.pvalue > 0.05:  # if the p value is > 0.05 then accept the null hypothesis
                      drift_report[base_column] = {
                       "pvalues": float(same_distribution.pvalue),
                       "same_distribution": True
            }
            else:
                drift_report[base_column] = {
                "pvalues": float(same_distribution.pvalue),
                "same_distribution": False
            }

            self.validation_error[report_key_name] = drift_report
        except Exception as e:
            raise InsuranceException(e, sys)


######################################################################################################################
 

    def initiate_data_validation(self)->artifact_entity.DataValidationArtifact:
        try:
            #for base data
            logging.info(f"Reading base dataframe")
            base_df = pd.read_csv(self.data_validation_config.base_file_path)
            base_df.replace({"na":np.NAN},inplace=True)#replacing na with NAN
            logging.info(f"Replace na value in base df")
            #Dropping missing values by calling missing_values_columns 
            logging.info(f"Drop null values colums from base df")
            base_df=self.drop_missing_values_columns(df=base_df,report_key_name="missing_values_within_base_dataset")

            #for train and test data
            logging.info(f"Reading train dataframe")
            train_df = pd.read_csv(self.data_ingestion_artifact.train_file_path)  #Since train/test file is added in dataingestionconfig we can directly call t from the artifact
            logging.info(f"Reading test dataframe")
            test_df = pd.read_csv(self.data_ingestion_artifact.test_file_path)

            #Dropping missing values by calling missing_values_columns 
            train_df = self.drop_missing_values_columns(df=train_df,report_key_name="missing_values_within_train_dataset")
            test_df = self.drop_missing_values_columns(df=test_df,report_key_name="missing_values_within_test_dataset")
        

        #Utils file here because, if any new updates done by the client than 
            exclude_columns = [TARGET_COLUMN]
            base_df = utils.convert_columns_float(df=base_df, exclude_columns=exclude_columns)
            train_df = utils.convert_columns_float(df=train_df, exclude_columns=exclude_columns)
            test_df = utils.convert_columns_float(df=test_df, exclude_columns=exclude_columns)


            logging.info(f"Is all required columns present in train df")
            train_df_columns_status = self.is_required_columns_exists(base_df=base_df, current_df=train_df,report_key_name="missing_columns_within_train_dataset")
            logging.info(f"Is all required columns present in test df")
            test_df_columns_status = self.is_required_columns_exists(base_df=base_df, current_df=test_df,report_key_name="missing_columns_within_test_dataset")

            if train_df_columns_status:
                logging.info(f"As all column are available in train df hence detecting data drift")
                self.data_drift(base_df=base_df, current_df=train_df,report_key_name="data_drift_within_train_dataset")
            if test_df_columns_status:
                logging.info(f"As all column are available in test df hence detecting data drift")
                self.data_drift(base_df=base_df, current_df=test_df,report_key_name="data_drift_within_test_dataset")
          
            #write the report
            logging.info("Write report in yaml file")
            utils.write_yaml_file(file_path=self.data_validation_config.report_file_path,
            data=self.validation_error)

            data_validation_artifact = artifact_entity.DataValidationArtifact(report_file_path=self.data_validation_config.report_file_path,)
            logging.info(f"Data validation artifact: {data_validation_artifact}")
            return data_validation_artifact

        except Exception as e:
            raise InsuranceException(e, sys)
