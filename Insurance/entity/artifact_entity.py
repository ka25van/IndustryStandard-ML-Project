import os, sys


#Here we are declaring in which format we must recieve the file
class DataIngestionArtifact:
    feature_store_file_path:str
    train_file_path:str
    test_file_path:str