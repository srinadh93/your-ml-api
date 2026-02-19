# API Documentation - ML Prediction API

Complete API reference with examples for the ML Prediction API.

## Base URL

```
http://localhost:8000
```

## Authentication

Currently, the API does not require authentication. For production, implement API keys or OAuth2.

---

## Endpoints

### 1. GET /health

**Description**: Health check endpoint for monitoring API and model status

**Method**: `GET`

**URL**: `/health`

**Parameters**: None

**Response Code**: `200 OK`

**Response Body**:
```json
{
  "status": "healthy",
  "model_loaded": true,
  "version": "1.0.0"
}
```

**Example Request**:
```bash
curl -X GET "http://localhost:8000/health" \
  -H "accept: application/json"
```

**Example Response**:
```json
{
  "status": "healthy",
  "model_loaded": true,
  "version": "1.0.0"
}
```

**Status Values**:
- `healthy`: API and model are fully operational
- `degraded`: API running but model not loaded

---

### 2. POST /predict

**Description**: Make predictions on uploaded image files

**Method**: `POST`

**URL**: `/predict`

**Content-Type**: `multipart/form-data`

**Parameters**:
- `file` (required, multipart file): Image file to classify
  - **Allowed formats**: PNG, JPEG, JPG, GIF, BMP
  - **Max size**: 50MB (configurable)

**Response Code**: 
- `200 OK` - Prediction successful
- `400 Bad Request` - Invalid file or format
- `500 Internal Server Error` - Processing error

**Response Body**:
```json
{
  "class_label": "cat",
  "probabilities": [0.05, 0.85, 0.08, 0.02, ...],
  "confidence": 0.85,
  "timestamp": "2024-01-15T10:30:45.123456"
}
```

**Example Request (curl)**:
```bash
curl -X POST "http://localhost:8000/predict" \
  -H "accept: application/json" \
  -F "file=@image.png"
```

**Example Request (Python)**:
```python
import requests

with open('image.png', 'rb') as f:
    response = requests.post(
        'http://localhost:8000/predict',
        files={'file': f}
    )
    print(response.json())
```

**Example Request (JavaScript)**:
```javascript
const formData = new FormData();
formData.append('file', fileInput.files[0]);

fetch('http://localhost:8000/predict', {
  method: 'POST',
  body: formData
})
.then(res => res.json())
.then(data => console.log(data));
```

**Example Response**:
```json
{
  "class_label": "cat",
  "probabilities": [
    0.02, 0.05, 0.01, 0.85, 0.03,
    0.02, 0.01, 0.00, 0.00, 0.01
  ],
  "confidence": 0.85,
  "timestamp": "2024-01-15T10:30:45.123456"
}
```

**Response Fields**:
- `class_label` (string): Predicted class name (one of 10 CIFAR-10 classes)
- `probabilities` (array): Confidence scores for each class [0-1]
- `confidence` (float): Confidence of predicted class [0-1]
- `timestamp` (string): ISO 8601 timestamp of prediction

**Error Responses**:

**400 - Missing File**:
```json
{
  "detail": "No file uploaded"
}
```

**400 - Invalid File Type**:
```json
{
  "detail": "Invalid file type. Allowed: .png, .jpg, .jpeg, .gif, .bmp"
}
```

**400 - Empty File**:
```json
{
  "detail": "Invalid image: Empty file"
}
```

**400 - Corrupted Image**:
```json
{
  "detail": "Invalid image: Cannot identify image file"
}
```

**500 - Prediction Error**:
```json
{
  "detail": "Prediction failed: Model error"
}
```

---

### 3. GET /docs

**Description**: Interactive API documentation (Swagger UI)

**Method**: `GET`

**URL**: `/docs`

**Response**: HTML with interactive API explorer

---

### 4. GET /openapi.json

**Description**: OpenAPI schema in JSON format

**Method**: `GET`

**URL**: `/openapi.json`

**Response**: Complete OpenAPI specification

---

## CIFAR-10 Classes

The model predicts one of these 10 classes:

| Index | Class | Index | Class |
|-------|-------|-------|-------|
| 0 | airplane | 5 | dog |
| 1 | automobile | 6 | frog |
| 2 | bird | 7 | horse |
| 3 | cat | 8 | ship |
| 4 | deer | 9 | truck |

---

## Example Usage Scenarios

### Scenario 1: Health Monitoring

```bash
# Check API health
curl http://localhost:8000/health

# Output
{
  "status": "healthy",
  "model_loaded": true,
  "version": "1.0.0"
}
```

### Scenario 2: Predict Image Class

```bash
# Predict class of image
curl -X POST http://localhost:8000/predict \
  -F "file=@cat.png"

# Output
{
  "class_label": "cat",
  "probabilities": [0.01, 0.02, 0.00, 0.95, 0.01, 0.00, 0.00, 0.00, 0.00, 0.01],
  "confidence": 0.95,
  "timestamp": "2024-01-15T10:35:20.456789"
}
```

### Scenario 3: Batch Processing

```python
import requests
import glob

# Process all PNG files in directory
for image_path in glob.glob('images/*.png'):
    with open(image_path, 'rb') as f:
        response = requests.post(
            'http://localhost:8000/predict',
            files={'file': f}
        )
        
        if response.status_code == 200:
            prediction = response.json()
            print(f"{image_path}: {prediction['class_label']} ({prediction['confidence']:.1%})")
        else:
            print(f"{image_path}: Error - {response.status_code}")
```

---

## Rate Limiting

Currently not implemented. For production, add:
- Per-IP rate limiting
- Per-API-key quotas
- Burst protection

---

## Versioning

Current API version: `1.0.0`

Breaking changes will increment major version (2.0.0, 3.0.0, etc.)

---

## Common Response Codes

| Code | Meaning |
|------|---------|
| 200 | Request successful |
| 400 | Bad request (invalid parameters) |
| 422 | Validation error |
| 500 | Server error |
| 503 | Service unavailable |

---

## Testing the API

### Using Swagger UI

1. Run API: `uvicorn src.main:app --reload`
2. Open: http://localhost:8000/docs
3. Click "Try it out" on endpoints
4. Enter parameters and execute

### Using curl

```bash
# Get health
curl http://localhost:8000/health

# Make prediction
curl -X POST http://localhost:8000/predict \
  -F "file=@image.png"
```

### Using Python requests

```python
import requests

# Health check
response = requests.get('http://localhost:8000/health')
print(response.json())

# Make prediction
with open('image.png', 'rb') as f:
    response = requests.post(
        'http://localhost:8000/predict',
        files={'file': f}
    )
    print(response.json())
```

---

## Performance Metrics

- **Latency**: 50-100ms per prediction (CPU)
- **Throughput**: 10-20 predictions/second (single instance)
- **Memory**: ~200MB per instance
- **Model size**: 1.06 MB

---

## Troubleshooting

### Model Not Loaded

**Error**: `"model_loaded": false`

**Solution**: 
- Check model file exists at `models/my_classifier_model.h5`
- Check logs for loading errors
- Restart API server

### File Upload Fails

**Error**: `413 Payload Too Large`

**Solution**: 
- Reduce image file size
- Configure `client_max_body_size` in server

### Slow Predictions

**Causes**: 
- CPU-only inference (use GPU for speed)
- Large image size
- Server under load

**Solution**: 
- Use GPU docker image
- Deploy multiple instances
- Use load balancer

---

For more information, see [README.md](README.md) and [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md).
