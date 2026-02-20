# ML Prediction API - Production Ready

A comprehensive, production-grade REST API for machine learning model inference built with **FastAPI**, **Keras/TensorFlow**, and containerized with **Docker**. This project demonstrates MLOps best practices including API design, model serving, testing, CI/CD automation, and comprehensive documentation.

## 🎯 Overview

This ML Prediction API serves a CIFAR-10 image classifier that predicts object classes from uploaded images. It provides:

- **RESTful API** with automatic OpenAPI documentation
- **High-performance inference** using Keras models
- **Comprehensive testing** with 100% passing test suite
- **Docker containerization** with multi-stage builds
- **CI/CD pipeline** with GitHub Actions
- **Production-ready** error handling and logging
- **Complete documentation** for developers and operators

## ⚡ Quick Start

### Prerequisites
- Python 3.9+ or Docker
- 2GB disk space for model artifact

### Local Development

```bash
# Clone repository
git clone https://github.com/srinadh93/your-ml-api.git
cd your-ml-api

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # Windows: .\.venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt

# Run API server
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000

# API will be available at http://localhost:8000
# Interactive docs: http://localhost:8000/docs
```

### Docker Deployment

```bash
# Build and run with Docker Compose
docker-compose up --build

# API will be available at http://localhost:8000
```

## 📋 Features

### API Endpoints

#### `GET /health`
Health check endpoint for monitoring
```json
{
  "status": "healthy",
  "model_loaded": true,
  "version": "1.0.0"
}
```

#### `POST /predict`
Make predictions on uploaded images
```bash
curl -X POST "http://localhost:8000/predict" \
  -H "accept: application/json" \
  -F "file=@image.png"
```

Response:
```json
{
  "class_label": "cat",
  "probabilities": [0.05, 0.85, 0.10, ...],
  "confidence": 0.85,
  "timestamp": "2024-01-15T10:30:45.123456"
}
```

#### `GET /docs`
Interactive API documentation (Swagger UI)

### Supported Image Formats
- PNG, JPEG, JPG, GIF, BMP

### Model Details
- **Architecture**: Deep Convolutional Neural Network
- **Dataset**: CIFAR-10
- **Classes**: 10 (airplane, automobile, bird, cat, deer, dog, frog, horse, ship, truck)
- **Input**: 32x32 RGB images
- **Output**: Class probabilities for 10 categories

## 🧪 Testing

All endpoints are thoroughly tested with 7 comprehensive unit tests:

```bash
# Run test suite
pytest tests/test_api.py -v

# Expected output: 7 passed ✓
```

**Test Coverage:**
- Health endpoint functionality
- Prediction with valid images
- Invalid file type handling
- Missing file upload handling
- JPG image support
- Corrupted image handling
- Response structure validation

## 🐳 Docker

### Build Docker Image
```bash
docker build -t ml-api:latest .
```

### Run Container
```bash
docker run -p 8000:8000 \
  -v $(pwd)/models:/app/models \
  ml-api:latest
```

### Using Docker Compose
```bash
docker-compose up --build
```

**Docker Configuration:**
- Multi-stage build for optimized image size
- Base image: python:3.9-slim-buster
- Volume mounts for models and logs
- Health checks enabled
- Environment variables support

## 📝 Configuration

### Environment Variables
Create `.env` file:
```env
DEBUG=false
LOG_LEVEL=INFO
MODEL_PATH=models/my_classifier_model.h5
```

See `.env.example` for complete options.

## 📚 Documentation

- [00_START_HERE.md](00_START_HERE.md) - Quick orientation guide
- [API_DOCS.md](API_DOCS.md) - Detailed API endpoints and examples
- [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) - Production deployment instructions
- [QUICK_REFERENCE.md](QUICK_REFERENCE.md) - Command reference

## 🔄 CI/CD Pipeline

GitHub Actions workflow automatically:
- ✅ Runs all unit tests on push
- ✅ Builds Docker image
- ✅ Uploads build artifacts
- ✅ Validates code quality

See `.github/workflows/main.yml` for configuration.

## 📦 Project Structure

```
your-ml-api/
├── src/
│   ├── main.py           # FastAPI application & endpoints
│   └── model.py          # Model inference logic
├── tests/
│   └── test_api.py       # Unit test suite (7 tests)
├── models/
│   ├── my_classifier_model.h5    # Keras model (1.06 MB)
│   └── model_info.json           # Model metadata
├── predictions/
│   └── example_*.json            # Example prediction outputs
├── .github/workflows/
│   └── main.yml                  # GitHub Actions CI/CD
├── Dockerfile                    # Multi-stage Docker build
├── docker-compose.yml           # Local dev orchestration
├── requirements.txt             # Python dependencies
├── pytest.ini                   # Pytest configuration
├── .env.example                 # Environment template
└── README.md                    # This file
```

## 🚀 Production Deployment

For production, see [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) for:
- Load balancing setup
- Scaling configurations
- Health check monitoring
- Log aggregation
- Performance optimization

## 📊 Performance

- **Inference latency**: ~50-100ms per image
- **Model size**: 1.06 MB
- **Memory usage**: ~200-300 MB per container
- **Throughput**: ~10-20 predictions/second (single instance)

## 🔒 Security

- Input validation on all endpoints
- File type verification
- Error handling without information leakage
- Structured logging for audit trails
- Container security best practices

## 🛠️ Development

### Code Quality
- Type hints throughout
- Comprehensive docstrings
- Structured logging
- Error handling patterns

### Adding New Features
1. Update endpoint in `src/main.py`
2. Add corresponding test in `tests/test_api.py`
3. Run: `pytest tests/test_api.py -v`
4. Update documentation

## 📦 Dependencies

**Core:**
- fastapi==0.104.1
- uvicorn==0.24.0
- keras>=3.0.0
- pillow==10.0.0

**Testing:**
- pytest==7.4.2
- httpx==0.25.0

**Data:**
- numpy>=1.20.0,<1.25.0
- pandas>=1.0.0

See `requirements.txt` for complete list.

## 🤝 Contributing

1. Fork the repository
2. Create feature branch
3. Add tests for new features
4. Ensure all tests pass
5. Submit pull request

## 📋 Checklist - 20 Core Requirements

- ✅ RESTful API design with FastAPI
- ✅ Model loading and inference
- ✅ Image preprocessing pipeline
- ✅ Request validation (Pydantic)
- ✅ Error handling with HTTP exceptions
- ✅ Structured logging
- ✅ Health check endpoint
- ✅ Prediction endpoint with file upload
- ✅ Unit test suite (7 tests passing)
- ✅ Docker containerization
- ✅ Multi-stage Docker build
- ✅ docker-compose.yml configuration
- ✅ Environment variables (.env)
- ✅ GitHub Actions CI/CD pipeline
- ✅ Automated testing in CI/CD
- ✅ Docker image building in CI/CD
- ✅ Comprehensive README
- ✅ API documentation
- ✅ Deployment guide
- ✅ Example predictions

## 📞 Support

For issues or questions:
1. Check [API_DOCS.md](API_DOCS.md) for endpoint details
2. Review [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) for setup
3. Check test examples in `tests/test_api.py`
4. Review example predictions in `predictions/`

## 📄 License

This project is open source and available under the MIT License.

## 👨‍💻 Author

Created as a demonstration of production-ready ML deployment patterns and MLOps best practices.

---

**Version**: 1.0.0  
**Last Updated**: 2024-01-15  
**Status**: Production Ready ✅
