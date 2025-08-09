from dotenv import load_dotenv
import os

# Einmalig .env laden
load_dotenv()

# JWT
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

# Datenbank
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./image_service.db")

# Redis & RQ
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
RQ_QUEUE_NAME = os.getenv("RQ_QUEUE_NAME", "image_processing")

# File Upload
UPLOAD_DIR = os.getenv("UPLOAD_DIR", "static")
MAX_FILE_SIZE = int(os.getenv("MAX_FILE_SIZE", "10485760"))
ALLOWED_EXTENSIONS = os.getenv("ALLOWED_EXTENSIONS", "jpg,jpeg,png,gif,webp").split(",")

# Mock-Modus für externe API
USE_MOCK_API = os.getenv("USE_MOCK_API", "true").lower() == "true"

# Externe Bild-API (Barcode Lookup)
BARCODE_LOOKUP_API_KEY = os.getenv("BARCODE_LOOKUP_API_KEY", "")
BASE_BARCODE_LOOKUP_URL = os.getenv(
    "BASE_BARCODE_LOOKUP_URL",
    "https://api.barcodelookup.com/v3/products"
)
