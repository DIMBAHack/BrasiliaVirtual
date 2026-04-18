from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from typing import List, Optional
import shutil
import os

from models.user_model import UserCreate, UserUpdate, UserResponse
from models.user_repository import UserRepository
from core.database import MongoDB

router = APIRouter(prefix="/users", tags=["Usuários"])

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


def get_repo() -> UserRepository:
    return UserRepository(
        users_col=MongoDB.users_col(),
        files_col=MongoDB.files_col(),
    )


# ── Usuários ────────────────────────────────────────────────

@router.post("/", response_model=UserResponse, status_code=201)
def criar_usuario(user: UserCreate, repo: UserRepository = Depends(get_repo)):
    try:
        return repo.create_user(user)
    except ValueError as e:
        raise HTTPException(400, detail=str(e))


@router.get("/", response_model=List[UserResponse])
def listar_usuarios(skip: int = 0, limit: int = 20, repo: UserRepository = Depends(get_repo)):
    return repo.list_users(skip=skip, limit=limit)


@router.get("/{user_id}", response_model=UserResponse)
def buscar_usuario(user_id: str, repo: UserRepository = Depends(get_repo)):
    u = repo.get_by_id(user_id)
    if not u:
        raise HTTPException(404, detail="Usuário não encontrado.")
    return u


@router.patch("/{user_id}", response_model=UserResponse)
def atualizar_usuario(user_id: str, data: UserUpdate, repo: UserRepository = Depends(get_repo)):
    u = repo.update_user(user_id, data)
    if not u:
        raise HTTPException(404, detail="Usuário não encontrado.")
    return u


@router.delete("/{user_id}", status_code=204)
def deletar_usuario(user_id: str, repo: UserRepository = Depends(get_repo)):
    if not repo.delete_user(user_id):
        raise HTTPException(404, detail="Usuário não encontrado.")


# ── Arquivos do usuário (filesDB) ────────────────────────────

@router.post("/{user_id}/files", status_code=201)
def upload_arquivo(
    user_id: str,
    file: UploadFile = File(...),
    documento_id: Optional[str] = None,
    repo: UserRepository = Depends(get_repo),
):
    dest = os.path.join(UPLOAD_DIR, f"{user_id}_{file.filename}")
    with open(dest, "wb") as buf:
        shutil.copyfileobj(file.file, buf)

    try:
        record = repo.add_file(
            user_id=user_id,
            filename=file.filename,
            content_type=file.content_type or "application/octet-stream",
            size=os.path.getsize(dest),
            path=dest,
            documento_id=documento_id,
        )
    except ValueError as e:
        raise HTTPException(404, detail=str(e))

    return {"mensagem": "Arquivo salvo com sucesso.", "arquivo": record}


@router.get("/{user_id}/files")
def listar_arquivos(user_id: str, repo: UserRepository = Depends(get_repo)):
    if not repo.get_by_id(user_id):
        raise HTTPException(404, detail="Usuário não encontrado.")
    return repo.get_user_files(user_id)


@router.delete("/{user_id}/files/{file_id}", status_code=204)
def deletar_arquivo(user_id: str, file_id: str, repo: UserRepository = Depends(get_repo)):
    if not repo.delete_file(user_id, file_id):
        raise HTTPException(404, detail="Arquivo não encontrado.")
