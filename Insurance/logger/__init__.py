#Log is imp as it records every error in the program
import os
from datetime import datetime
import logging

#Creating a directory for the log data 
LOG_DIR="Insurance_log"

#Noting the time of log recorded
LOG_TIME=f"{datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}"

#creating a file name for the log time
LOG_FILE_NAME=f"log_{LOG_TIME}.log"

#Creating a directory for log if it doesn't exists
os.makedirs(LOG_DIR, exist_ok=True)

#Also to make a path for the file
LOG_FILE_PATH= os.path.join(LOG_DIR,LOG_FILE_NAME)

#If you want to read log select baseconfig and press f12 from your system.
#by going through logging in python in google
logging.basicConfig(filename='LOG_FILE_PATH',  #Here the filename means the path
filemode="w", #write mode
format='[%(asctime)s] %(name)s - %(levelname)s - %(message)s',
level=logging.DEBUG
)