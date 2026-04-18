from fastapi import APIRouter, File, Form, UploadFile
from services.documento_service import DocumentoService

router = APIRouter(tags=["Análise de Documentos"])
_service = DocumentoService()


@router.post("/upload/")
async def upload_e_analisar(
    file: UploadFile = File(..., description="Arquivo .txt, .pdf ou .docx"),
    tema: str = Form(..., description="Tema do trabalho acadêmico"),
):
    """
    Envia um arquivo e o tema para análise.
    Retorna um `documento_id` para consultar o resultado via GET /documento/{id}.
    A análise ocorre em background — polling até status = 'concluido'.
    """
    return await _service.processar(file, tema)


@router.get("/documento/{documento_id}")
async def buscar_resultado(documento_id: str):
    """
    Retorna o status e o relatório completo da análise.
    - status = 'processando': análise ainda em curso
    - status = 'concluido': resultado disponível
    - status = 'erro': falha durante processamento
    """
    return await _service.buscar(documento_id)
