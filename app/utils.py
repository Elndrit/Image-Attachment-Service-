import os
import uuid
import aiofiles
from typing import Optional
from fastapi import UploadFile, HTTPException, status
from PIL import Image
import io
from config import ALLOWED_EXTENSIONS, MAX_FILE_SIZE, UPLOAD_DIR

def get_file_extension(filename: str) -> str:
    """Extract file extension from filename."""
    return filename.split('.')[-1].lower()

def is_allowed_file(filename: str) -> bool:
    """Check if file extension is allowed."""
    return get_file_extension(filename) in ALLOWED_EXTENSIONS

def validate_image_file(file: UploadFile) -> None:
    """Validate uploaded image file."""
    if not file.filename:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No filename provided"
        )
    
    if not is_allowed_file(file.filename):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File type not allowed. Allowed types: {', '.join(ALLOWED_EXTENSIONS)}"
        )
    
    if file.size and file.size > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File too large. Maximum size: {MAX_FILE_SIZE // 1024 // 1024}MB"
        )

async def save_uploaded_file(file: UploadFile, description: Optional[str] = None) -> dict:
    """Save uploaded file and return file info."""
    validate_image_file(file)
    
    # Create upload directory if it doesn't exist
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    
    # Generate unique filename
    file_extension = get_file_extension(file.filename)
    unique_filename = f"{uuid.uuid4()}.{file_extension}"
    file_path = os.path.join(UPLOAD_DIR, unique_filename)
    
    # Read and validate image
    try:
        content = await file.read()
        
        # Validate image with PIL
        image = Image.open(io.BytesIO(content))
        image.verify()  # Verify it's a valid image
        
        # Reset file pointer
        await file.seek(0)
        
        # Save file
        async with aiofiles.open(file_path, 'wb') as f:
            await f.write(content)
        
        return {
            "filename": unique_filename,
            "original_filename": file.filename,
            "file_path": file_path,
            "file_size": len(content),
            "mime_type": file.content_type or f"image/{file_extension}",
            "description": description
        }
        
    except Exception as e:
        # Clean up if file was created
        if os.path.exists(file_path):
            os.remove(file_path)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid image file: {str(e)}"
        )

def get_file_url(filename: str) -> str:
    """Generate download URL for a file."""
    return f"/images/{filename}"
