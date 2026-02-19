# Quick Reference Guide

## 🚀 Getting Started (5 minutes)

### Start the API Locally

```bash
# Option 1: With Docker Compose (Recommended)
docker-compose up --build
# API at http://localhost:8000

# Option 2: Local Python
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn src.main:app --reload
```

## 📍 Important URLs

| Purpose | URL |
|---------|-----|
| API Base | http://localhost:8000 |
| Health Check | http://localhost:8000/health |
| API Docs (Swagger) | http://localhost:8000/docs |
| API Docs (ReDoc) | http://localhost:8000/redoc |
| OpenAPI Schema | http://localhost:8000/openapi.json |

## 🧪 Testing

```bash
# Run all tests
pytest tests/ -v

# Run specific test
pytest tests/test_api.py::test_health_check_endpoint -v

# Run with coverage
pytest tests/ --cov=src
```

## 📤 Making Predictions

### Using curl
```bash
curl -X POST http://localhost:8000/predict \
  -F "file=@image.png"
```

### Using Python
```python
import requests

with open("image.png", "rb") as f:
    response = requests.post(
        "http://localhost:8000/predict",
        files={"file": f}
    )
    
print(response.json())
# {"class_label": "cat", "probabilities": [...]}
```

## 🔧 Environment Variables

```bash
# Model path
MODEL_PATH=models/my_classifier_model.h5

# Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
LOG_LEVEL=INFO

# API configuration
API_PORT=8000
API_HOST=0.0.0.0
```

## 📁 Key Files

| File | Purpose |
|------|---------|
| `src/main.py` | FastAPI application |
| `src/model.py` | Model loading & preprocessing |
| `tests/test_api.py` | Unit tests |
| `Dockerfile` | Container image |
| `docker-compose.yml` | Local dev environment |
| `.github/workflows/main.yml` | CI/CD pipeline |
| `models/my_classifier_model.h5` | ML model |
| `README.md` | Full documentation |

## 🐳 Docker Commands

```bash
# Build image
docker build -t ml-api:latest .

# Run container
docker run -p 8000:8000 ml-api:latest

# Build with docker-compose
docker-compose build

# Start services
docker-compose up -d

# View logs
docker-compose logs -f ml_api

# Stop services
docker-compose down
```

## 🔍 Debugging

### Check health
```bash
curl http://localhost:8000/health
```

### View logs
```bash
# Docker Compose
docker-compose logs ml_api

# Direct container
docker logs <container-id>
```

### Check model
```bash
# Verify model exists
ls -la models/my_classifier_model.h5

# Check Python import
python -c "from src.model import load_model; print('Model loading works!')"
```

## 📊 CIFAR-10 Classes (Class Indices)

| 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 |
|---|---|---|---|---|---|---|---|---|---|
| airplane | automobile | bird | cat | deer | dog | frog | horse | ship | truck |

## 🚀 Deployment Quick Links

| Platform | Guide |
|----------|-------|
| AWS ECS | See DEPLOYMENT_GUIDE.md |
| Google Cloud Run | See DEPLOYMENT_GUIDE.md |
| Azure Container Instances | See DEPLOYMENT_GUIDE.md |
| Kubernetes | See DEPLOYMENT_GUIDE.md |
| Local Docker | `docker-compose up` |

## 📚 Documentation Files

- **README.md** - Full project documentation
- **API_DOCS.md** - API reference and examples
- **DEPLOYMENT_GUIDE.md** - Deployment instructions
- **PROJECT_COMPLETION.md** - Project summary
- **QUICK_REFERENCE.md** - This file

## ⚡ Common Tasks

### Update Model
```bash
# 1. Place new model in models/ directory
# 2. Set MODEL_PATH environment variable
# 3. Restart API
docker-compose down
docker-compose up --build
```

### Run Tests Locally
```bash
pytest tests/ -v --tb=short
```

### Check Code Quality
```bash
# Install tools
pip install black flake8

# Format code
black src/ tests/

# Check style
flake8 src/ tests/
```

### View CI/CD Status
1. Go to GitHub repository
2. Click "Actions" tab
3. View latest workflow run

## 🆘 Troubleshooting

| Issue | Solution |
|-------|----------|
| Model not found | Check `MODEL_PATH` env var, ensure file exists |
| Port already in use | Change port: `docker-compose up -p 9000:8000` |
| Tests failing | Run `pip install -r requirements.txt` first |
| Docker build fails | Run `docker-compose build --no-cache` |
| API not responding | Check logs: `docker-compose logs ml_api` |

## 📞 File Location Reference

```
your-ml-api/
├── API_DOCS.md              ← API documentation
├── DEPLOYMENT_GUIDE.md      ← Deployment instructions
├── Dockerfile               ← Docker build file
├── PROJECT_COMPLETION.md    ← Project summary
├── README.md                ← Main documentation
├── QUICK_REFERENCE.md       ← This file
├── docker-compose.yml       ← Local dev setup
├── models/                  ← ML model directory
│   └── my_classifier_model.h5
├── predictions/             ← Example predictions
├── src/                     ← Application code
│   ├── main.py                   (API endpoints)
│   └── model.py                  (Model logic)
└── tests/                   ← Unit tests
    └── test_api.py
```

## ✅ Verification Steps

```bash
# 1. Clone and enter directory
git clone <repo-url>
cd your-ml-api

# 2. Start API
docker-compose up --build

# 3. Test health check
curl http://localhost:8000/health

# 4. Run tests
docker-compose run ml_api pytest tests/ -v

# 5. Make prediction
curl -X POST http://localhost:8000/predict \
  -F "file=@models/test_image.png"
```

## 🎯 Performance Tips

- Use smaller images (32x32 recommended)
- Run multiple instances for load balancing
- Use GPU if available (update Dockerfile)
- Implement caching for repeated predictions
- Monitor resource usage regularly

## 📝 Version Information

| Component | Version |
|-----------|---------|
| Python | 3.9+ |
| FastAPI | 0.104.1 |
| Keras | 3.0+ |
| Docker | Latest |
| Docker Compose | 1.29+ |

---

**Need More Help?** Check README.md, API_DOCS.md, or DEPLOYMENT_GUIDE.md for comprehensive guides.

*Last Updated: February 2026*
