#For the data to be stored in the database
import pymongo;
import pandas as pd;
import json;  #Since MongoDb stores data in json format


uri = "mongodb+srv://kavankaverappa5:<password>@cluster1.jl2dxpz.mongodb.net/?retryWrites=true&w=majority"  #Set the pasword to numerics so you won't we needing to go through the error
client = pymongo.MongoClient(uri)

#Collecting Data from
DATA_FILE_PATH =(r"C:\Users\Kaverappa Mapanamada\Desktop\DataSciencePractice\ML-IndustryStand\IndustryStandard-ML-Project\insurance.csv")

#Creating Database name
DATABASE_NAME= "Insurance"

#Creating a collection name which store the data
COLLECTION_NAME = "Insurance_Info"

if __name__ ==  "__main__":
    df = pd.read_csv(DATA_FILE_PATH)
    print(f"Row & Column:{df.shape}")
    #Row & Column:(1338, 7)

    #Let's remove the index0,,2,3... 
    df.reset_index(drop=True, inplace= True)

    #To get the data in json format so we need to transform and call values as needed(T = transpose), As MongoDb is key and value pair
    json_data=list(json.loads(df.T.to_json()).values()) #Here  we need to transpose df to json format and get the values in list
    
    #insert the values in MDb database
    client[DATABASE_NAME][COLLECTION_NAME].insert_many(json_data)