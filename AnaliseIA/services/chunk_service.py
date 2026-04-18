import json
import redis.asyncio as redis
from core.config import settings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from reader_service import ReaderService


class ChunkService:
    def __init__(self, file_management: ReaderService):
        self.file_management = file_management

    def process_file(self, file_id: str):
        text = self.file_management.get_file(file_id)
        if text is None:
            return {"error": "File not found"}
        else:
            return text["data"]
        
    def split(self):
        text = self.process_file()
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=3500, chunk_overlap=600, separators=["\n\n", "\n", " ", ""])
        chunks = text_splitter.split_text(self.process_file(text))
        return chunks
    
    def enumerate_chunks(self):
        self.chunks = self.chuncking()
        enumerated_chunks = list(enumerate(self.chunks))
        return enumerated_chunks
    
    def format_chunks(self):
        self.chunks = self.chuncking()
        
        formatted_chunks = [
            {
                "chunk_number": index,
                "text": chunk
            }
            for index, chunk in enumerate(self.chunks)
        ]
        
        return formatted_chunks
    
    def buscar_chunks(self, documento_id: str) -> list[dict]:
        pattern = f"chunks:{documento_id}:*"
        keys = self.redis.keys(pattern)
        chunks = []
        for key in keys:
            chunk_data = self.redis.get(key)
            if chunk_data:
                chunks.append(json.loads(chunk_data))
        return chunks
    

    async def salvar(self, documento_id: str, chunks: list[dict]) -> None:
        for chunk in chunks:
            chave = f"chunks:{documento_id}:{chunk['chunk_number']}"
            await self.redis.set(chave, json.dumps(chunk), ex=self.ttl)