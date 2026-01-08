import duckdb
from pipeline.ingestion.daily_loader import load_daily_reviews
from pipeline.normalization.normalizer import normalize_review
from pipeline.topic_proposal.proposer import propose_topics
from pipeline.consolidation.consolidator import consolidate_topic

DB_PATH = "db/swiggy_reviews.duckdb"


def process_day(target_date: str, limit: int = 10):
    """
    Processes reviews for a single date.
    LIMIT is for safe testing only.
    """

    print(f"\n📅 Processing date: {target_date}")

    con = duckdb.connect(DB_PATH)

    con.execute("""
        CREATE TABLE IF NOT EXISTS daily_topic_counts (
            topic_id INTEGER,
            review_date DATE,
            count INTEGER
        )
    """)

    reviews = load_daily_reviews(target_date)
    print(f"🧾 Total reviews found: {len(reviews)}")

    # ✅ SAFETY GUARD (THIS IS THE KEY LINE)
    reviews = reviews[:limit]
    print(f"⚠️  Processing only first {len(reviews)} reviews (SAFE MODE)")

    topic_counter = {}

    for idx, review in enumerate(reviews, start=1):
        print(f"\n🔍 Review {idx}/{len(reviews)}")

        norm = normalize_review(review)
        proposed_topics = propose_topics(norm)

        print("   Topics:", proposed_topics)

        for topic_text in proposed_topics:
            topic_id = consolidate_topic(topic_text)
            key = (topic_id, review["review_date"])
            topic_counter[key] = topic_counter.get(key, 0) + 1

        print(f"✅ Done review {idx}")

    print("\n💾 Writing counts to DB")

    for (topic_id, date), count in topic_counter.items():
        con.execute("""
            DELETE FROM daily_topic_counts
            WHERE topic_id = ? AND review_date = ?
        """, [topic_id, date])

        con.execute("""
            INSERT INTO daily_topic_counts (topic_id, review_date, count)
            VALUES (?, ?, ?)
        """, [topic_id, date, count])

    con.close()
    print("✅ Day processing complete\n")
