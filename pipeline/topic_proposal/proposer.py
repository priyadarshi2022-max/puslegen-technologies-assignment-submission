from typing import List, Dict
import json
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

# ---- LLM Client ----
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

MODEL_NAME = "gpt-4o-mini"  # or groq / together equivalent


def call_llm(prompt: str) -> str:
    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt}
        ],
        temperature=0.2,   # LOW for consistency
        max_tokens=120
    )
    return response.choices[0].message.content


SYSTEM_PROMPT = """
You are a strict JSON generator.

Task:
Extract 1 to 3 topic labels from a single app review.

Rules:
- Output MUST be valid JSON
- Output MUST be a JSON array of strings
- NO text outside JSON
- NO explanations
- NO markdown
- NO numbering
- Short noun phrases only
- Topics must reflect issues, requests, or feedback

If no clear topic exists, output an empty JSON array: []

Correct Output Examples:
["delivery partner rude", "delivery delay"]
["high minimum order amount"]
[]
"""


def propose_topics(review: Dict) -> List[str]:
    prompt = f"""
Review text:
{review['normalized_text']}
"""

    raw_response = call_llm(prompt)

    try:
        topics = json.loads(raw_response)
        return [t.strip().lower() for t in topics if len(t.strip()) > 3]
    except Exception as e:
        print("JSON PARSE ERROR:", e)
        return []
