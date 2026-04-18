from pymongo import MongoClient
from pymongo.database import Database
from pymongo.collection import Collection
import os


MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")


class MongoDB:
    client: MongoClient = None
    users_db: Database = None
    files_db: Database = None

    @classmethod
    def connect(cls):
        cls.client = MongoClient(MONGO_URI)
        cls.users_db = cls.client["usersDB"]
        cls.files_db = cls.client["filesDB"]
        print("✅ Conectado ao MongoDB")

    @classmethod
    def disconnect(cls):
        if cls.client:
            cls.client.close()
            print("🔌 Desconectado do MongoDB")

    @classmethod
    def get_users_collection(cls) -> Collection:
        return cls.users_db["users"]

    @classmethod
    def get_files_collection(cls) -> Collection:
        return cls.files_db["files"]


def get_users_collection() -> Collection:
    return MongoDB.get_users_collection()


def get_files_collection() -> Collection:
    return MongoDB.get_files_collection()