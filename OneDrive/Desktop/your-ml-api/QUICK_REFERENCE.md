# Quick Reference - ML Prediction API

Quick command reference for common tasks.

## Installation & Setup

```bash
# Clone repository
git clone https://github.com/srinadh93/your-ml-api.git && cd your-ml-api

# Create virtual environment
python -m venv .venv && source .venv/bin/activate  # Linux/macOS
python -m venv .venv && .\.venv\Scripts\Activate.ps1  # Windows

# Install dependencies
pip install -r requirements.txt
```

## Running the API

```bash
# Local development
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000

# With Docker
docker-compose up --build

# Production (Gunicorn)
gunicorn src.main:app --workers 4 --bind 0.0.0.0:8000
```

## Testing

```bash
# Run all tests
pytest tests/test_api.py -v

# Run specific test
pytest tests/test_api.py::test_health_check_endpoint -v

# Run with coverage
pytest tests/test_api.py --cov=src --cov-report=html
```

## Docker Commands

```bash
# Build image
docker build -t ml-api:latest .

# Run container
docker run -p 8000:8000 -v $(pwd)/models:/app/models ml-api:latest

# View logs
docker logs -f container_id

# Stop container
docker stop container_id

# Remove image
docker rmi ml-api:latest
```

## Docker Compose

```bash
# Start services
docker-compose up

# Start in background
docker-compose up -d

# Stop services
docker-compose down

# View logs
docker-compose logs -f

# Rebuild images
docker-compose up --build

# Remove volumes
docker-compose down -v
```

## API Requests

```bash
# Health check
curl http://localhost:8000/health

# Predict image
curl -X POST http://localhost:8000/predict \
  -F "file=@image.png"

# View API docs
# Browser: http://localhost:8000/docs
```

## Git Commands

```bash
# Clone repo
git clone https://github.com/srinadh93/your-ml-api.git

# Check status
git status

# Add all changes
git add .

# Commit changes
git commit -m "Your message"

# Push to GitHub
git push origin main

# Pull latest
git pull origin main
```

## Useful URLs

- API: http://localhost:8000
- Swagger Docs: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
- OpenAPI JSON: http://localhost:8000/openapi.json

## Environment Variables

```bash
# Create .env file
cp .env.example .env

# Edit .env with your settings
DEBUG=false
LOG_LEVEL=INFO
MODEL_PATH=models/my_classifier_model.h5
```

## Common Issues

| Issue | Solution |
|-------|----------|
| Port 8000 already in use | Use different port: `--port 8001` |
| Model not found | Check `models/` directory |
| Import errors | Run `pip install -r requirements.txt` |
| Docker build fails | Clear cache: `docker builder prune` |
| Tests failing | Check model file exists |

## File Locations

```
your-ml-api/
├── src/main.py           # API endpoints
├── src/model.py          # Model inference
├── tests/test_api.py     # Unit tests
├── models/               # Model artifacts
├── Dockerfile            # Container image
├── docker-compose.yml    # Container orchestration
└── requirements.txt      # Python dependencies
```

## Performance Tips

- Use GPU for faster inference: `docker run --gpus all ...`
- Scale horizontally: `docker-compose up -d --scale ml-api=3`
- Monitor memory: `docker stats`
- Profile endpoints: Check logs for latency

## Documentation

- [README.md](README.md) - Full project overview
- [API_DOCS.md](API_DOCS.md) - API reference
- [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) - Production setup
- [00_START_HERE.md](00_START_HERE.md) - Getting started

---

**Version**: 1.0.0  
**Last Updated**: 2024-01-15
