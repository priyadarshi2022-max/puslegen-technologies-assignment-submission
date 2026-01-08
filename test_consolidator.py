from pipeline.consolidation.consolidator import consolidate_topic

topics = [
    "delivery partner rude",
    "delivery person was impolite",
    "delivery guy behaved badly",
    "high minimum order amount",
    "minimum order is too high"
]

for t in topics:
    topic_id = consolidate_topic(t)
    print(t, "→ topic_id:", topic_id)
