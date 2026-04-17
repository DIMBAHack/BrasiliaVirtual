from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

class ConfigDB:
    def __init__(self):
        self.uri = "mongodb+srv://DIMBAconnection:<db_password>@cluster0.8zcy18j.mongodb.net/?appName=Cluster0"
        self.client = MongoClient(self.uri, server_api=ServerApi('1'))
        
    def get_db():
        config = ConfigDB()
        return config.client

        # Send a ping to confirm a successful connection
        try:
            client.admin.command('ping')
            print("Pinged your deployment. You successfully connected to MongoDB!")
        except Exception as e:
            print(e)