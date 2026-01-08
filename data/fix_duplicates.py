import duckdb

con = duckdb.connect("swiggy_reviews.duckdb")

# 1. Create deduplicated table
con.execute("""
CREATE TABLE reviews_dedup AS
SELECT *
FROM (
    SELECT *,
           ROW_NUMBER() OVER (
               PARTITION BY review_id
               ORDER BY review_time DESC
           ) AS rn
    FROM reviews
)
WHERE rn = 1
""")

# 2. Replace old table
con.execute("DROP TABLE reviews")
con.execute("ALTER TABLE reviews_dedup RENAME TO reviews")

# 3. Enforce uniqueness going forward
con.execute("""
CREATE UNIQUE INDEX IF NOT EXISTS idx_review_id
ON reviews(review_id)
""")

con.close()

print("✅ Deduplication complete.")
