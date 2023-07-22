#In DataIngestion we split the data into train/yesy data, in DataValidation we validate them.
#In DataTransformation we ; show the missing values, Handle outliers, Handle Imbalanced data, convert cat-data to num-data

import sys
from Insurance.exception import InsuranceException
from Insurance.entity import config_entity,artifact_entity
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import RobustScaler
import pandas as pd
import numpy as np
from Insurance.config import TARGET_COLUMN
from sklearn.preprocessing import LabelEncoder
from Insurance import utils


class DataTransformation:


    def __init__(self,data_transformation_config:config_entity.DataTransformationConfig,
                    data_ingestion_artifact:artifact_entity.DataIngestionArtifact): #DataIngestion here because; we get the data from ingestion and further it is taken into transformation
        try:
            self.data_transformation_config=data_transformation_config
            self.data_ingestion_artifact=data_ingestion_artifact
        except Exception as e:
            raise InsuranceException(e, sys)



    @classmethod #To transform the data we need to import the pipeline from sklearn
    def get_data_transformer_object(cls)->Pipeline: # Create cls class
        try:
            simple_imputer = SimpleImputer(strategy='constant', fill_value=0) #Impute missing vales we use simple imputer
            robust_scaler =  RobustScaler() #Removes median in Outliers
            pipeline = Pipeline(steps=[
                    ('Imputer',simple_imputer),
                    ('RobustScaler',robust_scaler)
                ])
            return pipeline
    

        except Exception as e:
            raise InsuranceException(e, sys)
 
#####################################################################################################

    def initiate_data_transformation(self,)->artifact_entity.DataTransformationArtifact:
        try:
            
            #Reading the train and test data
            train_df=pd.read_csv(self.data_ingestion_artifact.train_file_path)
            test_df=pd.read_csv(self.data_ingestion_artifact.test_file_path)

            #Feature selection by dropping the Target column i.e 'expense'
            #Like splitting into Independent data and dependent data
            #Dependent data
            input_feature_train_df=train_df.drop(TARGET_COLUMN, axis=1)
            input_feature_test_df=test_df.drop(TARGET_COLUMN, axis=1)

            #InDependent data
            target_train_df=train_df[TARGET_COLUMN]
            target_test_df=test_df[TARGET_COLUMN]

            #Label encoding is to convert categorical variables into numerical format.
            label_encoder= LabelEncoder()

            #Transforming the target data
            #squeeze() function is used when we want to remove single-dimensional entries from the shape of an array.
            target_feature_train_arr = target_train_df.squeeze()
            target_feature_test_arr = target_test_df.squeeze()

            #Now we need to make both the train and test data to numerical
            for col in input_feature_train_df.columns:  #For columns in train
                if input_feature_test_df[col].dtypes=='O':  #if there is data type object in test then transform the train and test to numerical
                    input_feature_train_df[col]=label_encoder.fit_transform(input_feature_train_df[col])
                    input_feature_test_df[col]=label_encoder.fit_transform(input_feature_test_df[col])
                else:                                       #Else if no object type write the same columns as it is
                     input_feature_train_df[col]=input_feature_train_df[col]
                     input_feature_test_df[col]=input_feature_test_df[col]


            #SMOTE method can be used to solve the imbalance problem; since there is no imbalance data we might not be needing this
            transformation_pipleine = DataTransformation.get_data_transformer_object()
            transformation_pipleine.fit(input_feature_train_df)

            input_feature_train_arr = transformation_pipleine.transform(input_feature_train_df)
            input_feature_test_arr = transformation_pipleine.transform(input_feature_test_df)
            
            train_arr = np.c_[input_feature_train_arr, target_feature_train_arr ]  ##c_ means it conatenates
            test_arr = np.c_[input_feature_test_arr, target_feature_test_arr]


            utils.save_numpy_array_data(file_path=self.data_transformation_config.transformed_train_path,
                                        array=train_arr)

            utils.save_numpy_array_data(file_path=self.data_transformation_config.transformed_test_path,
                                        array=test_arr)


            utils.save_object(file_path=self.data_transformation_config.transform_object_path,
             obj=transformation_pipleine)

            utils.save_object(file_path=self.data_transformation_config.target_encoder_path,
            obj=label_encoder)



            data_transformation_artifact = artifact_entity.DataTransformationArtifact(
                transform_object_path=self.data_transformation_config.transform_object_path,
                transformed_train_path = self.data_transformation_config.transformed_train_path,
                transformed_test_path = self.data_transformation_config.transformed_test_path,
                target_encoder_path = self.data_transformation_config.target_encoder_path

            )

            return data_transformation_artifact




        except Exception as e:
            raise InsuranceException(e, sys)
 



    

