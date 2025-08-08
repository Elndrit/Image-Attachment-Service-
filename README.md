# Image Attachment Service

A FastAPI-based service for uploading and managing images with JWT authentication and background image processing using Redis and RQ.

## 🏗️ Project Architecture

```
image_service/
├── app/
│   ├── main.py             # FastAPI app
│   ├── auth.py             # JWT Auth-Logik
│   ├── api.py              # Upload + Image-Serve Endpunkte
│   ├── worker.py           # Redis Consumer für Bildverarbeitung
│   ├── utils.py            # Hilfsfunktionen (z. B. save_image)
│   └── templates/
│       └── upload.html     # Simple Upload-UI
├── static/                 # Gespeicherte Bilder
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

## 🚀 Features (Planned)

- 🔐 JWT-based authentication
- 📤 Image upload with validation
- 🔄 Background image processing with Redis + RQ
- 📋 Image listing and management
- 🗑️ Image deletion
- 📥 Secure image download
- 🖼️ Support for multiple image formats (JPG, PNG, GIF, WebP)
- 📊 Automatic image metadata storage
- 🔒 User-specific image access control
- 🐳 Docker containerization
- 📱 Simple web UI for uploads

## 🛠️ Technology Stack

- **Backend**: FastAPI
- **Authentication**: JWT with bcrypt
- **Database**: SQLAlchemy (SQLite/PostgreSQL)
- **Background Processing**: Redis + RQ
- **Image Processing**: Pillow
- **Containerization**: Docker + Docker Compose
- **Frontend**: HTML templates with Jinja2

## 📋 Development Phases

### Phase 1: Backend-Setup (FastAPI + Redis + RQ)
- [x] Basic FastAPI structure
- [x] JWT authentication
- [ ] Redis integration
- [ ] RQ worker setup
- [ ] API basic structure

### Phase 2: Image Processing
- [ ] Background image processing
- [ ] Image resizing and compression
- [ ] Multiple format support
- [ ] Processing queue management

### Phase 3: Frontend & UI
- [ ] Upload interface
- [ ] Image gallery
- [ ] User management UI

### Phase 4: Production & Deployment
- [ ] Docker containerization
- [ ] Docker Compose orchestration
- [ ] Production configuration
- [ ] Monitoring and logging

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Redis server
- Docker (optional)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/Elndrit/Image-Attachment-Service-.git
cd Image-Attachment-Service-
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Start Redis server:
```bash
# On Windows (if using WSL or Docker)
redis-server

# Or using Docker
docker run -d -p 6379:6379 redis:alpine
```

4. Run the application:
```bash
# Start the FastAPI server
python -m uvicorn app.main:app --reload

# Start the RQ worker (in another terminal)
python -m rq worker
```

The server will start at `http://localhost:8000`

## 📚 API Documentation

Once the server is running, you can access:
- **Interactive API docs**: http://localhost:8000/docs
- **ReDoc documentation**: http://localhost:8000/redoc

## 🔧 Configuration

The application uses environment variables for configuration. Create a `.env` file in the root directory:

```env
# JWT Configuration
SECRET_KEY=your-super-secret-key-change-this-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Database Configuration
DATABASE_URL=sqlite:///./image_service.db

# Redis Configuration
REDIS_URL=redis://localhost:6379

# File Upload Configuration
UPLOAD_DIR=static
MAX_FILE_SIZE=10485760  # 10MB in bytes
ALLOWED_EXTENSIONS=jpg,jpeg,png,gif,webp
```

## 🐳 Docker Deployment

### Using Docker Compose

```bash
# Build and start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### Manual Docker Build

```bash
# Build the image
docker build -t image-attachment-service .

# Run the container
docker run -p 8000:8000 image-attachment-service
```

## 🧪 Testing

Run the test suite:

```bash
python test_api.py
```

## 📁 Project Structure

### Core Application (`app/`)
- `main.py` - FastAPI application entry point
- `auth.py` - JWT authentication logic
- `api.py` - API endpoints for upload and image serving
- `worker.py` - Redis consumer for background image processing
- `utils.py` - Utility functions for file handling
- `templates/` - HTML templates for web interface

### Static Files (`static/`)
- Stored images and processed files

### Configuration
- `Dockerfile` - Container configuration
- `docker-compose.yml` - Multi-service orchestration
- `requirements.txt` - Python dependencies

## 🔄 Background Processing

The service uses Redis and RQ for background image processing:

1. **Upload**: Images are uploaded and queued for processing
2. **Processing**: RQ workers process images in the background
3. **Storage**: Processed images are stored in the static directory
4. **Serving**: Images are served through the API

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 🔗 Links

- **Repository**: https://github.com/Elndrit/Image-Attachment-Service-
- **API Documentation**: http://localhost:8000/docs (when running)
