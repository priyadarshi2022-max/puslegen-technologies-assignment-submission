import duckdb
import numpy as np
import re
from pipeline.consolidation.embedder import embed_text

DB_PATH = "db/swiggy_reviews.duckdb"
SIMILARITY_THRESHOLD = 0.72


# -------------------------
# Text normalization (CRITICAL)
# -------------------------
def normalize_topic_text(text: str) -> str:
    """
    Normalize short topic phrases to stabilize embeddings.
    """
    text = text.lower()

    # remove filler verbs / articles
    text = re.sub(
        r"\b(was|were|is|are|been|being|very|extremely|too)\b",
        "",
        text,
    )

    # normalize people references
    text = re.sub(
        r"\b(delivery guy|delivery person|delivery partner)\b",
        "delivery partner",
        text,
    )

    # normalize whitespace
    text = re.sub(r"\s+", " ", text).strip()

    return text


def cosine_similarity(a, b):
    a = np.array(a)
    b = np.array(b)
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))


def consolidate_topic(topic_text: str) -> int:
    """
    Returns canonical topic_id for a proposed topic
    """

    con = duckdb.connect(DB_PATH)

    # ---- Ensure schema exists ----
    con.execute("CREATE SEQUENCE IF NOT EXISTS seq_topic_id;")

    con.execute("""
        CREATE TABLE IF NOT EXISTS topics (
            topic_id INTEGER PRIMARY KEY DEFAULT nextval('seq_topic_id'),
            canonical_name VARCHAR,
            created_on DATE
        )
    """)

    con.execute("""
        CREATE TABLE IF NOT EXISTS topic_variants (
            variant_text VARCHAR,
            topic_id INTEGER
        )
    """)

    # ---- Normalize incoming topic ----
    normalized_topic = normalize_topic_text(topic_text)
    new_embedding = embed_text(normalized_topic)

    # ---- Compare ONLY against canonical topics ----
    rows = con.execute("""
        SELECT topic_id, canonical_name
        FROM topics
    """).fetchall()

    best_match = None
    best_score = 0.0

    for topic_id, canonical in rows:
        canonical_norm = normalize_topic_text(canonical)
        canonical_embedding = embed_text(canonical_norm)

        score = cosine_similarity(new_embedding, canonical_embedding)

        if score > best_score:
            best_score = score
            best_match = topic_id

    # ---- Decision ----
    if best_match is not None and best_score >= SIMILARITY_THRESHOLD:
        final_topic_id = best_match
    else:
        con.execute(
            "INSERT INTO topics (canonical_name, created_on) VALUES (?, CURRENT_DATE)",
            [normalized_topic]
        )
        final_topic_id = con.execute(
            "SELECT max(topic_id) FROM topics"
        ).fetchone()[0]

    # ---- Store variant (original surface form) ----
    con.execute(
        "INSERT INTO topic_variants (variant_text, topic_id) VALUES (?, ?)",
        [topic_text, final_topic_id]
    )

    con.close()
    return final_topic_id
