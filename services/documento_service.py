from fastapi import UploadFile, HTTPException
from services.reader_service import ReaderService
from services.chunk_service import ChunkService
from services.files.fileManagement import FileManagement
from AnaliseIA.core.database import criar_documento, buscar_documento
from langchain_huggingface import HuggingFaceEmbeddings


class DocumentoService:
    def __init__(self, file_management: FileManagement):
        self.reader = ReaderService()
        self.chunk_service = ChunkService()
        self.file_management = file_management

    async def processar(self, file: UploadFile) -> dict:

        file_id = await self.file_management.upload_file(file)

        text = await self.reader.extract(file)

        chunks = self.chunk_service.split(text)
        if not chunks:
            raise HTTPException(status_code=422, detail="Nenhum texto encontrado no arquivo")

        documento_id = await criar_documento(file.filename, len(chunks))
        await self.chunk_service.salvar(documento_id, chunks)

        return {
            "documento_id": documento_id,
            "file_id": file_id,
            "filename": file.filename,
            "total_chunks": len(chunks),
            "status": "processando"
        }

    async def buscar(self, documento_id: str) -> dict:
        doc = await buscar_documento(documento_id)
        if not doc:
            raise HTTPException(status_code=404, detail="Documento não encontrado")
        return doc


    def embeddings(self, chunks: list[dict]) -> list:
        hf = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-mpnet-base-v2",
            model_kwargs={"device": "cpu"},
            encode_kwargs={"normalize_embeddings": False}
        )
        texts = [chunk["text"] for chunk in chunks]
        return hf.embed_documents(texts)