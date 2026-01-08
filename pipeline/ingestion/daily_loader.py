import duckdb
from datetime import datetime
from typing import List, Dict

DB_PATH = "db/swiggy_reviews.duckdb"  # adjust if needed


def load_daily_reviews(target_date: str) -> List[Dict]:
    """
    Load all reviews for a specific date.

    Args:
        target_date (str): Date in 'YYYY-MM-DD' format

    Returns:
        List[Dict]: Each dict contains:
            - review_id
            - review_text
            - rating
            - review_date
    """

    # ---- 1. Validate date format ----
    try:
        parsed_date = datetime.strptime(target_date, "%Y-%m-%d").date()
    except ValueError:
        raise ValueError("target_date must be in YYYY-MM-DD format")

    # ---- 2. Connect to DuckDB ----
    con = duckdb.connect(DB_PATH)

    query = """
        SELECT
            review_id,
            review_text,
            rating,
            review_date
        FROM reviews
        WHERE review_date = ?
          AND review_text IS NOT NULL
    """

    rows = con.execute(query, [parsed_date]).fetchall()
    con.close()

    # ---- 3. Python-side validation & cleaning ----
    results: List[Dict] = []

    for review_id, review_text, rating, review_date in rows:
        text = review_text.strip()

        # drop very short / meaningless entries
        if len(text) < 5:
            continue

        results.append({
            "review_id": review_id,
            "review_text": text,
            "rating": int(rating),
            "review_date": review_date
        })

    return results
