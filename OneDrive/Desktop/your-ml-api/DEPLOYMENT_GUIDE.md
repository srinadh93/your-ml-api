# Deployment Guide - ML Prediction API

Complete guide for deploying the ML Prediction API to production environments.

## Table of Contents

1. [Local Development](#local-development)
2. [Docker Deployment](#docker-deployment)
3. [Production Setup](#production-setup)
4. [Monitoring & Logging](#monitoring--logging)
5. [Scaling](#scaling)
6. [Troubleshooting](#troubleshooting)

---

## Local Development

### Prerequisites

- Python 3.9+
- pip
- Virtual environment tool

### Setup Steps

```bash
# 1. Clone repository
git clone https://github.com/srinadh93/your-ml-api.git
cd your-ml-api

# 2. Create virtual environment
python -m venv .venv

# 3. Activate environment
# On Linux/macOS:
source .venv/bin/activate

# On Windows (PowerShell):
.\.venv\Scripts\Activate.ps1

# On Windows (Command Prompt):
.venv\Scripts\activate.bat

# 4. Install dependencies
pip install -r requirements.txt

# 5. Run API server
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000

# 6. Access API
# Open: http://localhost:8000/docs
```

### Environment Variables (Local)

Create `.env` file:
```env
DEBUG=true
LOG_LEVEL=DEBUG
MODEL_PATH=models/my_classifier_model.h5
```

---

## Docker Deployment

### Prerequisites

- Docker 20.10+
- Docker Compose 2.0+ (for compose deployment)

### Quick Start

```bash
# Build and run with Docker Compose
docker-compose up --build

# API available at http://localhost:8000
```

### Manual Docker Build

```bash
# Build image
docker build -t ml-api:latest .

# Run container
docker run -p 8000:8000 \
  -v $(pwd)/models:/app/models \
  -e LOG_LEVEL=INFO \
  ml-api:latest

# API available at http://localhost:8000
```

### Docker Compose Configuration

See `docker-compose.yml` for:
- Service definitions
- Volume mounts
- Port mapping
- Environment variables
- Health checks
- Restart policies

---

## Production Setup

### 1. Infrastructure

#### Recommended Setup
- **Container Orchestration**: Kubernetes or Docker Swarm
- **Load Balancer**: Nginx, HAProxy, or cloud provider LB
- **Data Store**: Mount NFS or cloud storage for models
- **Monitoring**: Prometheus + Grafana
- **Logging**: ELK Stack or cloud logging

#### Minimal Production Setup

```yaml
# docker-compose.prod.yml
version: '3.8'
services:
  ml-api:
    image: ml-api:1.0.0
    replicas: 3
    resources:
      limits:
        cpus: '2'
        memory: 1G
      reservations:
        cpus: '1'
        memory: 512M
    environment:
      LOG_LEVEL: INFO
      DEBUG: "false"
    volumes:
      - models-volume:/app/models
      - logs-volume:/app/logs
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
    restart: unless-stopped
    
  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./ssl:/etc/nginx/ssl
    depends_on:
      - ml-api
    restart: unless-stopped

volumes:
  models-volume:
    driver: local
  logs-volume:
    driver: local
```

### 2. Kubernetes Deployment

#### Deployment Manifest

```yaml
# k8s-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: ml-api
  namespace: production
spec:
  replicas: 3
  selector:
    matchLabels:
      app: ml-api
  template:
    metadata:
      labels:
        app: ml-api
        version: "1.0.0"
    spec:
      containers:
      - name: ml-api
        image: your-registry/ml-api:1.0.0
        ports:
        - containerPort: 8000
        env:
        - name: LOG_LEVEL
          value: "INFO"
        - name: DEBUG
          value: "false"
        resources:
          limits:
            cpu: 2000m
            memory: 1Gi
          requests:
            cpu: 1000m
            memory: 512Mi
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 10
          timeoutSeconds: 5
          failureThreshold: 3
        readinessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 10
          periodSeconds: 5
          timeoutSeconds: 3
          failureThreshold: 3
        volumeMounts:
        - name: models
          mountPath: /app/models
          readOnly: true
        - name: logs
          mountPath: /app/logs
      volumes:
      - name: models
        persistentVolumeClaim:
          claimName: ml-models-pvc
      - name: logs
        emptyDir: {}
---
apiVersion: v1
kind: Service
metadata:
  name: ml-api-service
  namespace: production
spec:
  selector:
    app: ml-api
  ports:
  - protocol: TCP
    port: 80
    targetPort: 8000
  type: LoadBalancer
```

#### Deploy to Kubernetes

```bash
# Create namespace
kubectl create namespace production

# Create persistent volume for models
kubectl apply -f k8s-pv.yaml

# Deploy application
kubectl apply -f k8s-deployment.yaml

# Check deployment
kubectl get pods -n production
kubectl logs -f deployment/ml-api -n production

# Access service
kubectl port-forward service/ml-api-service 8000:80 -n production
```

### 3. Cloud Platform Deployments

#### AWS ECS

```bash
# Create ECR repository
aws ecr create-repository --repository-name ml-api

# Build and push image
docker build -t ml-api:latest .
docker tag ml-api:latest YOUR_ACCOUNT.dkr.ecr.YOUR_REGION.amazonaws.com/ml-api:latest
docker push YOUR_ACCOUNT.dkr.ecr.YOUR_REGION.amazonaws.com/ml-api:latest

# Create ECS task definition from template
aws ecs register-task-definition --cli-input-json file://task-definition.json

# Create ECS service
aws ecs create-service --cluster production --service-name ml-api --task-definition ml-api:1 --desired-count 3
```

#### Google Cloud Run

```bash
# Build image
gcloud builds submit --tag gcr.io/YOUR_PROJECT/ml-api .

# Deploy to Cloud Run
gcloud run deploy ml-api \
  --image gcr.io/YOUR_PROJECT/ml-api \
  --platform managed \
  --region us-central1 \
  --memory 1Gi \
  --cpu 2 \
  --allow-unauthenticated
```

#### Azure Container Instances

```bash
# Build and push image
az acr build --registry YOUR_REGISTRY --image ml-api:latest .

# Deploy container
az container create \
  --resource-group myResourceGroup \
  --name ml-api \
  --image YOUR_REGISTRY.azurecr.io/ml-api:latest \
  --cpu 2 \
  --memory 1 \
  --ports 8000 \
  --registry-username YOUR_USERNAME \
  --registry-password YOUR_PASSWORD
```

---

## Monitoring & Logging

### Prometheus Metrics

Add to `src/main.py`:

```python
from prometheus_client import Counter, Histogram
import time

request_count = Counter('api_requests_total', 'Total requests')
request_duration = Histogram('api_request_duration_seconds', 'Request duration')

@app.middleware("http")
async def add_metrics(request, call_next):
    request_count.inc()
    start = time.time()
    response = await call_next(request)
    request_duration.observe(time.time() - start)
    return response
```

### Structured Logging

Logging configuration in `src/main.py`:

```python
import json_logging
import logging

json_logging.init_non_web(enable_json=True)
logger = logging.getLogger(__name__)

# Structured log
logger.info("Prediction completed", extra={
    "class_label": "cat",
    "confidence": 0.95,
    "latency_ms": 75
})
```

### Log Aggregation (ELK Stack)

```yaml
# docker-compose-elk.yml
version: '3.8'
services:
  elasticsearch:
    image: docker.elastic.co/elasticsearch/elasticsearch:7.17.0
    environment:
      - discovery.type=single-node
    ports:
      - "9200:9200"
    volumes:
      - elasticsearch-data:/usr/share/elasticsearch/data

  kibana:
    image: docker.elastic.co/kibana/kibana:7.17.0
    ports:
      - "5601:5601"
    depends_on:
      - elasticsearch

  ml-api:
    build: .
    ports:
      - "8000:8000"
    environment:
      LOG_LEVEL: INFO
    logging:
      driver: json-file
      options:
        max-size: "10m"
        max-file: "3"

volumes:
  elasticsearch-data:
```

---

## Scaling

### Horizontal Scaling

```bash
# Docker Compose with multiple instances
docker-compose up -d --scale ml-api=3
```

### Load Balancing with Nginx

```nginx
# nginx.conf
upstream ml-api {
    least_conn;
    server ml-api-1:8000;
    server ml-api-2:8000;
    server ml-api-3:8000;
}

server {
    listen 80;
    
    location /health {
        access_log off;
        proxy_pass http://ml-api;
    }
    
    location / {
        proxy_pass http://ml-api;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_buffering off;
    }
}
```

### Kubernetes Horizontal Pod Autoscaler

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: ml-api-hpa
  namespace: production
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: ml-api
  minReplicas: 3
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 80
```

---

## Security Considerations

### Environment Variables

Never commit sensitive data:
```bash
# .env (local only, add to .gitignore)
API_KEY=secret-key-here
DATABASE_PASSWORD=password
```

### SSL/TLS Configuration

```nginx
server {
    listen 443 ssl;
    ssl_certificate /etc/ssl/certs/certificate.crt;
    ssl_certificate_key /etc/ssl/private/key.key;
    
    location / {
        proxy_pass http://ml-api;
    }
}
```

### Rate Limiting

```nginx
limit_req_zone $binary_remote_addr zone=api_limit:10m rate=10r/s;

server {
    location /predict {
        limit_req zone=api_limit burst=20 nodelay;
        proxy_pass http://ml-api;
    }
}
```

---

## Troubleshooting

### Container won't start

```bash
# Check logs
docker logs container_name

# Inspect image
docker inspect container_name

# Run with verbose output
docker run -it ml-api:latest bash
```

### Model not loading

```bash
# Verify model file
docker exec container_name ls -lah /app/models/

# Check file permissions
docker exec container_name chmod 644 /app/models/*.h5
```

### High latency

- Check CPU/memory usage
- Monitor network bandwidth
- Profile model inference time
- Consider GPU acceleration

### Out of memory

```bash
# Increase container memory limit
docker update --memory 2g container_name

# Monitor memory
docker stats container_name
```

---

## Performance Tuning

### Gunicorn Configuration

```bash
gunicorn src.main:app \
  --workers 4 \
  --worker-class uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:8000 \
  --access-logfile - \
  --error-logfile - \
  --log-level info
```

### Model Optimization

- Use ONNX for faster inference
- Quantize model to reduce size
- Use GPU acceleration (CUDA)
- Cache predictions when possible

---

For more information, see [README.md](README.md) and [API_DOCS.md](API_DOCS.md).
