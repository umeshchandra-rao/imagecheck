# ImageFind - Quantum-Inspired Image Retrieval System

A sophisticated image search and retrieval platform leveraging quantum computing algorithms, deep learning, and cloud infrastructure to deliver lightning-fast, AI-powered image discovery.

## 🎯 Project Overview

ImageFind is a **full-stack web application** that combines:
- **Quantum-Inspired Algorithms** for advanced image processing
- **Deep Learning Models** (ResNet-50, ViT) for feature extraction
- **Vector Database** (Pinecone) for similarity search
- **Cloud CDN** (Cloudinary) for image storage and optimization
- **Modern Frontend** (React + TypeScript) for intuitive UI

### Core Features
✅ Multi-category image upload (Healthcare, Satellite, Surveillance)
✅ Real-time similarity search across image database
✅ Quantum-inspired feature encoding for enhanced accuracy
✅ RESTful API with rate limiting and health checks
✅ Responsive UI with drag-and-drop upload
✅ Redis caching for performance optimization
✅ Docker containerization for easy deployment

---

## 📁 Project Structure

```
imagefind/
├── backend/                          # Python FastAPI Backend
│   ├── backend_server.py            # Main API server
│   ├── config.py                    # Configuration management
│   ├── requirements.txt             # Python dependencies
│   └── __init__.py
│
├── frontend/                         # React + TypeScript Frontend
│   ├── src/
│   │   ├── components/              # React components
│   │   │   ├── AdvancedUpload.tsx
│   │   │   ├── ImageCard.tsx
│   │   │   ├── ImageUpload.tsx
│   │   │   ├── ImageUploadNew.tsx
│   │   │   ├── SearchResults.tsx
│   │   │   └── StatsPanel.tsx
│   │   ├── services/
│   │   │   └── api.ts              # API client
│   │   ├── types/
│   │   │   └── index.ts            # TypeScript types
│   │   ├── App.tsx
│   │   ├── main.tsx
│   │   └── vite-env.d.ts
│   ├── package.json
│   ├── tsconfig.json
│   ├── vite.config.ts
│   └── index.html
│
├── ml/                              # Machine Learning Module
│   ├── unified_feature_extractor.py # Base feature extractor (ResNet-50)
│   ├── feature_extractors/          # Alternative extractors
│   │   ├── vit_extractor.py        # Vision Transformer
│   │   ├── ensemble_extractor.py   # Ensemble approach
│   │   └── __init__.py
│   ├── quantum/                     # Quantum algorithms
│   │   ├── ae_qip_algorithm.py     # Core quantum algorithm
│   │   ├── ae_qip_v3.py            # Version 3 implementation
│   │   ├── ae_qip_v4.py            # Version 4 implementation
│   │   └── __init__.py
│   └── __init__.py
│
├── services/                        # External Service Integrations
│   ├── cloudinary_service.py        # Image CDN service
│   ├── pinecone_service.py          # Vector database service
│   ├── cache_service.py             # Redis caching layer
│   └── __init__.py
│
├── scripts/                         # Utility Scripts
│   ├── setup/
│   │   ├── create_env.py           # Environment setup
│   │   └── setup_cloudinary_pinecone.py
│   ├── upload/
│   │   ├── upload_healthcare.py    # Healthcare image upload
│   │   ├── upload_satellite.py     # Satellite image upload
│   │   └── upload_surveillance.py  # Surveillance image upload
│   ├── maintenance/
│   │   └── verify_image.py         # Image verification
│   ├── utils/
│   │   ├── check_db.py             # Database health check
│   │   ├── check_stats.py          # System statistics
│   │   └── debug_upload.py         # Upload debugging
│   └── __init__.py
│
├── tests/                           # Test Suite
│   ├── unit/
│   │   └── test_connection.py      # Connection tests
│   ├── integration/
│   │   ├── test_upload.py          # Upload flow tests
│   │   └── test_image_search.py    # Search functionality tests
│   ├── feature/
│   │   ├── test_feature_consistency.py
│   │   ├── test_quantum_algorithm.py
│   │   └── test_randomness.py
│   └── __init__.py
│
├── src/                             # Additional modules
│   ├── cloud/                       # Cloud integration
│   │   └── __init__.py
│   └── __init__.py
│
├── data/                            # Data storage
│   └── uploads/                     # Local uploads (Docker volume)
│
├── Docker Files
│   ├── Dockerfile                   # Multi-stage Docker build
│   ├── docker-compose.yml           # Docker Compose configuration
│   ├── docker-start.sh              # Start script (Linux/Mac)
│   ├── docker-start.bat             # Start script (Windows)
│   ├── entrypoint.sh                # Container entry point
│   └── .dockerignore
│
├── Test & Demo Scripts
│   ├── test_api.py                  # API testing
│   ├── test_system.py               # System integration test
│   ├── test_v3_improvements.py      # Feature testing
│   ├── healthcare_uploader.py       # Healthcare data loader
│   ├── main.py                      # Main entry point
│
├── Configuration Files
│   ├── requirements.txt             # Python dependencies
│   ├── .env.example                 # Environment variables template
│   ├── .env.template                # Alternative env template
│   ├── .gitignore                   # Git ignore rules
│   └── .vscode/                     # VS Code settings
│
└── Startup Scripts
    ├── setup.bat                    # Windows setup
    ├── start_backend.bat            # Windows backend start
    ├── start_backend_new.bat        # Alternative backend start
    └── start_frontend.bat           # Windows frontend start
```

---

## 🚀 Quick Start

### Prerequisites
- **Python 3.13+**
- **Node.js 18+**
- **Docker & Docker Compose**
- **Git**

### Installation

#### 1. Clone the Repository
```bash
git clone https://github.com/vineethkumarrao/finalcheck.git
cd finalcheck
```

#### 2. Environment Setup
```bash
# Copy environment template
cp .env.example .env

# Add your credentials to .env
# Required:
# - CLOUDINARY_CLOUD_NAME
# - CLOUDINARY_API_KEY
# - CLOUDINARY_API_SECRET
# - PINECONE_API_KEY
# - PINECONE_ENVIRONMENT
# - PINECONE_INDEX_NAME
```

#### 3. Using Docker (Recommended)
```bash
# Build and run containers
docker-compose up --build

# Containers will start on:
# - Frontend: http://localhost:5000
# - Backend API: http://localhost:8000
```

#### 4. Local Development Setup

**Backend:**
```bash
cd backend
pip install -r requirements.txt
python -m uvicorn backend_server:app --host 0.0.0.0 --port 8000 --reload
```

**Frontend:**
```bash
cd frontend
npm install
npm run dev
# Runs on http://localhost:5173
```

---

## 📚 Technology Stack

### Backend
| Technology | Purpose | Version |
|------------|---------|---------|
| **FastAPI** | Web framework | >=0.115.0 |
| **Uvicorn** | ASGI server | >=0.31.0 |
| **PyTorch** | Deep learning | >=2.6.0 |
| **TorchVision** | Computer vision | >=0.17.0 |
| **Qiskit** | Quantum computing | >=1.0.2 |
| **Pinecone** | Vector database | >=7.0.0 |
| **Cloudinary** | Image CDN | >=1.44.0 |
| **Redis** | Caching layer | >=5.0.0 |
| **SlowAPI** | Rate limiting | >=0.1.9 |

### Frontend
| Technology | Purpose | Version |
|------------|---------|---------|
| **React** | UI framework | ^18.2.0 |
| **TypeScript** | Type safety | ^5.2.2 |
| **Vite** | Build tool | ^5.0.8 |
| **Material-UI** | Component library | ^5.15.0 |
| **Axios** | HTTP client | ^1.6.2 |
| **React-Dropzone** | File upload | ^14.2.3 |

### DevOps
| Tool | Purpose |
|------|---------|
| **Docker** | Containerization |
| **Docker Compose** | Multi-container orchestration |
| **Python 3.13** | Backend runtime |
| **Node.js 18** | Frontend build tool |

---

## 🔧 API Endpoints

### Health & Stats
```
GET /health                 # Health check
GET /api/stats             # System statistics
```

### Image Upload & Search
```
POST /api/upload                    # Simple upload
POST /api/upload-and-store          # Upload + store in vector DB
POST /api/search                    # Similarity search
GET /api/search/{category}          # Category-specific search
```

**Supported image formats:** JPEG (`.jpg`, `.jpeg`), PNG (`.png`), GIF (`.gif`), WebP (`.webp`)

### Request/Response Examples

**Upload Image:**
```bash
curl -X POST http://localhost:8000/api/upload \
  -F "file=@image.jpg" \
  -F "category=healthcare"
```

**Response:**
```json
{
  "status": "success",
  "message": "Image uploaded successfully",
  "data": {
    "filename": "image",
    "url": "https://res.cloudinary.com/.../image.jpg",
    "features": [0.123, 0.456, ...],
    "uploaded_at": "2025-10-28T16:00:00"
  }
}
```

**Search:**
```bash
curl -X POST http://localhost:8000/api/search \
  -H "Content-Type: application/json" \
  -d '{
    "image_file": "base64_encoded_image",
    "top_k": 5,
    "min_score": 0.85
  }'
```

---

## 🤖 Machine Learning Features

### Feature Extraction

#### 1. **Unified Feature Extractor** (Default)
- **Model**: ResNet-50 (ImageNet pre-trained)
- **Output Dimension**: 2048D vectors
- **Input**: 224×224 RGB images
- **Device**: CPU/GPU auto-detection
- **Location**: `ml/unified_feature_extractor.py`

#### 2. **Vision Transformer (ViT)**
- Alternative state-of-the-art model
- Better for diverse image domains
- Location: `ml/feature_extractors/vit_extractor.py`

#### 3. **Ensemble Extractor**
- Combines multiple models
- Higher accuracy, higher latency
- Location: `ml/feature_extractors/ensemble_extractor.py`

**Configuration:**
```python
# In backend/config.py
FEATURE_EXTRACTOR = 'resnet'  # Options: 'resnet', 'vit', 'ensemble'
FEATURE_DIMENSION = 2048
```

### Quantum-Inspired Algorithms

The system implements quantum-inspired image processing using Qiskit:

#### Amplitude Encoding with Quantum Image Processing (AE-QIP)

**Versions:**
- `ae_qip_algorithm.py` - Base implementation
- `ae_qip_v3.py` - Optimized version 3
- `ae_qip_v4.py` - Latest version 4

**Key Features:**
```python
# Quantum parameters
N_ENCODING_QUBITS = 3        # Qubit encoding depth
N_AUXILIARY_QUBITS = 7       # Auxiliary qubits for processing
USE_QUANTUM_INSPIRED = True  # Enable quantum processing
```

**Benefits:**
- Enhanced feature representation
- Improved similarity matching
- Quantum-inspired dimensionality reduction

---

## 🗄️ Database Integration

### Pinecone Vector Database

**Purpose**: Fast similarity search on image features

**Configuration:**
```python
PINECONE_API_KEY = "your_api_key"
PINECONE_ENVIRONMENT = "us-east-1"
PINECONE_INDEX_NAME = "quantum-images-prod"
```

**Features:**
- 2048-dimensional vectors (ResNet-50 output)
- Metadata filtering by image category
- Top-K similarity retrieval
- Real-time vector indexing

**Example Usage:**
```python
# Search for similar images
results = pinecone_service.search(
    query_features=feature_vector,
    top_k=10,
    min_score=0.85,
    category_filter='healthcare'
)
```

### Cloudinary Image CDN

**Purpose**: Image storage, optimization, and delivery

**Services:**
- Automatic image optimization
- Multiple format delivery (JPEG, WebP, PNG)
- Responsive image transformations
- Global CDN distribution

**Configuration:**
```python
CLOUDINARY_CLOUD_NAME = "your_cloud"
CLOUDINARY_API_KEY = "your_key"
CLOUDINARY_API_SECRET = "your_secret"
```

### Redis Cache

**Purpose**: Feature vector and result caching

**Configuration:**
```python
REDIS_HOST = "localhost"
REDIS_PORT = 6379
REDIS_DB = 0
```

**Cached Items:**
- Feature vectors (TTL: 24 hours)
- Search results
- Image metadata

---

## 📊 Image Categories

The system supports three primary image categories:

### 1. Healthcare
- Medical imaging (X-rays, CT scans)
- Clinical documentation
- Health records
- Path: `scripts/upload/upload_healthcare.py`

### 2. Satellite
- Earth observation imagery
- Geographical mapping
- Climate monitoring
- Path: `scripts/upload/upload_satellite.py`

### 3. Surveillance
- Security camera footage
- Traffic monitoring
- Event detection
- Path: `scripts/upload/upload_surveillance.py`

---

## 🧪 Testing

### Test Suite Structure

```
tests/
├── unit/              # Individual component tests
├── integration/       # End-to-end flow tests
└── feature/          # Feature-specific tests
```

### Running Tests

**All Tests:**
```bash
pytest tests/
```

**Specific Test Suite:**
```bash
pytest tests/unit/test_connection.py
pytest tests/integration/test_upload.py
pytest tests/feature/test_quantum_algorithm.py
```

**With Coverage:**
```bash
pytest tests/ --cov=. --cov-report=html
```

### Test Files

| File | Purpose |
|------|---------|
| `test_connection.py` | Service connectivity |
| `test_upload.py` | Upload workflow |
| `test_image_search.py` | Search functionality |
| `test_feature_consistency.py` | Feature extraction consistency |
| `test_quantum_algorithm.py` | Quantum algorithm correctness |
| `test_randomness.py` | Randomness validation |

---

## 🐳 Docker Deployment

### Dockerfile Overview

Multi-stage build process:

**Stage 1: Frontend Builder**
- Node.js 18-Alpine
- Builds React app with Vite
- Output: `/app/frontend/dist`

**Stage 2: Backend Runtime**
- Python 3.13-Slim
- Installs all dependencies
- Copies built frontend
- Starts both services

### Services

**Backend API:**
- Port: 8000
- Framework: FastAPI + Uvicorn
- Command: `python -m backend.backend_server`

**Frontend Server:**
- Port: 5000
- Method: Python HTTP server
- Directory: `frontend/dist`

### Docker Compose

```yaml
services:
  backend:
    build:
      context: .
      dockerfile: Dockerfile
    ports:
      - "8000:8000"
      - "5000:5000"
    environment:
      - CLOUDINARY_CLOUD_NAME
      - PINECONE_API_KEY
      # ... other env vars
    volumes:
      - ./data/uploads:/app/data/uploads
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
```

### Running Docker

**Build:**
```bash
docker-compose build --no-cache
```

**Start:**
```bash
docker-compose up -d
```

**Stop:**
```bash
docker-compose down
```

**View Logs:**
```bash
docker-compose logs -f backend
```

---

## 📝 Configuration

### Environment Variables

Create `.env` file:

```env
# Cloudinary
CLOUDINARY_CLOUD_NAME=your_cloud_name
CLOUDINARY_API_KEY=your_api_key
CLOUDINARY_API_SECRET=your_api_secret

# Pinecone
PINECONE_API_KEY=your_pinecone_key
PINECONE_ENVIRONMENT=us-east-1
PINECONE_INDEX_NAME=quantum-images-prod

# Feature Extraction
FEATURE_EXTRACTOR_TYPE=resnet  # resnet, vit, ensemble
FEATURE_DIMENSION=2048

# Quantum Parameters
N_ENCODING_QUBITS=3
N_AUXILIARY_QUBITS=7
USE_QUANTUM_INSPIRED=True

# Server
HOST=0.0.0.0
PORT=8000
DEBUG=True

# Redis (optional)
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0

# Thresholds
HIGH_CONFIDENCE_THRESHOLD=0.95
GOOD_CONFIDENCE_THRESHOLD=0.85
MINIMUM_MATCH_THRESHOLD=0.80
```

### Backend Configuration

`backend/config.py` contains all settings:

```python
class Config:
    # Cloudinary settings
    CLOUDINARY_CLOUD_NAME = os.getenv('CLOUDINARY_CLOUD_NAME', '')
    CLOUDINARY_API_KEY = os.getenv('CLOUDINARY_API_KEY', '')
    CLOUDINARY_API_SECRET = os.getenv('CLOUDINARY_API_SECRET', '')
    
    # Pinecone settings
    PINECONE_API_KEY = os.getenv('PINECONE_API_KEY', '')
    PINECONE_ENVIRONMENT = os.getenv('PINECONE_ENVIRONMENT', 'us-east-1')
    PINECONE_INDEX_NAME = os.getenv('PINECONE_INDEX_NAME', 'quantum-images-prod')
    
    # Feature extraction
    FEATURE_EXTRACTOR = 'resnet'
    FEATURE_DIMENSION = 2048
    
    # Confidence thresholds
    HIGH_CONFIDENCE_THRESHOLD = 0.95
    GOOD_CONFIDENCE_THRESHOLD = 0.85
    MINIMUM_MATCH_THRESHOLD = 0.80
```

---

## 🔐 Security Features

### Rate Limiting
- Uses **SlowAPI** for request throttling
- Prevents abuse and DoS attacks
- Configurable per endpoint

### CORS Middleware
- Restricts cross-origin requests
- Configurable allowed origins
- Prevents unauthorized API access

### Environment Variables
- Secrets stored in `.env`
- Never committed to version control
- Loaded via `python-dotenv`

### Input Validation
- File type verification
- Size constraints
- Malicious content detection

---

## 📈 Performance Optimization

### Caching Strategy
1. **Feature Vector Cache** (Redis)
   - 24-hour TTL
   - Reduces computation overhead
   - Fast retrieval

2. **Search Result Cache**
   - Caches similar image sets
   - Reduces Pinecone queries

3. **Model Weight Cache**
   - Local PyTorch model cache
   - Prevents re-download

### Database Optimization
- **Vector Indexing**: Pinecone handles indexing
- **Metadata Filtering**: Category-based filtering
- **Query Optimization**: Top-K retrieval efficiency

### Frontend Optimization
- **Code Splitting**: Lazy loading components
- **Image Optimization**: Cloudinary transformations
- **Caching**: Browser cache for static assets

---

## 🚨 Troubleshooting

### Common Issues

**1. ModuleNotFoundError: No module named 'config'**
```bash
# Solution: Ensure Python path is set correctly
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
```

**2. Cloudinary Upload Fails**
```bash
# Check credentials
echo $CLOUDINARY_CLOUD_NAME
echo $CLOUDINARY_API_KEY

# Verify in .env file
cat .env
```

**3. Pinecone Connection Error**
```bash
# Verify API key and environment
python -c "from pinecone import Pinecone; pc = Pinecone(api_key='YOUR_KEY')"
```

**4. Redis Connection Refused**
```bash
# Start Redis (optional - app continues without cache)
redis-server
# or with Docker
docker run -d -p 6379:6379 redis
```

**5. Docker Build Fails**
```bash
# Clear Docker cache and rebuild
docker system prune -f
docker-compose build --no-cache
```

### Debug Logging

Enable detailed logging:

```python
# In backend_server.py
logging.basicConfig(level=logging.DEBUG)

# Or via environment
export LOG_LEVEL=DEBUG
```

---

## 📚 API Documentation

### Interactive API Docs

When backend is running:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Example Workflows

**Workflow 1: Upload & Search**
```bash
# 1. Upload image
curl -X POST http://localhost:8000/api/upload \
  -F "file=@test.jpg" \
  -F "category=healthcare"

# 2. Get image ID from response
IMAGE_ID="quantum-images_healthcare_test"

# 3. Search similar images
curl -X POST http://localhost:8000/api/search \
  -H "Content-Type: application/json" \
  -d '{"image_file": "base64_data", "category": "healthcare"}'
```

**Workflow 2: Batch Upload**
```bash
# Upload multiple healthcare images
for file in healthcare_images/*.jpg; do
    curl -X POST http://localhost:8000/api/upload \
      -F "file=@$file" \
      -F "category=healthcare"
done
```

---

## 🤝 Contributing

### Development Workflow

1. Create feature branch: `git checkout -b feature/your-feature`
2. Make changes and test: `pytest tests/`
3. Commit with descriptive message: `git commit -m "Add your feature"`
4. Push to GitHub: `git push origin feature/your-feature`
5. Create Pull Request

### Code Style

- **Backend**: PEP 8 (Python)
- **Frontend**: ESLint + Prettier (TypeScript/React)
- **Formatting**: Auto-format on save (VS Code)

---

## 📄 License

This project is proprietary. All rights reserved.

---

## 👤 Author

**vineethkumarrao**
- GitHub: [@vineethkumarrao](https://github.com/vineethkumarrao)
- Project: [finalcheck](https://github.com/vineethkumarrao/finalcheck)

---

## 🆘 Support

For issues, questions, or suggestions:
1. Check existing GitHub issues
2. Create a new issue with detailed description
3. Include error logs and reproduction steps

---

## 🎓 Learning Resources

### Quantum Computing with Qiskit
- [Qiskit Documentation](https://docs.quantum.ibm.com/)
- [Quantum Computing Concepts](https://www.ibm.com/quantum)

### Deep Learning with PyTorch
- [PyTorch Tutorials](https://pytorch.org/tutorials/)
- [ResNet Paper](https://arxiv.org/abs/1512.03385)

### Vector Databases
- [Pinecone Docs](https://docs.pinecone.io/)
- [Vector Search Explained](https://www.pinecone.io/learn/vector-search/)

### FastAPI
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [API Best Practices](https://swagger.io/resources/articles/best-practices-in-api-design/)

---

**Last Updated**: October 28, 2025
**Version**: 1.0.0
**Status**: Production Ready ✅
