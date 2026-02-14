"""Preprocess script: download IMDB from Hugging Face, clean, and save CSVs.
Usage:
  python scripts/preprocess.py --max-samples 50000
"""
import argparse
import re
from datasets import load_dataset
import pandas as pd
import os


def clean_text(text: str) -> str:
    text = re.sub(r"http\S+", "", text)
    text = re.sub(r"[^\w\s\.,!?']", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def main(max_samples: int = None, out_dir: str = "data/processed"):
    os.makedirs(out_dir, exist_ok=True)
    ds = load_dataset("imdb")

    for split in ["train", "test"]:
        records = []
        dataset = ds[split]
        for i, item in enumerate(dataset):
            if max_samples and i >= max_samples:
                break
            text = clean_text(item["text"])
            label = int(item["label"])  # 0 or 1
            records.append({"text": text, "label": label})

        df = pd.DataFrame(records)
        out_path = os.path.join(out_dir, f"{split}.csv")
        df.to_csv(out_path, index=False)
        print(f"Wrote {len(df)} rows to {out_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-samples", type=int, default=None)
    parser.add_argument("--out-dir", type=str, default="data/processed")
    args = parser.parse_args()
    main(max_samples=args.max_samples, out_dir=args.out_dir)
