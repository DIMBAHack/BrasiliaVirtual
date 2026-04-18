from pymongo.collection import Collection
from pymongo import ASCENDING
from bson import ObjectId
from datetime import datetime
from typing import Optional, List
import hashlib
import secrets

from models.user_model import UserCreate, UserUpdate, UserResponse


def _hash_password(password: str) -> str:
    salt = secrets.token_hex(16)
    hashed = hashlib.sha256(f"{salt}{password}".encode()).hexdigest()
    return f"{salt}:{hashed}"


def _verify_password(password: str, hashed_password: str) -> bool:
    salt, hashed = hashed_password.split(":", 1)
    return hashlib.sha256(f"{salt}{password}".encode()).hexdigest() == hashed


class UserRepository:
    def __init__(self, users_col: Collection, files_col: Collection):
        self.users_col = users_col
        self.files_col = files_col
        self._ensure_indexes()

    def _ensure_indexes(self):
        self.users_col.create_index([("email", ASCENDING)], unique=True)
        self.users_col.create_index([("username", ASCENDING)], unique=True)
        self.files_col.create_index([("user_id", ASCENDING)])

    # ── CRUD ────────────────────────────────────

    def create_user(self, data: UserCreate) -> UserResponse:
        if self.users_col.find_one({"email": data.email}):
            raise ValueError(f"Email '{data.email}' já cadastrado.")
        if self.users_col.find_one({"username": data.username}):
            raise ValueError(f"Username '{data.username}' já em uso.")

        now = datetime.utcnow()
        doc = {
            "username": data.username,
            "email": data.email,
            "full_name": data.full_name,
            "is_active": data.is_active,
            "hashed_password": _hash_password(data.password),
            "created_at": now,
            "updated_at": now,
        }
        result = self.users_col.insert_one(doc)
        doc["_id"] = result.inserted_id
        return self._to_response(doc)

    def get_by_id(self, user_id: str) -> Optional[UserResponse]:
        try:
            doc = self.users_col.find_one({"_id": ObjectId(user_id)})
        except Exception:
            return None
        return self._to_response(doc) if doc else None

    def get_by_email(self, email: str) -> Optional[UserResponse]:
        doc = self.users_col.find_one({"email": email})
        return self._to_response(doc) if doc else None

    def get_by_username(self, username: str) -> Optional[UserResponse]:
        doc = self.users_col.find_one({"username": username})
        return self._to_response(doc) if doc else None

    def list_users(self, skip: int = 0, limit: int = 20) -> List[UserResponse]:
        return [self._to_response(d) for d in self.users_col.find().skip(skip).limit(limit)]

    def update_user(self, user_id: str, data: UserUpdate) -> Optional[UserResponse]:
        changes = {k: v for k, v in data.model_dump().items() if v is not None}
        if not changes:
            return self.get_by_id(user_id)
        changes["updated_at"] = datetime.utcnow()
        result = self.users_col.find_one_and_update(
            {"_id": ObjectId(user_id)},
            {"$set": changes},
            return_document=True,
        )
        return self._to_response(result) if result else None

    def delete_user(self, user_id: str) -> bool:
        result = self.users_col.delete_one({"_id": ObjectId(user_id)})
        if result.deleted_count:
            self.files_col.delete_many({"user_id": user_id})
            return True
        return False

    def authenticate(self, email: str, password: str) -> Optional[UserResponse]:
        doc = self.users_col.find_one({"email": email})
        if doc and _verify_password(password, doc["hashed_password"]):
            return self._to_response(doc)
        return None

    # ── Arquivos (filesDB) ───────────────────────

    def add_file(self, user_id: str, filename: str, content_type: str,
                 size: int, path: str, documento_id: Optional[str] = None) -> dict:
        if not self.get_by_id(user_id):
            raise ValueError(f"Usuário '{user_id}' não encontrado.")
        doc = {
            "user_id": user_id,
            "filename": filename,
            "content_type": content_type,
            "size": size,
            "path": path,
            "documento_id": documento_id,     # ID da análise no DMBAI
            "uploaded_at": datetime.utcnow(),
        }
        result = self.files_col.insert_one(doc)
        return {**doc, "_id": str(result.inserted_id)}

    def get_user_files(self, user_id: str) -> List[dict]:
        return [{**d, "_id": str(d["_id"])} for d in self.files_col.find({"user_id": user_id})]

    def delete_file(self, user_id: str, file_id: str) -> bool:
        result = self.files_col.delete_one({"_id": ObjectId(file_id), "user_id": user_id})
        return result.deleted_count > 0

    @staticmethod
    def _to_response(doc: dict) -> UserResponse:
        return UserResponse(
            id=str(doc["_id"]),
            username=doc["username"],
            email=doc["email"],
            full_name=doc.get("full_name"),
            is_active=doc.get("is_active", True),
            created_at=doc["created_at"],
            updated_at=doc["updated_at"],
        )
