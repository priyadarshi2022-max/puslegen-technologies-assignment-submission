import duckdb
import pandas as pd
from datetime import datetime, timedelta

DB_PATH = "db/swiggy_reviews.duckdb"


def generate_trend_report(target_date: str, window: int = 30) -> pd.DataFrame:
    end_date = datetime.strptime(target_date, "%Y-%m-%d").date()
    start_date = end_date - timedelta(days=window)

    con = duckdb.connect(DB_PATH)

    df = con.execute("""
        SELECT
            t.canonical_name AS topic,
            d.review_date,
            d.count
        FROM daily_topic_counts d
        JOIN topics t ON d.topic_id = t.topic_id
        WHERE d.review_date BETWEEN ? AND ?
    """, [start_date, end_date]).df()

    con.close()

    if df.empty:
        return pd.DataFrame()

    pivot = df.pivot_table(
        index="topic",
        columns="review_date",
        values="count",
        fill_value=0
    ).sort_index(axis=1)

    return pivot
