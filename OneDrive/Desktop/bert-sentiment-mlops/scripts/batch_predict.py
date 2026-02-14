"""Batch prediction using a saved model in `model_output/`.
Usage:
  python scripts/batch_predict.py --input data/unseen/predict_data.csv --output results/predictions.csv
"""
import argparse
import os
import pandas as pd
from transformers import pipeline


def main(input_file, output_file, model_path="model_output"):
    os.makedirs(os.path.dirname(output_file) or ".", exist_ok=True)
    if not os.path.exists(input_file):
        raise FileNotFoundError(input_file)

    df = pd.read_csv(input_file)
    if "text" not in df.columns:
        raise ValueError("Input CSV must contain a 'text' column")

    sentiment = pipeline("sentiment-analysis", model=model_path, tokenizer=model_path)
    preds = sentiment(list(df["text"].fillna("")))

    df["predicted_sentiment"] = [p["label"] for p in preds]
    df["confidence"] = [float(p["score"]) for p in preds]
    df.to_csv(output_file, index=False)
    print(f"Wrote predictions to {output_file}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--model-path", default="model_output")
    args = parser.parse_args()
    main(args.input, args.output, model_path=args.model_path)
