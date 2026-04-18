from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from models.db_models import ResultadoChunk


class UploadResponse(BaseModel):
    documento_id: str
    filename: str
    tema: str
    total_chunks: int
    status: str


class ResumoAnalise(BaseModel):
    total_trechos: int
    trechos_ia: int
    trechos_plagio: int
    trechos_fake_news: int
    trechos_autorais: int
    pct_ia: float
    pct_plagio: float
    pct_fake_news: float
    pct_autoral: float
    perplexidade_media: float
    veredicto: str   # "limpo" | "suspeito_ia" | "plagio" | "fake_news" | "multiplos_problemas"


class DocumentoResponse(BaseModel):
    documento_id: str
    filename: str
    tema: str
    status: str
    total_chunks: int
    criado_em: datetime
    concluido_em: Optional[datetime] = None
    resumo: Optional[ResumoAnalise] = None
    resultado: Optional[list[ResultadoChunk]] = None
    dicas_ia: Optional[list[str]] = None


class ErroResponse(BaseModel):
    detalhe: str
    documento_id: Optional[str] = None
