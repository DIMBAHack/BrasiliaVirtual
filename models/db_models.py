from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict


class ResultadoChunk(BaseModel):
    chunk_number: int
    text: str
    probabilidade_ia: float
    confiabilidade_fonte: Optional[float] = None
    plagio_detectado: Optional[bool] = None
    url_origem: Optional[str] = None


class DocumentoModel(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
    )
    id: Optional[str] = Field(None, alias="_id")
    filename: str
    status: str = "processando"       # processando | concluido | erro
    total_chunks: int
    criado_em: datetime = Field(default_factory=datetime.utcnow)
    atualizado_em: Optional[datetime] = None
    concluido_em: Optional[datetime] = None
    resultado: Optional[list[ResultadoChunk]] = None