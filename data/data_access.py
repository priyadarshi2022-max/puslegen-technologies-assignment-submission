def get_daily_reviews(con, date: str) -> list[str]:
  df = con.execute(
    f"""
    SELECT review_text
    FROM reviews
    WHERE review_date = '{date}
    """
  ).df()
  return df["review_text"].tolist()