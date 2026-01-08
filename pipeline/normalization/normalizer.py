from typing import Dict
from pipeline.normalization.rules import rule_based_cleanup

# placeholder for now — real LLM later
def llm_compress(text: str) -> str:
    """
    TEMP implementation:
    This will later be replaced by an LLM call.
    """
    return text


def normalize_review(review: Dict) -> Dict:
    cleaned = rule_based_cleanup(review["review_text"])
    compressed = llm_compress(cleaned)

    return {
        "review_id": review["review_id"],
        "original_text": review["review_text"],
        "normalized_text": compressed,
        "rating": review["rating"],
        "review_date": review["review_date"]
    }
