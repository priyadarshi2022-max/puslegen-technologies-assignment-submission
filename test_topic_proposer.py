from pipeline.ingestion.daily_loader import load_daily_reviews
from pipeline.normalization.normalizer import normalize_review
from pipeline.topic_proposal.proposer import propose_topics

reviews = load_daily_reviews("2024-07-15")

for r in reviews[:5]:
    norm = normalize_review(r)
    topics = propose_topics(norm)

    print("REVIEW:", norm["normalized_text"])
    print("TOPICS:", topics)
    print("-" * 60)
