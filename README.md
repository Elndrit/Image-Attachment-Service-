# Image Attachment Service (EAN Processing)

A FastAPI-based service for processing EAN codes and automatically fetching product images from external APIs. The service uses JWT authentication and background processing with Redis and RQ.

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

## 🚀 Features

- 🔐 JWT-based authentication
- 📊 EAN code processing and validation
- 🔄 Background image fetching with Redis + RQ
- 🌐 External API integration for product images
- 📁 Automatic image storage and organization
- 📋 Job status tracking and management
- 🔒 User-specific access control
- 🐳 Docker containerization
- 📱 RESTful API for EAN processing

## 🛠️ Technology Stack

- **Backend**: FastAPI
- **Authentication**: JWT with bcrypt
- **Database**: SQLAlchemy (SQLite/PostgreSQL)
- **Background Processing**: Redis + RQ
- **Image Processing**: Pillow
- **Containerization**: Docker + Docker Compose
- **Frontend**: HTML templates with Jinja2

## 📋 Development Phases

### Phase 1: Backend-Setup (FastAPI + Redis + RQ) ✅
- [x] Basic FastAPI structure
- [x] JWT authentication
- [x] Redis integration
- [x] RQ worker setup
- [x] API basic structure

### Phase 2: EAN Processing ✅
- [x] EAN code validation
- [x] Background EAN processing
- [x] External API integration (placeholder)
- [x] Image storage and organization

### Phase 3: External API Integration
- [ ] Connect to actual external API
- [ ] Implement proper error handling
- [ ] Add retry mechanisms
- [ ] Optimize image processing

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

## 🔌 API Endpoints

### EAN Processing

#### Fetch Image by EAN Code
```http
POST /api/v1/fetch-image
Authorization: Bearer <your-jwt-token>
Content-Type: application/json

{
  "ean_code": "1234567890123",
  "description": "Optional description"
}
```

#### Get Job Status
```http
GET /api/v1/jobs/{job_id}
Authorization: Bearer <your-jwt-token>
```

#### List All Jobs
```http
GET /api/v1/jobs
Authorization: Bearer <your-jwt-token>
```

#### Get Image by EAN Code
```http
GET /api/v1/images/{ean_code}
Authorization: Bearer <your-jwt-token>
```

## 🔧 Configuration

The application uses environment variables for configuration. 

### Environment Setup

1. **Copy the example environment file:**
   ```bash
   cp env.example .env
   ```

2. **Edit the `.env` file** with your specific configuration values:
   ```env
   # JWT Configuration
   SECRET_KEY=your-super-secret-key-change-this-in-production
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=30

   # Database Configuration
   DATABASE_URL=sqlite:///./image_service.db

   # Redis Configuration
   REDIS_URL=redis://localhost:6379
   REDIS_HOST=localhost
   REDIS_PORT=6379
   REDIS_DB=0

   # RQ Configuration
   RQ_QUEUE_NAME=image_processing

   # File Upload Configuration
   UPLOAD_DIR=static
   MAX_FILE_SIZE=10485760  # 10MB in bytes
   ALLOWED_EXTENSIONS=jpg,jpeg,png,gif,webp
   ```

**⚠️ Important:** The `.env` file is automatically ignored by git to keep sensitive information secure. Never commit your actual `.env` file to version control!

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
