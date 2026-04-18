from fastapi import APIRouter, File, UploadFile
from services.documento_service import DocumentoService
from models.schemas import UploadResponse, DocumentoResponse

router = APIRouter()
documento_service = DocumentoService()

@router.post("/upload/", response_model=UploadResponse)
async def upload_file(file: UploadFile = File(...)):
    return await documento_service.processar(file)

@router.get("/documento/{documento_id}", response_model=DocumentoResponse)
async def get_documento(documento_id: str):
    return await documento_service.buscar(documento_id)