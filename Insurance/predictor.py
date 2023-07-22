#Here we write a code so that whenever a new model is brought up it reates a new folder 
#It compares with the old model and accepts/rejects the model based on the accuracy 

import os
from typing import Optional
from Insurance.entity.config_entity import MODEL_FILE,TRANSFORMER_OBJECT_FILE,TARGET_ENCODER_OBJECT_FILE


class ModelResolver:
    def __init__(self,model_registry:str="saved_model",   #creating a folder name so that we can compare it with old model; comparatively which has the better accurac can be deployed
                transformer_dir_name="transformer",       #Similar to data_transformation
                target_encoder_dir_name="target_encoder",      #After transformation we need to encode the data
                model_dir_name="model"                    #Finally as a model file
                ):
                self.model_registry=model_registry
                os.makedirs(self.model_registry, exist_ok=True)     #if the saved_model in above is not created, then this line will do it
                self.transformer_dir_name=transformer_dir_name
                self.target_encoder_dir_name=target_encoder_dir_name
                self.model_dir_name=model_dir_name

    #To get the latest path of the directory created for the new model
    def get_latest_dir_path(self)->Optional[str]:
        try:
            dir_names = os.listdir(self.model_registry)  
            if len(dir_names)==0:
                return None
            dir_names = list(map(int,dir_names))  #run times->0/1/2/3......
            latest_dir_name = max(dir_names)
            return os.path.join(self.model_registry,f"{latest_dir_name}")
        except Exception as e:
            raise e

        #Model Path
    def get_latest_model_path(self):
        try:
            latest_dir=self.get_latest_dir_path()
            if latest_dir is None:
                raise Exception(f"Directory not found")
            return os.path.join(latest_dir,self.model_dir_name,MODEL_FILE)
        except Exception as e:
            raise e
    
        #Transformer Path
    def get_latest_transformer_path(self):
        try:
            latest_dir=self.get_latest_dir_path()
            if latest_dir is None:
                raise Exception(f"Director not found")
            return os.path.join(latest_dir,self.transformer_dir_name,TRANSFORMER_OBJECT_FILE)
        except Exception as e:
            raise e

        #Target Path
    def get_latest_target_encoder_path(self):
        try:
            latest_dir=self.get_latest_dir_path()
            if latest_dir is None:
                raise Exception(f"Director not found")
            return os.path.join(latest_dir,self.target_encoder_dir_name,TARGET_ENCODER_OBJECT_FILE)
        except Exception as e:
            raise e

#Now we need to save the above files respectively
    def get_latest_save_dir_path(self)->str:
        try:
            latest_dir = self.get_latest_dir_path()
            if latest_dir == None:
                return os.path.join(self.model_registry,f"{0}")
            latest_dir_num = int(os.path.basename(self.get_latest_dir_path()))
            return os.path.join(self.model_registry,f"{latest_dir_num + 1}")
        except Exception as e:
            raise e

    def get_latest_save_model_path(self):
        try:
            latest_dir = self.get_latest_save_dir_path()
            return os.path.join(latest_dir,self.model_dir_name,MODEL_FILE)
        except Exception as e:
            raise e

    def get_latest_save_transformer_path(self):
        try:
            latest_dir = self.get_latest_save_dir_path()
            return os.path.join(latest_dir,self.transformer_dir_name,TRANSFORMER_OBJECT_FILE)
        except Exception as e:
            raise e

    def get_latest_save_target_encoder_path(self):
        try:
            latest_dir = self.get_latest_save_dir_path()
            return os.path.join(latest_dir,self.target_encoder_dir_name,TARGET_ENCODER_OBJECT_FILE)
        except Exception as e:
            raise e