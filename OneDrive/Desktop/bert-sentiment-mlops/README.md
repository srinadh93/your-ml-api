# BERT Sentiment MLOps Project

A complete, production-ready sentiment analysis system using BERT (specifically DistilBERT for efficiency). This project demonstrates a full MLOps pipeline: data preprocessing, model fine-tuning, REST API serving, and a web interface—all containerized and orchestrated with Docker.

## Table of Contents
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Project Structure](#project-structure)
- [Quick Start](#quick-start)
- [API Documentation](#api-documentation)
- [Scripts](#scripts)
- [Docker & Deployment](#docker--deployment)
- [Configuration](#configuration)
- [Troubleshooting](#troubleshooting)

## Features
- ✅ **Data Preprocessing**: Automatic IMDB dataset download and cleaning
- ✅ **Model Fine-Tuning**: Transfer learning with DistilBERT on sentiment classification
- ✅ **REST API**: FastAPI with `/health` check and `/predict` endpoint
- ✅ **Web UI**: Streamlit interface for interactive predictions
- ✅ **Batch Prediction**: Process multiple texts from CSV files
- ✅ **Metrics & Tracking**: Automatic evaluation (accuracy, precision, recall, F1-score)
- ✅ **Containerization**: Docker Compose setup for reproducible deployment
- ✅ **Error Handling**: Graceful fallback to pre-trained model when local model unavailable

## Prerequisites
- **Python 3.8+** (for local development)
- **Docker & Docker Compose** (for containerized deployment)
- **Git** (for version control)
- **4GB+ RAM** (for model training and inference)

## Project Structure
```
bert-sentiment-mlops/
├── README.md                  # Project documentation
├── requirements.txt           # Python dependencies
├── .env.example              # Environment variables template
├── .gitignore                # Git ignore patterns
├── docker-compose.yml        # Container orchestration
├── Dockerfile.api            # API service container
├── Dockerfile.ui             # UI service container
│
├── scripts/                  # Runnable scripts
│   ├── preprocess.py         # Data preprocessing & cleaning
│   ├── train.py              # Model fine-tuning
│   └── batch_predict.py      # Batch prediction on CSV
│
├── src/                      # Application code
│   ├── api.py                # FastAPI application
│   └── ui.py                 # Streamlit web interface
│
└── data/                     # Data directories
    ├── processed/            # Train/test CSV files
    └── unseen/               # Input data for predictions
├── model_output/             # Fine-tuned model artifacts
└── results/                  # Evaluation metrics & summaries
```

## Quick Start

### Option 1: Local Development (Python + Docker)

1. **Clone the repository:**
```bash
git clone https://github.com/srinadh93/bert-sentiment-mlops.git
cd bert-sentiment-mlops
```

2. **Set up Python environment:**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3. **Preprocess data (downloads IMDB dataset):**
```bash
python scripts/preprocess.py --max-samples 5000
```

4. **Train the model:**
```bash
python scripts/train.py --model-name distilbert-base-uncased --epochs 1
```

5. **Start Docker services:**
```bash
docker-compose up --build -d
```

6. **Access services:**
   - **API**: http://localhost:8000
   - **UI**: http://localhost:8501

### Option 2: Docker Only (No Local Training)

```bash
git clone https://github.com/srinadh93/bert-sentiment-mlops.git
cd bert-sentiment-mlops
docker-compose up --build -d
```
The API will use the pre-trained DistilBERT model by default.

## API Documentation

### Health Check
**Endpoint:** `GET /health`

**Response:**
```json
{
  "status": "ok"
}
```

**Example:**
```bash
curl http://localhost:8000/health
```

### Sentiment Prediction
**Endpoint:** `POST /predict`

**Request Body:**
```json
{
  "text": "This movie was absolutely amazing!"
}
```

**Response (200 OK):**
```json
{
  "sentiment": "POSITIVE",
  "confidence": 0.9876
}
```

**Examples:**
```bash
# Positive sentiment
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"text":"I love this product! Highly recommended."}'

# Negative sentiment
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"text":"Worst experience ever. Totally disappointed."}'

# Mixed sentiment
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"text":"Good quality but expensive."}'
```

## Scripts

### preprocess.py
Downloads IMDB dataset, cleans text, and creates train/test CSVs.

**Usage:**
```bash
python scripts/preprocess.py --max-samples 10000 --out-dir data/processed
```

**Arguments:**
- `--max-samples` (int): Limit samples per split (default: None = all)
- `--out-dir` (str): Output directory for CSVs (default: data/processed)

**Output:**
- `data/processed/train.csv` — Training data (text, label)
- `data/processed/test.csv` — Test data (text, label)

### train.py
Fine-tunes a pre-trained BERT model on the preprocessed data.

**Usage:**
```bash
python scripts/train.py \
  --model-name distilbert-base-uncased \
  --epochs 3 \
  --batch-size 16 \
  --lr 2e-5
```

**Arguments:**
- `--model-name` (str): Hugging Face model (default: distilbert-base-uncased)
- `--epochs` (int): Training epochs (default: 1)
- `--batch-size` (int): Batch size (default: 16)
- `--lr` (float): Learning rate (default: 2e-5)
- `--data-dir` (str): Preprocessed data directory (default: data/processed)
- `--model-out` (str): Output model directory (default: model_output)
- `--results-dir` (str): Results directory (default: results)

**Output:**
- `model_output/` — Fine-tuned model artifacts
- `results/metrics.json` — Evaluation metrics
- `results/run_summary.json` — Hyperparameters and final metrics

### batch_predict.py
Runs predictions on a CSV file of texts.

**Usage:**
```bash
python scripts/batch_predict.py \
  --input data/unseen/predict_data.csv \
  --output results/predictions.csv
```

**Arguments:**
- `--input` (str): Input CSV with 'text' column (required)
- `--output` (str): Output CSV path (required)
- `--model-path` (str): Model directory (default: model_output)

**Input CSV Format:**
```csv
text
"Great movie!"
"Hated it."
```

**Output CSV Format:**
```csv
text,predicted_sentiment,confidence
"Great movie!",POSITIVE,0.95
"Hated it.",NEGATIVE,0.98
```

## Docker & Deployment

### Build and Run
```bash
docker-compose up --build -d
```

### Verify Services
```bash
docker ps
docker-compose logs api
docker-compose logs ui
```

### Stop Services
```bash
docker-compose down
```

### Check Health
```bash
docker-compose ps  # Should show both containers as healthy
```

## Configuration

### Environment Variables
Copy `.env.example` to `.env` and customize:

```bash
cp .env.example .env
```

**Available Variables:**
- `API_HOST` — API binding address (default: 0.0.0.0)
- `API_PORT` — API port (default: 8000)
- `MODEL_PATH` — Path to model artifacts (default: /app/model_output)
- `UI_PORT` — Streamlit UI port (default: 8501)
- `API_URL` — API URL for UI (default: http://api:8000)
- `TRAIN_MODEL_NAME` — Model for training (default: distilbert-base-uncased)
- `TRAIN_EPOCHS` — Training epochs (default: 1)
- `TRAIN_BATCH_SIZE` — Training batch size (default: 16)
- `TRAIN_LR` — Learning rate (default: 2e-5)

## Troubleshooting

### Issue: "Model not found"
**Solution:** Either train locally or use the pre-trained model fallback:
```bash
python scripts/preprocess.py --max-samples 1000
python scripts/train.py --epochs 1
```

### Issue: "Port already in use"
**Solution:** Change port in `.env` or stop conflicting services:
```bash
lsof -i :8000  # Find process using port
kill -9 <PID>
```

### Issue: Out of memory during training
**Solution:** Reduce batch size or max samples:
```bash
python scripts/train.py --batch-size 8 --epochs 1
python scripts/preprocess.py --max-samples 2000
```

### Issue: Docker build fails
**Solution:** Clear Docker cache and rebuild:
```bash
docker-compose down
docker system prune -a
docker-compose up --build -d
```

## Model Information

- **Model**: DistilBERT (default) or BERT
- **Task**: Binary sentiment classification (positive/negative)
- **Dataset**: IMDB Movie Reviews (25K train, 25K test)
- **Fine-tuning**: Transfer learning on IMDB task

## Performance Metrics

Example metrics from fine-tuning on 5000 IMDB samples (1 epoch):
- Accuracy: ~92%
- Precision: ~91%
- Recall: ~93%
- F1-Score: ~92%

*Note: Metrics vary based on dataset size, epochs, and hyperparameters.*

## Notes

- **Large model files**: If `model_output/` exceeds Git limits, it's in `.gitignore`. Train locally before deployment.
- **Results directory**: Metrics and run summaries are generated after training.
- **Streamlit caching**: First UI load may be slow as it downloads model weights.
- **Default fallback**: API uses pre-trained DistilBERT if local model unavailable.

## License

MIT License - See LICENSE file for details.

## Contact & Support

For issues or questions, open an issue on GitHub: https://github.com/srinadh93/bert-sentiment-mlops/issues
