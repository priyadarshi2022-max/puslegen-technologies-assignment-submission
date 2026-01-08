from google_play_scraper import reviews, Sort
import pandas as pd
from datetime import datetime, timezone
import os
import duckdb

APP_ID = "in.swiggy.android"
START_DATE = datetime(2024, 6, 1, tzinfo=timezone.utc)
END_DATE = datetime.now(timezone.utc)


DB_PATH = "swiggy_reviews.duckdb"

con = duckdb.connect(DB_PATH)
con.execute("""
CREATE TABLE IF NOT EXISTS reviews (
            review_id VARCHAR,
            app_id VARCHAR,
            review_text VARCHAR,
            rating INTEGER,
            review_time TIMESTAMP,
            review_date DATE
)
""")


continuation_token = None
total_inserted = 0

while True:
  result, continuation_token = reviews(
    APP_ID,
    lang='en',
    country='in',
    sort=Sort.NEWEST,
    count=200,
    continuation_token=continuation_token
  )

  if not result:
    print("No more reviews returned. Stopping scrape")
    break
  

  last_review_date = result[-1]['at']

  if last_review_date.tzinfo is None:
    last_review_date = last_review_date.replace(tzinfo=timezone.utc)

  batch_rows = []

  for r in result:
    review_time = r["at"]

    if review_time.tzinfo is None:
      review_time = review_time.replace(tzinfo=timezone.utc)
    if START_DATE <= review_time <= END_DATE:
      batch_rows.append({
        "review_id": r["reviewId"],
        "app_id": APP_ID,
        "review_text": r["content"],
        "rating": r["score"],
        "review_time": review_time,
        "review_date": review_time.date()
      })

  if batch_rows:
    df_batch = pd.DataFrame(batch_rows)
    con.execute(
      "INSERT INTO reviews SELECT * FROM df_batch"
    )
    total_inserted += len(df_batch)

  print(
    f"Inserted {total_inserted} reviews so far"
    f"(current batch last date: {last_review_date.date()})"
  )

  if last_review_date < START_DATE:
    print("Reached reviews older than June 2024. Stopping scrape.")
    break
  
  if not continuation_token:
    print("No continuation token. Stopping scrape")
    break
  
