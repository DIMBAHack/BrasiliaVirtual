"""
Gerenciamento centralizado de conexões MongoDB.
Unifica usersDB, filesDB e DMBAI em um único cliente.
"""
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import MongoClient
from pymongo.collection import Collection
from dotenv import load_dotenv
import os


# ─────────────────────────────────────────────
# Cliente ASSÍNCRONO (Motor) — usado pelos serviços de análise
# ─────────────────────────────────────────────
_async_client: AsyncIOMotorClient = None
load_dotenv()

async def conectar():
    mongo = os.getenv("MONGODB_URL")
    global _async_client
    _async_client = AsyncIOMotorClient(mongo)
    print(f"✅ Motor conectado → {mongo}")


async def desconectar():
    global _async_client
    if _async_client:
        _async_client.close()
        print("🔌 Motor desconectado.")


def get_async_db(nome: str = os.getenv("MONGODB_DB_NAME", "DMBAI")):
    """Retorna um banco assíncrono pelo nome."""
    if _async_client is None:
        raise RuntimeError("Motor não conectado. Chame `conectar()` no lifespan.")
    return _async_client[nome]


# ─────────────────────────────────────────────
# Cliente SÍNCRONO (PyMongo) — usado pelo UserRepository
# ─────────────────────────────────────────────
class MongoDB:
    _client: MongoClient = None

    @classmethod
    def connect(cls):
        mongo = os.getenv("MONGODB_URL")
        if cls._client is None:
            cls._client = MongoClient(mongo)
            print("✅ PyMongo conectado.")

    @classmethod
    def disconnect(cls):
        if cls._client:
            cls._client.close()
            cls._client = None
            print("🔌 PyMongo desconectado.")

    @classmethod
    def _col(cls, db_name: str, col_name: str) -> Collection:
        if cls._client is None:
            raise RuntimeError("PyMongo não conectado. Chame `MongoDB.connect()`.")
        return cls._client[db_name][col_name]

    @classmethod
    def users_col(cls) -> Collection:
        return cls._col("usersDB", "users")

    @classmethod
    def files_col(cls) -> Collection:
        return cls._col("filesDB", "files")

    @classmethod
    def analises_col(cls) -> Collection:
        return cls._col("DMBAI", "analises")

    @classmethod
    def documentos_col(cls) -> Collection:
        return cls._col("DMBAI", "documentos")
