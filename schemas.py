from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

# User schemas
class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    username: str
    password: str

# Token schemas
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

# Image schemas
class ImageAttachmentBase(BaseModel):
    description: Optional[str] = None

class ImageAttachmentCreate(ImageAttachmentBase):
    pass

class ImageAttachment(ImageAttachmentBase):
    id: int
    filename: str
    original_filename: str
    file_path: str
    file_size: int
    mime_type: str
    uploaded_at: datetime
    owner_id: int
    
    class Config:
        from_attributes = True

class ImageAttachmentResponse(BaseModel):
    id: int
    filename: str
    original_filename: str
    file_size: int
    mime_type: str
    description: Optional[str] = None
    uploaded_at: datetime
    download_url: str
    
    class Config:
        from_attributes = True
