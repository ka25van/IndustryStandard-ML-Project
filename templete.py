#We can manually create files like data.py, main.py etc. But instead we can write a templete/script like this so process gets easier and this templete can be used for other projects too.

import os  #provides the facility to establish the interaction between the user and the operating system.
from pathlib import Path
import logging  #it means of tracking events that happen when some software runs.

logging.basicConfig(
    level = logging.INFO,
    format = "[%(asctime)s: %(levelname)s]: %(message)s"
)
#Asking for project/src name
while True:
    project_name = input("Enter your project name: ")
    if project_name !='':
        break

logging.info(f"Creating project by name: {project_name}")


#These files must be present 
list_of_files = [
    ".github/workflows/.gitkeep",
    ".github/workflows/main.yaml",
   # f"src/{project_name}/__init__.py",
    f"{project_name}/__init__.py",
    f"{project_name}/components/__init__.py",
    f"{project_name}/entity/__init__.py",
    f"{project_name}/pipeline/__init__.py",
    f"{project_name}/logger/__init__.py",
    f"{project_name}/config.py",
    f"{project_name}/exception.py",
    f"{project_name}/predictor.py",
    f"{project_name}/utils.py",
    f"configs/config.yaml",
    "requirements.txt",
    "setup.py",
    "main.py"
]


for filepath in list_of_files:
    filepath = Path(filepath)
    filedir, filename = os.path.split(filepath)
    if filedir !="":
        os.makedirs(filedir, exist_ok=True)
        logging.info(f"Creating a new directory at : {filedir} for file: {filename}")
    if (not os.path.exists(filepath)) or (os.path.getsize(filepath) == 0):
        with open(filepath, "w") as f:
            pass
            logging.info(f"Creating a new file: {filename} for path: {filepath}")
    else:
        logging.info(f"file is already present at: {filepath}")