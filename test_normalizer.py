from pipeline.ingestion.daily_loader import load_daily_reviews
from pipeline.normalization.normalizer import normalize_review

reviews = load_daily_reviews("2024-07-15")

for r in reviews[:5]:
    out = normalize_review(r)
    print("RAW :", out["original_text"])
    print("NORM:", out["normalized_text"])
    print("-" * 60)
