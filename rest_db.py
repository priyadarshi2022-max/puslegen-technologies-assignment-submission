import duckdb

con = duckdb.connect("db/swiggy_reviews.duckdb")

con.execute("DROP TABLE IF EXISTS topic_variants")
con.execute("DROP TABLE IF EXISTS topics")
con.execute("DROP SEQUENCE IF EXISTS seq_topic_id")

con.close()

print("✅ Topic tables reset")
