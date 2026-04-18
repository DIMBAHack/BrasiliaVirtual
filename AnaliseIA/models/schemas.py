from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from models.db_models import ResultadoChunk


class UploadResponse(BaseModel):
    documento_id: str
    filename: str
    total_chunks: int
    status: str


class DocumentoResponse(BaseModel):
    documento_id: str
    filename: str
    status: str
    total_chunks: int
    criado_em: datetime
    concluido_em: Optional[datetime] = None
    resultado: Optional[list[ResultadoChunk]] = None