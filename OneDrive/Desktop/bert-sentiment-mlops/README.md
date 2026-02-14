# BERT Sentiment MLOps Project

This repository contains a full MLOps-style sentiment analysis pipeline using a pretrained transformer (DistilBERT by default), fine-tuning, a FastAPI serving endpoint, and a Streamlit UI. Everything is containerized and orchestrated via `docker-compose`.

Quick start

1. Create a Python environment and install dependencies listed in `requirements.txt`.
2. (Optional) Run data preprocessing:

```bash
python scripts/preprocess.py --max-samples 10000
```

3. Train the model (will save to `model_output/` and write metrics to `results/`):

```bash
python scripts/train.py --model-name distilbert-base-uncased --epochs 1
```

4. Start services with Docker Compose (build will include `model_output/` if present):

```bash
docker-compose up --build -d
```

Services
- `api` — FastAPI model server (http://localhost:8000)
- `ui` — Streamlit frontend (http://localhost:8501)

Files of interest
- `scripts/preprocess.py` — download/clean IMDB and create `data/processed/train.csv` and `test.csv`
- `scripts/train.py` — fine-tune model and save artifacts to `model_output/`, writes `results/metrics.json` and `results/run_summary.json`
- `src/api.py` — FastAPI app exposing `/health` and `/predict`
- `src/ui.py` — Streamlit UI calling the API
- `scripts/batch_predict.py` — run predictions on a CSV of texts

Notes
- If model artifacts are large, add `model_output/` and `results/` to `.gitignore` and train locally before building the API image.
- Use the `.env.example` to configure the environment.