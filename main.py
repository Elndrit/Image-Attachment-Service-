from fastapi import FastAPI, Depends, HTTPException, status, UploadFile, File, Form
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from typing import List, Optional
import os

from database import engine, get_db
from models import Base, User, ImageAttachment
from schemas import UserCreate, User as UserSchema, Token, ImageAttachmentResponse
from auth import authenticate_user, create_access_token, get_current_active_user, get_password_hash
from utils import save_uploaded_file, get_file_url
from config import settings

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Image Attachment Service",
    description="A FastAPI service for uploading and managing images with JWT authentication",
    version="1.0.0"
)

# Mount static files for serving images
os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
app.mount("/images", StaticFiles(directory=settings.UPLOAD_DIR), name="images")

@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "message": "Image Attachment Service API",
        "version": "1.0.0",
        "docs": "/docs",
        "redoc": "/redoc"
    }

@app.post("/register", response_model=UserSchema)
async def register(user: UserCreate, db: Session = Depends(get_db)):
    """Register a new user."""
    # Check if username already exists
    db_user = db.query(User).filter(User.username == user.username).first()
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )
    
    # Check if email already exists
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Create new user
    hashed_password = get_password_hash(user.password)
    db_user = User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """Login and get access token."""
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/users/me", response_model=UserSchema)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    """Get current user information."""
    return current_user

@app.post("/upload", response_model=ImageAttachmentResponse)
async def upload_image(
    file: UploadFile = File(...),
    description: Optional[str] = Form(None),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Upload an image file."""
    # Save the uploaded file
    file_info = await save_uploaded_file(file, description)
    
    # Create database record
    db_image = ImageAttachment(
        filename=file_info["filename"],
        original_filename=file_info["original_filename"],
        file_path=file_info["file_path"],
        file_size=file_info["file_size"],
        mime_type=file_info["mime_type"],
        description=file_info["description"],
        owner_id=current_user.id
    )
    
    db.add(db_image)
    db.commit()
    db.refresh(db_image)
    
    # Return response with download URL
    return ImageAttachmentResponse(
        id=db_image.id,
        filename=db_image.filename,
        original_filename=db_image.original_filename,
        file_size=db_image.file_size,
        mime_type=db_image.mime_type,
        description=db_image.description,
        uploaded_at=db_image.uploaded_at,
        download_url=get_file_url(db_image.filename)
    )

@app.get("/images", response_model=List[ImageAttachmentResponse])
async def list_images(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """List all images for the current user."""
    images = db.query(ImageAttachment).filter(ImageAttachment.owner_id == current_user.id).all()
    
    return [
        ImageAttachmentResponse(
            id=image.id,
            filename=image.filename,
            original_filename=image.original_filename,
            file_size=image.file_size,
            mime_type=image.mime_type,
            description=image.description,
            uploaded_at=image.uploaded_at,
            download_url=get_file_url(image.filename)
        )
        for image in images
    ]

@app.get("/images/{image_id}", response_model=ImageAttachmentResponse)
async def get_image(
    image_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get specific image details."""
    image = db.query(ImageAttachment).filter(
        ImageAttachment.id == image_id,
        ImageAttachment.owner_id == current_user.id
    ).first()
    
    if not image:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Image not found"
        )
    
    return ImageAttachmentResponse(
        id=image.id,
        filename=image.filename,
        original_filename=image.original_filename,
        file_size=image.file_size,
        mime_type=image.mime_type,
        description=image.description,
        uploaded_at=image.uploaded_at,
        download_url=get_file_url(image.filename)
    )

@app.delete("/images/{image_id}")
async def delete_image(
    image_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Delete an image."""
    image = db.query(ImageAttachment).filter(
        ImageAttachment.id == image_id,
        ImageAttachment.owner_id == current_user.id
    ).first()
    
    if not image:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Image not found"
        )
    
    # Delete file from filesystem
    if os.path.exists(image.file_path):
        os.remove(image.file_path)
    
    # Delete from database
    db.delete(image)
    db.commit()
    
    return {"message": "Image deleted successfully"}

@app.get("/download/{filename}")
async def download_image(
    filename: str,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Download an image file."""
    # Verify the image belongs to the current user
    image = db.query(ImageAttachment).filter(
        ImageAttachment.filename == filename,
        ImageAttachment.owner_id == current_user.id
    ).first()
    
    if not image:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Image not found"
        )
    
    if not os.path.exists(image.file_path):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Image file not found on server"
        )
    
    return FileResponse(
        path=image.file_path,
        filename=image.original_filename,
        media_type=image.mime_type
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
