from dataclasses import dataclass
import os, sys


#Here we are declaring in which format we must recieve the file
@dataclass
class DataIngestionArtifact:
    feature_store_file_path:str
    train_file_path:str
    test_file_path:str


@dataclass
class DataValidationArtifact:
    report_file_path:str