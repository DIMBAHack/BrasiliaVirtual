from fastapi import UploadFile, HTTPException
from services.reader_service import ReaderService
from services.chunk_service import ChunkService
from core.database import criar_documento, buscar_documento


class DocumentoService:
    def __init__(self):
        self.reader = ReaderService()
        self.chunks = ChunkService()

    async def processar(self, file: UploadFile) -> dict:
        text = await self.reader.extract(file)
        chunks = self.chunks.split(text)

        if not chunks:
            raise HTTPException(status_code=422, detail="Nenhum texto encontrado no arquivo")

        documento_id = await criar_documento(file.filename, len(chunks))
        await self.chunks.salvar(documento_id, chunks)

        # await queue.add(documento_id)  # BullMQ — a implementar

        return {
            "documento_id": documento_id,
            "filename": file.filename,
            "total_chunks": len(chunks),
            "status": "processando"
        }

    async def buscar(self, documento_id: str) -> dict:
        doc = await buscar_documento(documento_id)
        if not doc:
            raise HTTPException(status_code=404, detail="Documento não encontrado")
        return doc