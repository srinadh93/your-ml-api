# Deployment Guide

This document provides detailed instructions for deploying the ML Prediction API to various environments.

## Table of Contents

1. [Local Development](#local-development)
2. [Docker Deployment](#docker-deployment)
3. [Cloud Deployment](#cloud-deployment)
   - [AWS](#aws)
   - [Google Cloud](#google-cloud)
   - [Azure](#azure)
4. [Kubernetes](#kubernetes)
5. [CI/CD Best Practices](#cicd-best-practices)

---

## Local Development

### Prerequisites

- Python 3.9+
- pip or poetry
- Git
- Virtual environment tool (venv)

### Setup Steps

```bash
# Clone the repository
git clone <repo-url>
cd your-ml-api

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Set environment variables
export MODEL_PATH=models/my_classifier_model.h5
export LOG_LEVEL=DEBUG

# Start the server
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

### Development Workflow

```bash
# Run tests
pytest tests/ -v

# Run with code coverage
pytest tests/ --cov=src --cov-report=html

# Format code
black src/ tests/

# Check code style
flake8 src/ tests/
```

---

## Docker Deployment

### Quick Start with Docker Compose

```bash
# Build and start
docker-compose up --build

# Run in background
docker-compose up -d

# Stop services
docker-compose down

# View logs
docker-compose logs -f ml_api

# Rebuild without cache
docker-compose build --no-cache
```

The API will be available at `http://localhost:8000`

### Standalone Docker

```bash
# Build image
docker build -t ml-api:latest .

# Run container
docker run -p 8000:8000 \
  -v $(pwd)/models:/app/models \
  -e MODEL_PATH=/app/models/my_classifier_model.h5 \
  -e LOG_LEVEL=INFO \
  ml-api:latest

# Run with custom environment variables
docker run -p 8000:8000 \
  -e MODEL_PATH=/app/models/custom_model.h5 \
  -e LOG_LEVEL=DEBUG \
  --name ml-api-container \
  ml-api:latest

# View logs
docker logs ml-api-container

# Stop container
docker stop ml-api-container
```

### Docker Image Optimization

To minimize image size:

```bash
# Check image size
docker images | grep ml-api

# Multi-stage build benefits:
# - Build stage: 800MB
# - Runtime stage: 200MB (only 25% of build size)

# To further reduce size, consider:
# - Using python:3.9-alpine (minimal Linux)
# - Removing test dependencies from production image
# - Using .dockerignore to exclude unnecessary files
```

---

## Cloud Deployment

### AWS Deployment

#### Option 1: Amazon ECS (Elastic Container Service)

**Prerequisites**: AWS CLI, ECR repository

```bash
# Build image for ECR
docker build -t ml-api:latest .

# Create ECR repository
aws ecr create-repository --repository-name ml-api --region us-east-1

# Get login credentials
aws ecr get-login-password --region us-east-1 | \
  docker login --username AWS --password-stdin \
  <account-id>.dkr.ecr.us-east-1.amazonaws.com

# Tag image
docker tag ml-api:latest \
  <account-id>.dkr.ecr.us-east-1.amazonaws.com/ml-api:latest

# Push image
docker push <account-id>.dkr.ecr.us-east-1.amazonaws.com/ml-api:latest

# Create ECS task definition (task-definition.json):
# {
#   "family": "ml-api-task",
#   "networkMode": "awsvpc",
#   "requiresCompatibilities": ["FARGATE"],
#   "cpu": "256",
#   "memory": "512",
#   "containerDefinitions": [
#     {
#       "name": "ml-api",
#       "image": "<account-id>.dkr.ecr.us-east-1.amazonaws.com/ml-api:latest",
#       "portMappings": [{"containerPort": 8000, "protocol": "tcp"}],
#       "environment": [
#         {"name": "MODEL_PATH", "value": "/app/models/my_classifier_model.h5"},
#         {"name": "LOG_LEVEL", "value": "INFO"}
#       ],
#       "logConfiguration": {
#         "logDriver": "awslogs",
#         "options": {
#           "awslogs-group": "/ecs/ml-api",
#           "awslogs-region": "us-east-1",
#           "awslogs-stream-prefix": "ecs"
#         }
#       }
#     }
#   ]
# }

# Register task definition
aws ecs register-task-definition \
  --cli-input-json file://task-definition.json \
  --region us-east-1

# Create ECS service
aws ecs create-service \
  --cluster ml-api-cluster \
  --service-name ml-api-service \
  --task-definition ml-api-task:1 \
  --desired-count 2 \
  --launch-type FARGATE \
  --network-configuration "awsvpcConfiguration={subnets=[subnet-xxx],securityGroups=[sg-xxx],assignPublicIp=ENABLED}" \
  --region us-east-1
```

#### Option 2: AWS Lambda with API Gateway

```bash
# Create Lambda function Docker image
docker build -t ml-api-lambda:latest \
  -f Dockerfile.lambda .

# Package for Lambda
zip -r lambda-deployment.zip src/ models/ requirements.txt

# Deploy via AWS CLI
aws lambda create-function \
  --function-name ml-api \
  --role arn:aws:iam::ACCOUNT_ID:role/lambda-role \
  --code S3Bucket=my-bucket,S3Key=lambda-deployment.zip \
  --handler src.main.app \
  --runtime python3.9 \
  --timeout 60 \
  --memory-size 1024 \
  --region us-east-1
```

### Google Cloud Deployment

#### Option 1: Cloud Run (Easiest)

```bash
# Authenticate
gcloud auth login

# Create artifact repository (optional)
gcloud artifacts repositories create ml-api \
  --repository-format=docker \
  --location=us-central1

# Build and push image
gcloud builds submit \
  --region=us-central1 \
  --tag=us-central1-docker.pkg.dev/PROJECT_ID/ml-api/ml-api:latest

# Deploy to Cloud Run
gcloud run deploy ml-api \
  --image=us-central1-docker.pkg.dev/PROJECT_ID/ml-api/ml-api:latest \
  --platform=managed \
  --region=us-central1 \
  --memory=512Mi \
  --cpu=1 \
  --allow-unauthenticated \
  --set-env-vars=MODEL_PATH=/app/models/my_classifier_model.h5,LOG_LEVEL=INFO
```

#### Option 2: Google Kubernetes Engine (GKE)

```bash
# Create GKE cluster
gcloud container clusters create ml-api-cluster \
  --num-nodes=3 \
  --machine-type=n1-standard-2 \
  --region=us-central1

# Get credentials
gcloud container clusters get-credentials ml-api-cluster --region=us-central1

# Build image and push to Artifact Registry
gcloud builds submit \
  --tag=us-central1-docker.pkg.dev/PROJECT_ID/ml-api/ml-api:latest

# Deploy to GKE using kubectl (see Kubernetes section below)
kubectl apply -f kubernetes-deployment.yaml
```

### Azure Deployment

#### Option 1: Azure Container Instances

```bash
# Login to Azure
az login

# Create resource group
az group create --name ml-api-rg --location eastus

# Create container registry
az acr create --resource-group ml-api-rg \
  --name mlapi --sku Basic

# Build and push image
az acr build --registry mlapi \
  --image ml-api:latest .

# Deploy to Azure Container Instances
az container create \
  --resource-group ml-api-rg \
  --name ml-api-container \
  --image mlapi.azurecr.io/ml-api:latest \
  --registry-login-server mlapi.azurecr.io \
  --registry-username <username> \
  --registry-password <password> \
  --environment-variables \
    MODEL_PATH=/app/models/my_classifier_model.h5 \
    LOG_LEVEL=INFO \
  --ports 8000 \
  --dns-name-label ml-api \
  --cpu 1 \
  --memory 1.5
```

#### Option 2: Azure App Service (Docker)

```bash
# Create App Service Plan
az appservice plan create \
  --name ml-api-plan \
  --resource-group ml-api-rg \
  --sku B1 \
  --is-linux

# Create Web App
az webapp create \
  --resource-group ml-api-rg \
  --plan ml-api-plan \
  --name ml-api-app \
  --deployment-container-image-name mlapi.azurecr.io/ml-api:latest

# Configure container
az webapp config container set \
  --name ml-api-app \
  --resource-group ml-api-rg \
  --docker-custom-image-name mlapi.azurecr.io/ml-api:latest \
  --docker-registry-server-url https://mlapi.azurecr.io \
  --docker-registry-server-user <username> \
  --docker-registry-server-password <password>

# Set environment variables
az webapp config appsettings set \
  --resource-group ml-api-rg \
  --name ml-api-app \
  --settings \
    MODEL_PATH=/app/models/my_classifier_model.h5 \
    LOG_LEVEL=INFO
```

---

## Kubernetes

### Deployment Manifest

Create `kubernetes-deployment.yaml`:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: ml-api-deployment
  namespace: default
  labels:
    app: ml-api
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
        image: ml-api:latest
        imagePullPolicy: IfNotPresent
        ports:
        - containerPort: 8000
          protocol: TCP
        env:
        - name: MODEL_PATH
          value: "/app/models/my_classifier_model.h5"
        - name: LOG_LEVEL
          value: "INFO"
        resources:
          requests:
            cpu: "250m"
            memory: "512Mi"
          limits:
            cpu: "1000m"
            memory: "1Gi"
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
          failureThreshold: 2
        volumeMounts:
        - name: models
          mountPath: /app/models
      volumes:
      - name: models
        configMap:
          name: model-config
          defaultMode: 0644
---
apiVersion: v1
kind: Service
metadata:
  name: ml-api-service
  namespace: default
spec:
  type: LoadBalancer
  selector:
    app: ml-api
  ports:
  - port: 80
    targetPort: 8000
    protocol: TCP
---
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: ml-api-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: ml-api-deployment
  minReplicas: 2
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

### Kubernetes Deployment Commands

```bash
# Create namespace
kubectl create namespace ml-api

# Create ConfigMap for model
kubectl create configmap model-config \
  --from-file=models/ \
  --namespace=ml-api

# Apply deployment
kubectl apply -f kubernetes-deployment.yaml --namespace=ml-api

# Check deployment status
kubectl get deployments --namespace=ml-api
kubectl get pods --namespace=ml-api

# View logs
kubectl logs -f deployment/ml-api-deployment --namespace=ml-api

# Scale deployment
kubectl scale deployment ml-api-deployment --replicas=5 --namespace=ml-api

# Update image
kubectl set image deployment/ml-api-deployment \
  ml-api=ml-api:v1.1.0 \
  --namespace=ml-api

# Delete deployment
kubectl delete deployment ml-api-deployment --namespace=ml-api
```

### Ingress Configuration

Create `kubernetes-ingress.yaml`:

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: ml-api-ingress
  namespace: ml-api
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /
spec:
  ingressClassName: nginx
  rules:
  - host: ml-api.example.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: ml-api-service
            port:
              number: 80
  tls:
  - hosts:
    - ml-api.example.com
    secretName: ml-api-tls
```

---

## CI/CD Best Practices

### GitHub Actions

The repository includes a GitHub Actions workflow that:

1. **Triggers on**:
   - Push to main branch
   - Pull requests to main branch

2. **Executes**:
   - Code checkout
   - Python environment setup
   - Dependency installation
   - Unit test execution
   - Docker image build
   - Artifact upload

3. **Check status**:
   - Go to repository → Actions tab
   - Click on workflow run to view details
   - Check commit badge for status

### Best Practices

```bash
# Commit messages for clear history
git commit -m "feat: add model caching for improved latency"
git commit -m "fix: handle corrupted image input gracefully"
git commit -m "perf: optimize preprocessing pipeline"

# Semantic versioning for releases
git tag -a v1.0.0 -m "First production release"
git push origin v1.0.0

# Branch protection rules
# - Require pull request reviews
# - Require status checks to pass
# - Require branches to be up to date
# - Dismiss stale pull request approvals
```

### Monitoring Deployments

```bash
# AWS CloudWatch
aws logs tail /ecs/ml-api --follow

# Google Cloud Logs
gcloud logging read "resource.type=cloud_run_revision" --limit 50

# Azure Monitor
az monitor metrics list --resource /subscriptions/xxxx/resourceGroups/ml-api-rg/providers/Microsoft.ContainerInstances/containerGroups/ml-api

# Kubernetes logs
kubectl logs -f deployment/ml-api-deployment --all-containers=true
```

---

## Troubleshooting Deployment

### Issue: Container fails to start

**Solution**:
```bash
# Check container logs
docker logs <container-id>

# Check if model file exists
docker exec <container-id> ls -la /app/models/

# Verify MODEL_PATH environment variable
docker exec <container-id> env | grep MODEL_PATH
```

### Issue: High memory usage

**Solution**:
- Reduce model size or quantize
- Scale horizontally (more containers, fewer replicas each)
- Implement request queuing
- Use model serving frameworks (TorchServe, KServe)

### Issue: Slow response time

**Solution**:
- Enable result caching
- Use GPU acceleration
- Optimize image preprocessing
- Load test and identify bottlenecks

---

## Performance Tuning

### For Production

```python
# In src/main.py, consider adding:

# 1. Request queuing
from fastapi_queue import FastAPIQueue
app = FastAPIQueue(app, )

# 2. Caching
from functools import lru_cache
@lru_cache(maxsize=1000)
def cached_prediction(image_hash):
    pass

# 3. Compression
from fastapi.middleware.gzip import GZIPMiddleware
app.add_middleware(GZIPMiddleware, minimum_size=1000)

# 4. CORS for cross-origin requests
from fastapi.middleware.cors import CORSMiddleware
app.add_middleware(CORSMiddleware, allow_origins=["*"])
```

---

## Rollback Procedures

```bash
# Docker Compose
docker-compose down
git checkout previous-version
docker-compose up --build

# Kubernetes
kubectl rollout history deployment/ml-api-deployment
kubectl rollout undo deployment/ml-api-deployment
kubectl rollout undo deployment/ml-api-deployment --to-revision=2

# AWS ECS
aws ecs update-service \
  --cluster ml-api-cluster \
  --service ml-api-service \
  --task-definition ml-api-task:1

# Google Cloud Run
gcloud run deploy ml-api \
  --image=us-central1-docker.pkg.dev/PROJECT_ID/ml-api/ml-api:previous-tag
```

---

## Security Checklist

- [ ] Use HTTPS/TLS in production
- [ ] Enable authentication/authorization
- [ ] Implement rate limiting
- [ ] Set up logging and monitoring
- [ ] Regular security updates
- [ ] Encrypt sensitive data
- [ ] Use secrets management
- [ ] Implement CORS restrictions
- [ ] Regular backup of models
- [ ] Disaster recovery plan

---

## Support

For deployment issues, check:
1. Application logs
2. Container/pod logs
3. CI/CD pipeline logs
4. Cloud provider dashboards
5. Network and firewall rules

---

**Last Updated**: February 2026
