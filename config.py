import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    # JWT Configuration
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-super-secret-key-change-this-in-production")
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
    
    # Database Configuration
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./image_service.db")
    
    # Redis Configuration
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379")
    REDIS_HOST: str = os.getenv("REDIS_HOST", "localhost")
    REDIS_PORT: int = int(os.getenv("REDIS_PORT", "6379"))
    REDIS_DB: int = int(os.getenv("REDIS_DB", "0"))
    
    # RQ Configuration
    RQ_QUEUE_NAME: str = os.getenv("RQ_QUEUE_NAME", "image_processing")
    
    # File Upload Configuration
    UPLOAD_DIR: str = os.getenv("UPLOAD_DIR", "static")
    MAX_FILE_SIZE: int = int(os.getenv("MAX_FILE_SIZE", "10485760"))  # 10MB
    ALLOWED_EXTENSIONS: list = os.getenv("ALLOWED_EXTENSIONS", "jpg,jpeg,png,gif,webp").split(",")

settings = Settings()
