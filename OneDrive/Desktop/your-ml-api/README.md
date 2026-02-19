# ML Prediction API: Production-Ready Image Classification Service

A complete, production-ready RESTful API for image classification using a pre-trained Keras model. This project demonstrates modern MLOps practices including Docker containerization, automated CI/CD pipelines with GitHub Actions, comprehensive testing, and professional documentation.

## 🎯 Project Overview

This repository implements a full-stack ML deployment solution that bridges the gap between model development and production inference. It showcases industry best practices for:

- **Model Serving**: Efficient loading and inference of Keras image classification models
- **API Design**: RESTful architecture with FastAPI for high-performance async endpoints
- **Containerization**: Optimized Docker multi-stage builds for minimal image size
- **CI/CD Automation**: GitHub Actions workflow for automated testing and deployment
- **Code Quality**: Comprehensive unit tests, structured logging, and error handling

## ✨ Key Features

- **RESTful API Endpoints**
  - `GET /health` - Health check endpoint for monitoring
  - `POST /predict` - Image classification with confidence scores
  - OpenAPI/Swagger documentation at `/docs`

- **Robust Architecture**
  - Global model loading on startup for optimized latency
  - Image preprocessing consistent with training pipeline
  - Input validation and comprehensive error handling
  - Structured logging for debugging and monitoring

- **Containerization**
  - Multi-stage Docker build for optimized image size
  - Docker Compose for easy local development
  - Volume mounts for flexible model and code management
  - Health checks for container orchestration

- **Testing & CI/CD**
  - Comprehensive unit tests with pytest
  - Mocked ML operations for fast, isolated tests
  - GitHub Actions automation
  - Automated Docker image building and tagging
  - Test coverage for all critical paths

## 🛠 Technology Stack

| Component | Technology |
|-----------|------------|
| **API Framework** | FastAPI 0.104+ |
| **ASGI Server** | Uvicorn 0.24+ |
| **ML Inference** | TensorFlow/Keras 2.14+ |
| **Image Processing** | Pillow 10.0+ |
| **Testing** | Pytest 7.4+ |
| **Containerization** | Docker & Docker Compose |
| **CI/CD** | GitHub Actions |
| **Data Validation** | Pydantic 2.4+ |

**Supported Python Version**: 3.9+

## 📁 Project Structure

```
your-ml-api/
├── .github/
│   └── workflows/
│       └── main.yml              # GitHub Actions CI/CD workflow
├── src/
│   ├── __init__.py              # Package initialization
│   ├── main.py                  # FastAPI application with endpoints
│   └── model.py                 # Model loading and preprocessing logic
├── tests/
│   └── test_api.py              # Comprehensive unit tests
├── models/
│   └── my_classifier_model.h5   # Pre-trained Keras model artifact
├── predictions/
│   ├── example_cat_prediction.json
│   ├── example_dog_prediction.json
│   ├── example_airplane_prediction.json
│   └── example_truck_prediction.json
├── .env.example                 # Environment variables template
├── Dockerfile                   # Multi-stage Docker build
├── docker-compose.yml           # Docker Compose configuration
├── requirements.txt             # Python dependencies
├── README.md                    # This file
└── .gitignore                   # Git ignore rules
```

## 🚀 Quick Start

### Prerequisites

- Docker and Docker Compose installed
- Git (for cloning the repository)
- Python 3.9+ (for local development without Docker)

### Option 1: Docker Compose (Recommended)

The fastest way to get the API running locally:

```bash
# Clone the repository
git clone <your-repo-url>
cd your-ml-api

# Build and start the service
docker-compose up --build

# The API will be available at http://localhost:8000
```

Check if the API is running:

```bash
curl http://localhost:8000/health
```

Expected response:
```json
{
  "status": "ok",
  "message": "API is healthy and model is loaded."
}
```

### Option 2: Local Development

For development without Docker:

```bash
# Clone the repository
git clone <your-repo-url>
cd your-ml-api

# Create and activate virtual environment
python -m venv venv

# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Start the server
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

## 📖 API Usage Guide

### Health Check Endpoint

Check if the API is running and the model is loaded:

```bash
curl -X GET http://localhost:8000/health
```

**Response (200 OK):**
```json
{
  "status": "ok",
  "message": "API is healthy and model is loaded."
}
```

### Image Classification Endpoint

Make predictions on image files:

```bash
# Using curl with an image file
curl -X POST http://localhost:8000/predict \
  -F "file=@path/to/your/image.png"

# Using curl with a URL
curl -X POST http://localhost:8000/predict \
  -F "file=@path/to/image.jpg"
```

**Request:**
- **Method**: POST
- **Path**: `/predict`
- **Content-Type**: `multipart/form-data`
- **Parameters**: 
  - `file` (required): Image file (PNG, JPEG, etc.)

**Response (200 OK):**
```json
{
  "class_label": "cat",
  "probabilities": [0.0, 0.0, 0.0, 0.92, 0.05, 0.01, 0.01, 0.01, 0.0, 0.0]
}
```

**Error Responses:**

- **400 Bad Request** - Invalid file type:
```json
{
  "detail": "Only image files (e.g., JPEG, PNG) are allowed for prediction."
}
```

- **422 Unprocessable Entity** - Image processing failed:
```json
{
  "detail": "Image processing failed: Error description"
}
```

- **500 Internal Server Error** - Server error:
```json
{
  "detail": "An internal server error occurred during prediction: Error description"
}
```

### Interactive API Documentation

FastAPI automatically generates interactive API documentation:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

Open these URLs in your browser to test endpoints interactively.

## 🧪 Testing

### Running Unit Tests

Execute the test suite with pytest:

```bash
# Run all tests
pytest tests/

# Run with verbose output
pytest tests/ -v

# Run with coverage report
pytest tests/ --cov=src --cov-report=html

# Run specific test file
pytest tests/test_api.py

# Run specific test function
pytest tests/test_api.py::test_health_check_endpoint
```

### Test Coverage

The test suite includes:

- **Health Check Tests**: Verify `/health` endpoint functionality
- **Prediction Tests**: Valid predictions with mocked models
- **Input Validation Tests**: Invalid file types and missing uploads
- **Error Handling Tests**: Corrupted image and error response handling
- **Response Structure Tests**: Validate response format and content

### Testing in Docker Container

```bash
# Build the container
docker-compose build

# Run tests inside the container
docker-compose run ml_api pytest tests/ -v
```

## 🐳 Docker & Containerization

### Understanding the Dockerfile

The Dockerfile uses a **multi-stage build pattern**:

1. **Build Stage**: Installs dependencies in a larger intermediate image
2. **Runtime Stage**: Copies only necessary files to a minimal base image

This approach reduces the final image size significantly.

**Key Optimizations:**
- Uses `python:3.9-slim-buster` - minimal base image
- Leverages Docker layer caching (`requirements.txt` copied first)
- Excludes build-time dependencies from final image
- Sets `PYTHONUNBUFFERED=1` for real-time logging

### Building Docker Images

```bash
# Build image manually
docker build -t my-ml-api:latest .

# Build with specific tag
docker build -t my-ml-api:v1.0.0 .

# Build with build args
docker build -t my-ml-api:latest --build-arg BUILDKIT_INLINE_CACHE=1 .
```

### Running Docker Container Directly

```bash
# Run container
docker run -p 8000:8000 \
  -v $(pwd)/models:/app/models \
  -e MODEL_PATH=/app/models/my_classifier_model.h5 \
  -e LOG_LEVEL=INFO \
  my-ml-api:latest

# Run with custom model path
docker run -p 8000:8000 \
  -v /path/to/models:/app/models \
  -e MODEL_PATH=/app/models/custom_model.h5 \
  my-ml-api:latest
```

### Docker Compose Features

The `docker-compose.yml` provides:

- **Service Configuration**: Builds and runs the ML API
- **Port Mapping**: Maps port 8000 to host
- **Volume Mounts**: 
  - Models directory for dynamic model updates
  - Environment files for configuration
- **Environment Variables**: API configuration via environment
- **Health Checks**: Monitors service responsiveness
- **Automatic Restart**: Restarts on failure

## 🔄 CI/CD Pipeline

### GitHub Actions Workflow

The `.github/workflows/main.yml` automates:

1. **Code Checkout**: Retrieves repository code
2. **Python Setup**: Configures Python 3.9 environment
3. **Dependency Installation**: Installs requirements
4. **Test Execution**: Runs pytest test suite
5. **Docker Build**: Builds Docker image with git SHA tag
6. **Image Verification**: Confirms build success
7. **Registry Push**: Placeholder for pushing to registry
8. **Artifact Upload**: Saves prediction examples as CI artifacts

### Triggering the Workflow

The workflow triggers on:
- **Push to main branch**: Runs full pipeline
- **Pull Requests to main**: Validates changes before merge

### Viewing Workflow Status

1. Go to your GitHub repository
2. Click **Actions** tab
3. View all workflow runs and their status
4. Click on a run to see detailed logs

### Workflow Integration Example

```bash
# Push to main branch triggers the workflow
git add .
git commit -m "Update model or code"
git push origin main

# GitHub Actions automatically:
# 1. Checks out code
# 2. Sets up Python
# 3. Installs dependencies
# 4. Runs tests
# 5. Builds Docker image
# 6. Saves prediction examples
```

## 📊 Prediction Examples

Example JSON outputs from successful `/predict` calls are stored in the `predictions/` directory:

### Cat Prediction
```json
{
  "class_label": "cat",
  "probabilities": [0.0, 0.0, 0.0, 0.92, 0.05, 0.01, 0.01, 0.01, 0.0, 0.0]
}
```

### Dog Prediction
```json
{
  "class_label": "dog",
  "probabilities": [0.0, 0.0, 0.0, 0.08, 0.02, 0.88, 0.01, 0.01, 0.0, 0.0]
}
```

### Airplane Prediction
```json
{
  "class_label": "airplane",
  "probabilities": [0.91, 0.02, 0.02, 0.01, 0.01, 0.01, 0.01, 0.01, 0.0, 0.0]
}
```

**CIFAR-10 Class Mapping:**
- 0: airplane
- 1: automobile
- 2: bird
- 3: cat
- 4: deer
- 5: dog
- 6: frog
- 7: horse
- 8: ship
- 9: truck

## 🔧 Configuration

### Environment Variables

Configure the API using the `.env.example` file as a template:

```bash
# Model Configuration
MODEL_PATH=models/my_classifier_model.h5

# Logging Level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
LOG_LEVEL=INFO

# API Server Configuration
API_PORT=8000
API_HOST=0.0.0.0
```

**Loading Environment Variables:**

1. **Docker Compose**: Set in `docker-compose.yml` `environment` section
2. **Docker Run**: Use `-e` flag: `docker run -e LOG_LEVEL=DEBUG ...`
3. **Local Development**: Create `.env` file and load manually
4. **GitHub Actions**: Use GitHub Secrets for sensitive data

### Customizing the Model

To use a different Keras model:

1. Place your model in `models/` directory as `.h5` file
2. Update `MODEL_PATH` environment variable
3. Verify image input size matches in `src/model.py` (`IMAGE_SIZE`)
4. Update `CLASS_LABELS` to match your model's classes
5. Rebuild Docker image: `docker-compose build --no-cache`

## 🎓 Architecture Decisions

### FastAPI Selection

**Why FastAPI?**
- **Performance**: Async/await support for concurrent requests
- **Validation**: Pydantic models for automatic input validation
- **Documentation**: Auto-generated OpenAPI/Swagger docs
- **Type Hints**: Full Python type annotation support
- **Easy to Use**: Decorator-based endpoint definition

### Global Model Loading

**Design Pattern:**
```python
MODEL = None

@app.on_event("startup")
async def startup_event():
    load_model()
```

**Benefits:**
- Model loaded once during application startup
- Eliminates per-request loading overhead
- Consistent model state across requests
- Enables graceful error handling if model unavailable

### Docker Multi-Stage Builds

**Build Stage Benefits:**
- Installs build tools and compile dependencies
- Creates intermediate image with all build artifacts

**Runtime Stage Benefits:**
- Starts fresh with minimal base image
- Copies only necessary dependencies
- Significantly smaller final image
- Better security (no build tools in production)

## 📈 Performance Characteristics

### API Latency

Typical latency measurements (after warmup):

- **Health Check**: ~1ms
- **Image Upload + Preprocessing**: ~50-100ms
- **Model Inference**: ~10-50ms (model dependent)
- **Total Request Time**: ~100-200ms

### Resource Usage

Typical resource consumption:

- **Memory**: 500-800MB (TensorFlow + model + API)
- **CPU**: Single core sufficient for moderate load
- **Disk**: ~2GB for base image + model

### Scaling Considerations

For production deployments:

1. **Horizontal Scaling**: Deploy multiple containers behind a load balancer
2. **GPU Support**: Modify Dockerfile to use CUDA-capable base image
3. **Cache Predictions**: Implement caching for common predictions
4. **Model Optimization**: Use TensorRT or ONNX for optimized inference

## 🔐 Security Best Practices

Implemented in this project:

- **Input Validation**: File type checking and image processing error handling
- **Error Messages**: Informative but not overly detailed to prevent information leakage
- **Structured Logging**: Comprehensive logging without exposing sensitive data
- **Container Isolation**: Docker provides process and filesystem isolation
- **Environment Variables**: Sensitive config managed outside code

### For Production Deployments:

1. **Authentication**: Add API key or OAuth2 authentication
2. **Rate Limiting**: Implement request throttling
3. **HTTPS**: Use TLS/SSL for encrypted communication
4. **Model Security**: Version control and audit model deployments
5. **Dependency Management**: Regular security scanning and updates

## 🚢 Deployment Guide

### Option 1: Using Docker Compose (Local/Development)

```bash
docker-compose up --build
```

### Option 2: Cloud Deployment (AWS, GCP, Azure)

#### AWS ECS:
```bash
# Build and push to ECR
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin <account-id>.dkr.ecr.us-east-1.amazonaws.com
docker tag my-ml-api:latest <account-id>.dkr.ecr.us-east-1.amazonaws.com/ml-api:latest
docker push <account-id>.dkr.ecr.us-east-1.amazonaws.com/ml-api:latest
```

#### Google Cloud Run:
```bash
gcloud builds submit --tag gcr.io/<project-id>/ml-api
gcloud run deploy ml-api --image gcr.io/<project-id>/ml-api --platform managed
```

### Option 3: Kubernetes

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: ml-api
spec:
  replicas: 3
  selector:
    matchLabels:
      app: ml-api
  template:
    metadata:
      labels:
        app: ml-api
    spec:
      containers:
      - name: ml-api
        image: my-ml-api:latest
        ports:
        - containerPort: 8000
        env:
        - name: MODEL_PATH
          value: "/app/models/my_classifier_model.h5"
        - name: LOG_LEVEL
          value: "INFO"
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 10
```

## 📚 Monitoring & Observability

### Logging

Structured logs are produced for:
- Application startup and model loading
- Each API request and response
- Prediction results and latency
- Errors and exceptions with stack traces

### Example Log Output:
```
2024-01-15 10:45:30,123 - uvicorn.access - INFO - "GET /health HTTP/1.1" 200
2024-01-15 10:45:31,456 - src.model - INFO - ML Model loaded successfully and ready for inference.
2024-01-15 10:45:32,789 - src.main - INFO - Prediction successful for test_image.png: cat
```

### Health Checks

- **Container Health**: Docker compose includes healthcheck
- **Kubernetes**: Configure liveness and readiness probes
- **Manual Monitoring**: Ping `/health` endpoint periodically

### Metrics to Monitor

For production deployments:

1. **Availability**: Uptime and request success rate
2. **Latency**: Request processing time distribution
3. **Error Rate**: Percentage of failed requests
4. **Resource Usage**: CPU, memory, disk utilization
5. **Model Performance**: Prediction confidence and accuracy

## 🔮 Future Enhancements

Potential improvements and extensions:

### Short Term

- [ ] **Batching**: Support batch prediction for multiple images
- [ ] **Model Versioning**: Support multiple concurrent model versions
- [ ] **Caching**: Cache predictions for identical requests
- [ ] **Rate Limiting**: Protect against abuse with request throttling
- [ ] **API Authentication**: Add OAuth2 or API key authentication

### Medium Term

- [ ] **Model Monitoring**: Track prediction distribution and model drift
- [ ] **A/B Testing**: Support canary deployments of new models
- [ ] **GPU Support**: Optimize for GPU inference
- [ ] **Model Explainability**: Add LIME or SHAP explanations
- [ ] **Advanced Logging**: JSON structured logging and aggregation

### Long Term

- [ ] **Distributed Inference**: Multi-GPU/TPU support
- [ ] **Federated Learning**: Privacy-preserving model updates
- [ ] **AutoML**: Automated model selection and tuning
- [ ] **Real-time Monitoring Dashboard**: Custom metrics visualization
- [ ] **Advanced MLOPs**: Feature store integration, data lineage tracking

## 🤝 Contributing

To contribute to this project:

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Make your changes and add tests
4. Run tests: `pytest tests/ -v`
5. Commit changes: `git commit -am 'Add your feature'`
6. Push to branch: `git push origin feature/your-feature`
7. Submit a pull request

### Code Style

This project follows PEP 8 guidelines. Format code with:

```bash
# Install formatting tools
pip install black flake8

# Format code
black src/ tests/

# Check style
flake8 src/ tests/
```

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙋 Support & Questions

For issues, questions, or suggestions:

1. **GitHub Issues**: Open an issue on the repository
2. **Pull Requests**: Submit PRs for bug fixes or features
3. **Documentation**: Refer to FastAPI and TensorFlow/Keras documentation

## 📎 Useful Resources

### Official Documentation
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [TensorFlow/Keras Guide](https://www.tensorflow.org/guide)
- [Docker Documentation](https://docs.docker.com/)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)

### MLOps Resources
- [MLOps.community](https://mlops.community/)
- [Made With ML](https://madewithml.com/)
- [Full Stack Deep Learning](https://fullstackdeeplearning.com/)

### Best Practices
- [Twelve-Factor App](https://12factor.net/)
- [Google Cloud AI Service Best Practices](https://cloud.google.com/ai-platform/docs/best-practices)
- [AWS ML Best Practices](https://docs.aws.amazon.com/sagemaker/latest/dg/best-practices.html)

## ✅ Checklist for Deployment

Before deploying to production:

- [ ] All tests passing locally
- [ ] Docker image builds successfully
- [ ] docker-compose up works without errors
- [ ] Health check endpoint responds correctly
- [ ] Prediction endpoint works with test images
- [ ] All environment variables documented in `.env.example`
- [ ] Model artifact included and accessible
- [ ] CI/CD pipeline configured in GitHub Actions
- [ ] README updated with accurate instructions
- [ ] Code reviewed for security and best practices
- [ ] Logging is structured and informative
- [ ] Error handling covers edge cases

---

**Created**: February 2026  
**Version**: 1.0.0  
**Status**: Production Ready ✅

For the latest updates, visit the [GitHub Repository](https://github.com/your-username/your-ml-api)
