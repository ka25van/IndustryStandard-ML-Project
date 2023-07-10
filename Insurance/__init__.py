#This here collects the data from the mongodb databse, but we can't show the data base access directly. So we creatte a .env file and call it here
from dotenv import load_dotenv
print("Data callfrom .env")
load_dotenv()