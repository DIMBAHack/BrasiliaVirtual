import json
import redis.asyncio as redis
from core.config import settings


class ChunkService:
    def __init__(self, chunk_size: int = 3500, chunk_overlap: int = 600, ttl: int = 86400):
        if chunk_overlap >= chunk_size:
            raise ValueError("chunk_overlap deve ser menor que chunk_size")
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.ttl = ttl
        self.redis = redis.from_url(settings.REDIS_URL)

    def split(self, text: str) -> list[dict]:
        if not text or not text.strip():
            return []

        chunks = []
        start = 0
        index = 0

        while start < len(text):
            end = start + self.chunk_size
            chunk = text[start:end]
            chunks.append({"chunk_number": index, "text": chunk})
            start += self.chunk_size - self.chunk_overlap
            index += 1

        return chunks

    async def salvar(self, documento_id: str, chunks: list[dict]) -> None:
        for chunk in chunks:
            chave = f"chunks:{documento_id}:{chunk['chunk_number']}"
            await self.redis.set(chave, json.dumps(chunk), ex=self.ttl)