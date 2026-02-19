# API Documentation

## FastAPI Automatic Documentation

When the API is running, you can access interactive API documentation at:

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`
- **OpenAPI Schema**: `http://localhost:8000/openapi.json`

These provide interactive interfaces to explore and test all endpoints.

## Endpoints Reference

### GET /health
**Purpose**: Health check endpoint for monitoring service status.

**Request**:
```bash
curl -X GET "http://localhost:8000/health"
```

**Response** (200 OK):
```json
{
  "status": "ok",
  "message": "API is healthy and model is loaded."
}
```

---

### POST /predict
**Purpose**: Classify an image using the pre-trained Keras model.

**Request**:
```bash
curl -X POST "http://localhost:8000/predict" \
  -F "file=@path/to/image.png"
```

**Request Parameters**:
- `file` (required, FormData): Image file to classify
  - Supported formats: PNG, JPEG, GIF, BMP, WebP, etc.
  - Maximum size: Limited by server memory
  - Content-Type: Must start with `image/`

**Response** (200 OK):
```json
{
  "class_label": "cat",
  "probabilities": [0.0, 0.0, 0.0, 0.92, 0.05, 0.01, 0.01, 0.01, 0.0, 0.0]
}
```

**Response Schema**:
| Field | Type | Description |
|-------|------|-------------|
| `class_label` | string | Predicted class name (e.g., "cat", "dog", "airplane") |
| `probabilities` | array[float] | Softmax probabilities for each class (10 values for CIFAR-10) |

**Error Responses**:

**400 Bad Request** - Invalid file type:
```json
{
  "detail": "Only image files (e.g., JPEG, PNG) are allowed for prediction."
}
```

**422 Unprocessable Entity** - Image processing error:
```json
{
  "detail": "Image processing failed: Error description"
}
```

**500 Internal Server Error** - Server error:
```json
{
  "detail": "An internal server error occurred during prediction: Error description"
}
```

---

## CIFAR-10 Classes

The model predicts one of the following 10 classes:

| Index | Class |
|-------|-------|
| 0 | airplane |
| 1 | automobile |
| 2 | bird |
| 3 | cat |
| 4 | deer |
| 5 | dog |
| 6 | frog |
| 7 | horse |
| 8 | ship |
| 9 | truck |

---

## Testing the API

### Using curl

```bash
# Health check
curl http://localhost:8000/health

# Image prediction
curl -X POST http://localhost:8000/predict \
  -F "file=@test_image.png"

# Multiple predictions
for img in images/*.png; do
  echo "Predicting $img..."
  curl -X POST http://localhost:8000/predict \
    -F "file=@$img"
done
```

### Using Python requests

```python
import requests

# Health check
response = requests.get("http://localhost:8000/health")
print(response.json())

# Image prediction
with open("test_image.png", "rb") as f:
    files = {"file": f}
    response = requests.post("http://localhost:8000/predict", files=files)
    print(response.json())
```

### Using Postman/Insomnia

1. Open Postman/Insomnia
2. Create a new POST request
3. Set URL: `http://localhost:8000/predict`
4. Go to Body tab, select `form-data`
5. Add key `file` with type `File`
6. Select your image file
7. Send the request

---

## Performance Optimization

### Latency Characteristics

- **Cold Start**: First request may take longer due to model loading (handled at startup)
- **Health Check**: ~1-2ms
- **Prediction**: 50-200ms depending on model and image size
- **Image Preprocessing**: ~10-50ms
- **Inference**: ~10-50ms

### Throughput

The API can handle multiple concurrent requests thanks to FastAPI's async capabilities. For production use:

- Single instance: ~5-20 requests/second
- Behind a load balancer: Depends on available resources

---

## Model Configuration

### Image Input Shape

- **Height**: 32 pixels
- **Width**: 32 pixels
- **Channels**: 3 (RGB)
- **Format**: Floating point arrays normalized to [0, 1]

### Preprocessing Pipeline

1. Load image from bytes
2. Convert to RGB (if needed)
3. Resize to 32x32
4. Normalize pixel values: `pixel_value / 255.0`
5. Add batch dimension: `(1, 32, 32, 3)`
6. Pass to model for inference

---

## Advanced Usage

### Batch Processing

To process multiple images at once, send multiple requests to the `/predict` endpoint:

```python
from concurrent.futures import ThreadPoolExecutor
import requests

images = ["img1.png", "img2.png", "img3.png"]

def predict_image(image_path):
    with open(image_path, "rb") as f:
        response = requests.post(
            "http://localhost:8000/predict",
            files={"file": f}
        )
    return response.json()

with ThreadPoolExecutor(max_workers=5) as executor:
    results = list(executor.map(predict_image, images))

for img, result in zip(images, results):
    print(f"{img}: {result['class_label']}")
```

### Custom Model Loading

To use a different trained model:

1. Save it as an HDF5 file (`.h5` format)
2. Place it in the `models/` directory
3. Set the path in the environment variable:
   ```bash
   export MODEL_PATH="/path/to/your/model.h5"
   ```
4. Restart the API service

---

## Monitoring & Logging

The API includes structured logging for:

- Application startup
- Model loading events
- API requests and responses
- Prediction results
- Error events with stack traces

### Log Levels

Control logging verbosity with the `LOG_LEVEL` environment variable:

```bash
LOG_LEVEL=DEBUG    # Most verbose
LOG_LEVEL=INFO     # Typical production level
LOG_LEVEL=WARNING  # Only warnings and errors
LOG_LEVEL=ERROR    # Only errors
```

### Example Log Output

```
2024-01-15 10:45:31 - src.model - INFO - ML Model loaded successfully and ready for inference.
2024-01-15 10:45:32 - src.main - INFO - Prediction successful for test_image.png: cat
2024-01-15 10:45:35 - src.main - ERROR - Data preprocessing error for corrupted.png: Error processing image
```

---

## Troubleshooting

### Issue: Model not found error

**Error**: `FileNotFoundError: Model file not found at models/my_classifier_model.h5`

**Solution**:
1. Ensure model file exists in `models/` directory
2. Check file permissions
3. Verify `MODEL_PATH` environment variable is correct
4. Rebuild Docker image: `docker-compose build --no-cache`

### Issue: Request timeout

**Error**: Connection timeout when sending large images

**Solution**:
1. Reduce image size before sending
2. Increase timeout in client: `requests.post(..., timeout=60)`
3. Scale API instances behind a load balancer

### Issue: GPU out of memory

**Error**: CUDA out of memory error during inference

**Solution**:
1. Reduce batch size
2. Use lighter model version
3. Enable GPU memory growth in TensorFlow
4. Add more GPU memory if available

---

## Security Recommendations

### For Production Deployment

1. **Enable HTTPS/TLS**: Use a reverse proxy (nginx) with certificates
2. **Add Authentication**: Implement API key or OAuth2
3. **Rate Limiting**: Prevent abuse with request throttling
4. **Input Validation**: Already implemented (file type checking)
5. **CORS Configuration**: Restrict origins if needed
6. **Logging Secrets**: Never log sensitive data
7. **Model Security**: Version control model artifacts
8. **Dependency Updates**: Regularly update security patches

### Example CORS Configuration

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://yourdomain.com"],
    allow_credentials=True,
    allow_methods=["POST", "GET"],
    allow_headers=["*"],
)
```

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | Feb 2026 | Initial release with CIFAR-10 support |

---

## Support & Feedback

For issues or questions:
- Check the main [README.md](README.md) for setup instructions
- Review GitHub Actions logs for CI/CD pipeline status
- Check application logs for debugging information

---

**Last Updated**: February 2026  
**API Version**: 1.0.0
