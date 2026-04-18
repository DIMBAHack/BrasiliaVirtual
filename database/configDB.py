from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

class ConfigDB:
    def __init__(self):
        self.uri = "mongodb+srv://DIMBAconnection:<db_password>@cluster0.8zcy18j.mongodb.net/?appName=Cluster0"
        self.client = MongoClient(self.uri, server_api=ServerApi('1'))

    def fileDB(self):
        try:
            self.client.admin.command('ping')
            print("Conectado ao MongoDB com sucesso!")
        except Exception as e:
            print(f"Erro de conexão: {e}")
        return self.client["FilesDB"]

    def fontesDB(self):
        try:
            self.client.admin.command('ping')  
            print("Conectado ao MongoDB com sucesso!")
        except Exception as e:
            print(f"Erro de conexão: {e}")
        return self.client["fontesDB"]

    def userDB(self):
        try:
            self.client.admin.command('ping')  
            print("Conectado ao MongoDB com sucesso!")
        except Exception as e:
            print(f"Erro de conexão: {e}")
        return self.client["userDB"]