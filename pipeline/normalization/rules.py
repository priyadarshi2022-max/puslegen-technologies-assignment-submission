import re

STOP_PHRASES = [
    "very very",
    "very",
    "worst",
    "bad",
    "really",
    "please",
]

def rule_based_cleanup(text: str) -> str:
    text = text.lower()

    # remove non-alphanumeric except spaces
    text = re.sub(r"[^a-z0-9\s]", " ", text)

    # collapse repeated characters
    text = re.sub(r"(.)\1{2,}", r"\1", text)

    # remove stop phrases
    for phrase in STOP_PHRASES:
        text = text.replace(phrase, "")

    # normalize whitespace
    text = re.sub(r"\s+", " ", text).strip()

    return text
