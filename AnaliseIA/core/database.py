from datetime import datetime
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorClient
from AnaliseIA.core.config import settings
from models.db_models import DocumentoModel, ResultadoChunk


client: AsyncIOMotorClient = None
db = None


async def conectar():
    global client, db
    client = AsyncIOMotorClient(settings.MONGODB_URL)
    db = client[settings.MONGODB_DB_NAME]
    print(f"Conectado ao MongoDB Atlas: {settings.MONGODB_DB_NAME}")


async def desconectar():
    global client
    if client:
        client.close()
        print("Conexão com MongoDB encerrada.")


def get_db():
    return db


async def criar_documento(filename: str, total_chunks: int) -> str:
    documento = DocumentoModel(
        filename=filename,
        total_chunks=total_chunks
    )
    result = await db["documentos"].insert_one(documento.model_dump(exclude={"id"}))
    return str(result.inserted_id)


STATUS_VALIDOS = {"processando", "concluido", "erro"}

async def atualizar_status(documento_id: str, status: str) -> None:
    if status not in STATUS_VALIDOS:
        raise ValueError(f"Status inválido: '{status}'")
    ...


async def salvar_resultado(documento_id: str, resultado: list[ResultadoChunk]) -> None:
    await db["documentos"].update_one(
        {"_id": ObjectId(documento_id)},
        {"$set": {
            "status": "concluido",
            "resultado": [r.model_dump() for r in resultado],
            "concluido_em": datetime.utcnow()
        }}
    )


async def buscar_documento(documento_id: str) -> dict | None:
    doc = await db["documentos"].find_one({"_id": ObjectId(documento_id)})
    if doc:
        doc["_id"] = str(doc["_id"])
    return doc