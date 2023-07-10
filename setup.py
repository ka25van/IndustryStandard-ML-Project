#Why setup.py is used? ->It typically contains information about the package, such as its name, version, and dependencies, as well as instructions for building and installing the package.

#By following the python documentation we can get clear idea.
from setuptools import find_packages, setup
from typing import List

requirement_file_name="requirements.txt"
REMOVE_PACKAGE="-e ."

def get_requirements() -> List[str]:
    with open(requirement_file_name) as requirement_file:#open the file where the packages are mentioned
                requirement_list = requirement_file.readlines()  #reads file of requirement.txt line by line
    requirement_list =[requirement_name.replace("\n","") for requirement_name in requirement_list]#the read moves to next line 

#We don't need -e . file to be read 
    if REMOVE_PACKAGE in requirement_list:
        requirement_list.remove(REMOVE_PACKAGE)
        return requirement_list

    setup(name='Insurance',
      version='1.0',  #if updating and uploading in github the version must be changed
      description='Insurance Industry Standard project',
      author='Kaverappa',
      author_email='kavankaverappa5@gmail.com',
      packages=find_packages(), #reading from init.py inside Insurace(src)
      install_reqires = get_requirements()
     )