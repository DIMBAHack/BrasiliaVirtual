from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from typing import List
import shutil, os

from userModel import UserCreate, UserUpdate, UserResponse
from userRepository import UserRepository
from userRouter import get_users_collection, get_files_collection

router = APIRouter(prefix="/users", tags=["Users"])

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


def get_repo() -> UserRepository:
    return UserRepository(
        users_col=get_users_collection(),
        files_col=get_files_collection(),
    )


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register_user(user: UserCreate, repo: UserRepository = Depends(get_repo)):
    try:
        return repo.create_user(user)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/", response_model=List[UserResponse])
def list_users(skip: int = 0, limit: int = 20, repo: UserRepository = Depends(get_repo)):
    return repo.list_users(skip=skip, limit=limit)


@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: str, repo: UserRepository = Depends(get_repo)):
    user = repo.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado.")
    return user


@router.patch("/{user_id}", response_model=UserResponse)
def update_user(user_id: str, data: UserUpdate, repo: UserRepository = Depends(get_repo)):
    user = repo.update_user(user_id, data)
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado.")
    return user


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: str, repo: UserRepository = Depends(get_repo)):
    if not repo.delete_user(user_id):
        raise HTTPException(status_code=404, detail="Usuário não encontrado.")

@router.post("/{user_id}/files", status_code=status.HTTP_201_CREATED)
def upload_file(user_id: str, file: UploadFile = File(...), repo: UserRepository = Depends(get_repo)):
    dest = os.path.join(UPLOAD_DIR, f"{user_id}_{file.filename}")
    with open(dest, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    file_size = os.path.getsize(dest)
    try:
        record = repo.add_file(
            user_id=user_id,
            filename=file.filename,
            content_type=file.content_type,
            size=file_size,
            path=dest,
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

    return {"message": "Arquivo enviado com sucesso.", "file": record}


@router.get("/{user_id}/files")
def list_user_files(user_id: str, repo: UserRepository = Depends(get_repo)):
    if not repo.get_user_by_id(user_id):
        raise HTTPException(status_code=404, detail="Usuário não encontrado.")
    return repo.get_user_files(user_id)


@router.delete("/{user_id}/files/{file_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_file(user_id: str, file_id: str, repo: UserRepository = Depends(get_repo)):
    if not repo.delete_file(user_id, file_id):
        raise HTTPException(status_code=404, detail="Arquivo não encontrado.")