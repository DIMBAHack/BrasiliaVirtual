from pydantic import BaseModel, EmailStr, Field, BeforeValidator
from typing import Annotated

from typing import Optional
from datetime import datetime
from bson import ObjectId



def _validate_object_id(v):
    if not ObjectId.is_valid(v):
        raise ValueError("Invalid ObjectId")
    return ObjectId(v)

 
PyObjectId = Annotated[ObjectId, BeforeValidator(_validate_object_id)]


class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    full_name: Optional[str] = None
    is_active: bool = True


class UserCreate(UserBase):
    password: str = Field(..., min_length=6)


class UserUpdate(BaseModel):
    username: Optional[str] = Field(None, min_length=3, max_length=50)
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    is_active: Optional[bool] = None


class UserInDB(UserBase):
    id: Optional[PyObjectId] = Field(default=None, alias="_id")
    hashed_password: str
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


class UserResponse(UserBase):
    id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True