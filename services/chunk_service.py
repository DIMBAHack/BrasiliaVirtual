import json
import redis.asyncio as redis
from AnaliseIA.core.config import settings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from fastapi import HTTPException


class ChunkService:
    def __init__(self, chunk_size: int = 3500, chunk_overlap: int = 600, ttl: int = 86400):
        if chunk_overlap >= chunk_size:
            raise ValueError("chunk_overlap deve ser menor que chunk_size")
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.ttl = ttl
        self.redis = redis.from_url(settings.REDIS_URL)
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            separators=["\n\n", "\n", " ", ""]
        )

    def split(self, text: str) -> list[dict]:
        if not text or not text.strip():
            return []

        raw_chunks = self.splitter.split_text(text)

        return [
            {"chunk_number": index, "text": chunk}
            for index, chunk in enumerate(raw_chunks)
        ]

    async def salvar(self, documento_id: str, chunks: list[dict]) -> None:
        for chunk in chunks:
            chave = f"chunks:{documento_id}:{chunk['chunk_number']}"
            await self.redis.set(chave, json.dumps(chunk), ex=self.ttl)

    async def buscar_chunks(self, documento_id: str) -> list[dict]:
        pattern = f"chunks:{documento_id}:*"
        keys = await self.redis.keys(pattern)

        if not keys:
            raise HTTPException(status_code=404, detail="Chunks não encontrados")

        chunks = []
        for key in sorted(keys):
            data = await self.redis.get(key)
            if data:
                chunks.append(json.loads(data))

        return sorted(chunks, key=lambda c: c["chunk_number"])