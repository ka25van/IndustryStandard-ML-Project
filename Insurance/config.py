#To create an environment which stores key valed paires and configured info of the mongodb database
import pymongo
import pandas as pd
import numpy as np
import os,sys
import json
from dataclasses import dataclass


@dataclass #to make it static
class EnvironmentVariable:
    mongo_db_url = os.getenv("MONGO_DB_URL")


env_var=EnvironmentVariable()
mongo_client = pymongo.MongoClient(env_var.mongo_db_url)
TARGET_COLUMN="expenses"            #Targeting a specific column
print(env_var.mongo_db_url)