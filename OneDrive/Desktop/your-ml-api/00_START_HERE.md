# 00 - START HERE

Welcome to the ML Prediction API! This guide will get you started in 5 minutes.

## 🚀 Quick Start (5 minutes)

### Option 1: Local Python (Recommended for development)

```bash
# 1. Install Python dependencies
pip install -r requirements.txt

# 2. Start the API server
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000

# 3. Open in browser
# Visit: http://localhost:8000/docs
```

### Option 2: Docker (Recommended for deployment)

```bash
# 1. Build and run with Docker Compose
docker-compose up --build

# 2. Open in browser
# Visit: http://localhost:8000/docs
```

## ✅ Verify It's Working

```bash
# Test health endpoint
curl http://localhost:8000/health

# Expected response:
# {"status":"healthy","model_loaded":true,"version":"1.0.0"}
```

## 📸 Make Your First Prediction

```bash
# Test with a sample image
curl -X POST http://localhost:8000/predict \
  -F "file=@predictions/example_cat_prediction.json"

# Or use the web interface:
# 1. Go to http://localhost:8000/docs
# 2. Click on "POST /predict"
# 3. Click "Try it out"
# 4. Upload an image
# 5. Click "Execute"
```

## 📁 Project Structure

```
your-ml-api/
├── src/                          # Application source code
│   ├── main.py                  # FastAPI endpoints
│   └── model.py                 # Model inference logic
├── tests/                        # Test suite
│   └── test_api.py              # Unit tests (7 tests)
├── models/                       # ML model artifacts
│   └── my_classifier_model.h5   # Keras model file
├── predictions/                  # Example predictions
│   └── example_*.json           # Sample outputs
└── [config files & docs]
```

## 📚 Documentation

| Document | Purpose |
|----------|---------|
| [README.md](README.md) | Full project overview & features |
| [API_DOCS.md](API_DOCS.md) | Complete API reference with examples |
| [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) | Production deployment instructions |
| [QUICK_REFERENCE.md](QUICK_REFERENCE.md) | Common commands & quick reference |

## 🧪 Run Tests

```bash
# Run all 7 tests (should all pass ✓)
pytest tests/test_api.py -v

# Expected: 7 passed
```

## 🔧 Available Endpoints

### GET /health
Check if API and model are ready
```bash
curl http://localhost:8000/health
```

### POST /predict
Predict image class
```bash
curl -X POST http://localhost:8000/predict \
  -F "file=@your_image.png"
```

### GET /docs
Interactive API documentation (Swagger UI)
```
http://localhost:8000/docs
```

## 🎯 What Can It Do?

- Classifies CIFAR-10 image categories:
  - airplane, automobile, bird, cat, deer
  - dog, frog, horse, ship, truck
- Returns class predictions with confidence scores
- Fast inference (~50-100ms per image)
- RESTful API with automatic documentation

## 🛑 Troubleshooting

| Problem | Solution |
|---------|----------|
| **Port 8000 already in use** | Use different port: `--port 8001` |
| **ModuleNotFoundError** | Install dependencies: `pip install -r requirements.txt` |
| **Model not found** | Check `models/my_classifier_model.h5` exists |
| **Connection refused** | Make sure server is running |

## 🐳 Docker Quick Commands

```bash
# Start with Docker
docker-compose up --build

# Stop Docker
docker-compose down

# View logs
docker-compose logs -f

# Build image manually
docker build -t ml-api:latest .

# Run from image
docker run -p 8000:8000 ml-api:latest
```

## 📊 API Response Example

```json
{
  "class_label": "cat",
  "probabilities": [0.02, 0.05, 0.01, 0.85, 0.03, 0.02, 0.01, 0.00, 0.00, 0.01],
  "confidence": 0.85,
  "timestamp": "2024-01-15T10:30:45.123456"
}
```

## 🔌 API Details

- **Framework**: FastAPI (modern, fast, automatic docs)
- **Model**: Keras/TensorFlow (CIFAR-10 classifier)
- **Input**: Image files (PNG, JPG, GIF, BMP)
- **Output**: JSON with predictions & confidence
- **Speed**: ~50-100ms per prediction

## 🚀 Next Steps

1. ✅ Get API running (you just did this!)
2. 📊 Make predictions with `/predict` endpoint
3. 📖 Read [API_DOCS.md](API_DOCS.md) for full reference
4. 🧪 Run tests to verify everything works
5. 🐳 Try Docker deployment
6. 🌐 Deploy to production (see [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md))

## 💡 Pro Tips

- Use **Swagger UI** at `/docs` for interactive testing
- Check **health endpoint** before making predictions
- Look at `predictions/` folder for example outputs
- Run **tests** to verify installation: `pytest tests/test_api.py -v`

## 📞 Need Help?

1. Check example predictions: `predictions/example_*.json`
2. Review test cases: `tests/test_api.py`
3. Read API docs: [API_DOCS.md](API_DOCS.md)
4. See deployment guide: [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)

## ✨ Features Summary

- ✅ Production-ready REST API
- ✅ Automatic API documentation
- ✅ Comprehensive test suite (7/7 passing)
- ✅ Docker containerization
- ✅ CI/CD pipeline (GitHub Actions)
- ✅ Error handling & logging
- ✅ Multiple output formats
- ✅ Health monitoring

---

**Ready to get started?** 

```bash
uvicorn src.main:app --reload
```

Then visit: http://localhost:8000/docs

**Questions?** Check [README.md](README.md) or [API_DOCS.md](API_DOCS.md)

**Version**: 1.0.0  
**Status**: Production Ready ✅
