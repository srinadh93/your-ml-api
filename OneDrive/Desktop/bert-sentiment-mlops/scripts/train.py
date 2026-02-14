"""Train script using Hugging Face Transformers Trainer API.
Saves model artifacts to model_output/ and metrics to results/.
"""
import argparse
import os
import json
from datasets import load_dataset, Dataset
import pandas as pd
from transformers import (
    AutoTokenizer,
    AutoModelForSequenceClassification,
    TrainingArguments,
    Trainer,
)
import numpy as np
from sklearn.metrics import accuracy_score, precision_recall_fscore_support


def compute_metrics(pred):
    labels = pred.label_ids
    preds = np.argmax(pred.predictions, axis=1)
    precision, recall, f1, _ = precision_recall_fscore_support(labels, preds, average="binary")
    acc = accuracy_score(labels, preds)
    return {
        "accuracy": float(acc),
        "precision": float(precision),
        "recall": float(recall),
        "f1_score": float(f1),
    }


def load_csv_dataset(path):
    df = pd.read_csv(path)
    return Dataset.from_pandas(df)


def main(
    model_name="distilbert-base-uncased",
    epochs=1,
    batch_size=16,
    lr=2e-5,
    data_dir="data/processed",
    model_out="model_output",
    results_dir="results",
):
    os.makedirs(model_out, exist_ok=True)
    os.makedirs(results_dir, exist_ok=True)

    train_ds = load_csv_dataset(os.path.join(data_dir, "train.csv"))
    test_ds = load_csv_dataset(os.path.join(data_dir, "test.csv"))

    tokenizer = AutoTokenizer.from_pretrained(model_name)

    def tokenize(batch):
        return tokenizer(batch["text"], padding=True, truncation=True, max_length=256)

    train_tok = train_ds.map(tokenize, batched=True)
    test_tok = test_ds.map(tokenize, batched=True)

    model = AutoModelForSequenceClassification.from_pretrained(model_name, num_labels=2)

    args = TrainingArguments(
        output_dir=model_out,
        num_train_epochs=epochs,
        per_device_train_batch_size=batch_size,
        per_device_eval_batch_size=batch_size,
        evaluation_strategy="epoch",
        save_strategy="epoch",
        learning_rate=lr,
        logging_steps=50,
        load_best_model_at_end=True,
        metric_for_best_model="f1_score",
    )

    trainer = Trainer(
        model=model,
        args=args,
        train_dataset=train_tok,
        eval_dataset=test_tok,
        tokenizer=tokenizer,
        compute_metrics=compute_metrics,
    )

    trainer.train()

    metrics = trainer.evaluate()
    # Ensure keys match required schema
    required_metrics = {k: float(metrics.get(k, 0.0)) for k in ["eval_accuracy", "eval_f1_score"]}

    # Convert compute_metrics output if present
    computed = compute_metrics(trainer.predict(test_tok))

    metrics_out = {
        "accuracy": computed["accuracy"],
        "precision": computed["precision"],
        "recall": computed["recall"],
        "f1_score": computed["f1_score"],
    }

    with open(os.path.join(results_dir, "metrics.json"), "w") as f:
        json.dump(metrics_out, f, indent=2)

    summary = {
        "hyperparameters": {
            "model_name": model_name,
            "learning_rate": float(lr),
            "batch_size": int(batch_size),
            "num_epochs": int(epochs),
        },
        "final_metrics": {
            "accuracy": metrics_out["accuracy"],
            "f1_score": metrics_out["f1_score"],
        },
    }

    with open(os.path.join(results_dir, "run_summary.json"), "w") as f:
        json.dump(summary, f, indent=2)

    # Save model and tokenizer
    trainer.save_model(model_out)
    tokenizer.save_pretrained(model_out)

    print("Training complete. Model saved to", model_out)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--model-name", default="distilbert-base-uncased")
    parser.add_argument("--epochs", type=int, default=1)
    parser.add_argument("--batch-size", type=int, default=16)
    parser.add_argument("--lr", type=float, default=2e-5)
    parser.add_argument("--data-dir", default="data/processed")
    parser.add_argument("--model-out", default="model_output")
    parser.add_argument("--results-dir", default="results")
    args = parser.parse_args()
    main(
        model_name=args.model_name,
        epochs=args.epochs,
        batch_size=args.batch_size,
        lr=args.lr,
        data_dir=args.data_dir,
        model_out=args.model_out,
        results_dir=args.results_dir,
    )
