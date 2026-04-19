"""
core/database.py — fonte única de verdade para todas as conexões MongoDB.
"""
import os
from dotenv import load_dotenv

from pymongo import MongoClient
from pymongo.collection import Collection
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from pydantic_settings import BaseSettings

load_dotenv()


# ── Settings ────────────────────────────────────────────────────────────────

class Settings(BaseSettings):
    MONGODB_URL: str
    MONGODB_DB_NAME: str = "DMBAI"
    OPENAI_API_KEY: str = ""
    ANTHROPIC_API_KEY: str = ""
    GOOGLE_API_KEY: str = ""
    REDIS_URL: str = "redis://localhost:6379"
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_PASSWORD: str = ""

    class Config:
        env_file = ".env"
        extra = "ignore"   # ← ignora qualquer chave extra no .env

settings = Settings()


# ── Motor (async) — usado pelo DocumentoService ─────────────────────────────

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
# from sua_config import settings

class AsyncMongoManager:
    # Atributos de classe (compartilhados globalmente)
    _client: AsyncIOMotorClient | None = None
    _db: AsyncIOMotorDatabase | None = None

    @classmethod
    def conectar(cls):
        """Inicializa a conexão estaticamente."""
        if cls._client is None:
            cls._client = AsyncIOMotorClient(settings.MONGODB_URL)
            cls._db = cls._client[settings.MONGODB_DB_NAME]
            print("✅ Motor (async) conectado ao MongoDB (Estático)")

    @classmethod
    async def desconectar(cls):
        """Encerra a conexão estaticamente."""
        if cls._client is not None:
            cls._client.close()
            cls._client = None
            cls._db = None
            print("🔌 Motor desconectado")

    @classmethod
    def get_db(cls) -> AsyncIOMotorDatabase:
        """Retorna a instância do banco de dados estaticamente."""
        if cls._db is None:
            raise RuntimeError("Motor não conectado. Verifique o lifespan do FastAPI.")
        return cls._db


# ── PyMongo (sync) — usado pelo UserRepository ──────────────────────────────

class MongoDB:
    _client: MongoClient = None

    @classmethod
    def connect(cls):
        cls._client = MongoClient(
            settings.MONGODB_URL,

            tls=True,

            tlsAllowInvalidCertificates=True,

        )

        cls._client.admin.command("ping")

        print("✅ PyMongo (sync) conectado ao MongoDB")
    @classmethod
    def disconnect(cls):
        if cls._client:
            cls._client.close()
            print("🔌 PyMongo desconectado")

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
    
    # Motor (async)
