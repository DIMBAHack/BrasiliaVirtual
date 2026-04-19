from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import os
from dotenv import load_dotenv
load_dotenv()

class ConfigDB:
    def __init__(self):
        self.uri = os.getenv('MONGODB_URL')
        self.client = MongoClient(self.uri, server_api=ServerApi('1'))
        
    def fileDB(self):
        files = self.client["FilesDB"]
        try:
            self.client.admin.command('ping')
            print("Pinged your deployment. You successfully connected to MongoDB!")
        except Exception as e:
            print(e)
        return files
    
    def fontesDB(self):
        fontes = self.client["fontesDB"]
        try:
            self.client.admin.comman('ping')
            print("Pinged your deployment. You successfully connected to MongoDB!")
        except Exception as e:
            print(e)
        return fontes
    

    def userDB(self):
        user = self.client.admin.comman('ping')
        try:
            self.client.admin.comman('ping')
            print("Pinged your deployment. You successfully connected to MongoDB!")
        except Exception as e:
            print(e)
        return user