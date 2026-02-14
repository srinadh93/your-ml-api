from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification


class PredictRequest(BaseModel):
    text: str


app = FastAPI()
predictor = None


@app.on_event("startup")
def load_model():
    global predictor
    model_path = os.environ.get("MODEL_PATH", "/app/model_output")
    
    # Check if model exists
    if not os.path.exists(model_path) or not os.listdir(model_path):
        print(f"Warning: Model not found at {model_path}. Using default distilbert-base-uncased model.")
        print("To use a fine-tuned model, run: python scripts/preprocess.py && python scripts/train.py")
        model_path = "distilbert-base-uncased"
    
    try:
        # Use pipeline for simplicity
        predictor = pipeline("sentiment-analysis", model=model_path, tokenizer=model_path)
        print(f"Model loaded successfully from {model_path}")
    except Exception as e:
        print(f"Error loading model: {e}")
        raise


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/predict")
def predict(req: PredictRequest):
    global predictor
    if predictor is None:
        raise HTTPException(status_code=500, detail="Model not loaded")
    text = req.text
    if not isinstance(text, str) or not text.strip():
        raise HTTPException(status_code=400, detail="Input text must be a non-empty string")

    res = predictor(text[:10000])
    if not res:
        raise HTTPException(status_code=500, detail="Prediction failed")

    label = res[0]["label"]
    score = float(res[0]["score"]) if "score" in res[0] else 0.0

    return {"sentiment": label, "confidence": score}
