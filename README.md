# Image Attachment Service

A FastAPI-based service for uploading and managing images with JWT authentication.

## Features

- 🔐 JWT-based authentication
- 📤 Image upload with validation
- 📋 Image listing and management
- 🗑️ Image deletion
- 📥 Secure image download
- 🖼️ Support for multiple image formats (JPG, PNG, GIF, WebP)
- 📊 Automatic image metadata storage
- 🔒 User-specific image access control

## Quick Start

### Prerequisites

- Python 3.8+
- pip

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd Image-Attachment-Service
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the server:
```bash
python main.py
```

The server will start at `http://localhost:8000`

## API Documentation

Once the server is running, you can access:
- **Interactive API docs**: http://localhost:8000/docs
- **ReDoc documentation**: http://localhost:8000/redoc

## API Endpoints

### Authentication

#### Register User
```http
POST /register
Content-Type: application/json

{
  "username": "john_doe",
  "email": "john@example.com",
  "password": "securepassword123"
}
```

#### Login
```http
POST /token
Content-Type: application/x-www-form-urlencoded

username=john_doe&password=securepassword123
```

### Image Management

#### Upload Image
```http
POST /upload
Authorization: Bearer <your-jwt-token>
Content-Type: multipart/form-data

file: <image-file>
description: "Optional image description"
```

#### List Images
```http
GET /images
Authorization: Bearer <your-jwt-token>
```

#### Get Image Details
```http
GET /images/{image_id}
Authorization: Bearer <your-jwt-token>
```

#### Download Image
```http
GET /download/{filename}
Authorization: Bearer <your-jwt-token>
```

#### Delete Image
```http
DELETE /images/{image_id}
Authorization: Bearer <your-jwt-token>
```

## Configuration

The application uses environment variables for configuration. Create a `.env` file in the root directory:

```env
# JWT Configuration
SECRET_KEY=your-super-secret-key-change-this-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Database Configuration
DATABASE_URL=sqlite:///./image_service.db

# File Upload Configuration
UPLOAD_DIR=uploads
MAX_FILE_SIZE=10485760  # 10MB in bytes
ALLOWED_EXTENSIONS=jpg,jpeg,png,gif,webp
```

## Usage Examples

### Using curl

1. **Register a new user:**
```bash
curl -X POST "http://localhost:8000/register" \
  -H "Content-Type: application/json" \
  -d '{"username": "testuser", "email": "test@example.com", "password": "password123"}'
```

2. **Login and get token:**
```bash
curl -X POST "http://localhost:8000/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=testuser&password=password123"
```

3. **Upload an image:**
```bash
curl -X POST "http://localhost:8000/upload" \
  -H "Authorization: Bearer <your-jwt-token>" \
  -F "file=@/path/to/your/image.jpg" \
  -F "description=My uploaded image"
```

4. **List images:**
```bash
curl -X GET "http://localhost:8000/images" \
  -H "Authorization: Bearer <your-jwt-token>"
```

### Using Python requests

```python
import requests

# Base URL
base_url = "http://localhost:8000"

# Register
response = requests.post(f"{base_url}/register", json={
    "username": "testuser",
    "email": "test@example.com",
    "password": "password123"
})

# Login
response = requests.post(f"{base_url}/token", data={
    "username": "testuser",
    "password": "password123"
})
token = response.json()["access_token"]

# Upload image
headers = {"Authorization": f"Bearer {token}"}
with open("image.jpg", "rb") as f:
    response = requests.post(
        f"{base_url}/upload",
        headers=headers,
        files={"file": f},
        data={"description": "My image"}
    )

# List images
response = requests.get(f"{base_url}/images", headers=headers)
images = response.json()
```

## Security Features

- **JWT Authentication**: Secure token-based authentication
- **Password Hashing**: Passwords are hashed using bcrypt
- **File Validation**: Images are validated for format and size
- **Access Control**: Users can only access their own images
- **SQL Injection Protection**: Uses SQLAlchemy ORM
- **File Type Validation**: Only allowed image formats are accepted

## Database Schema

### Users Table
- `id`: Primary key
- `username`: Unique username
- `email`: Unique email address
- `hashed_password`: Bcrypt hashed password
- `created_at`: Account creation timestamp
- `updated_at`: Last update timestamp

### Image Attachments Table
- `id`: Primary key
- `filename`: Unique filename on server
- `original_filename`: Original uploaded filename
- `file_path`: Path to file on filesystem
- `file_size`: File size in bytes
- `mime_type`: MIME type of the file
- `description`: Optional description
- `uploaded_at`: Upload timestamp
- `owner_id`: Foreign key to users table

## Development

### Project Structure
```
Image-Attachment-Service/
├── main.py              # FastAPI application
├── config.py            # Configuration settings
├── database.py          # Database connection
├── models.py            # SQLAlchemy models
├── schemas.py           # Pydantic schemas
├── auth.py              # Authentication utilities
├── utils.py             # File handling utilities
├── requirements.txt     # Python dependencies
└── README.md           # This file
```

### Adding New Features

1. **New Endpoints**: Add routes in `main.py`
2. **Database Changes**: Update models in `models.py`
3. **Validation**: Update schemas in `schemas.py`
4. **Configuration**: Add settings in `config.py`

## License

This project is licensed under the MIT License.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request
