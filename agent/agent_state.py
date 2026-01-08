from typing import TypedDict, List, Dict

class AgentState(TypedDict):
  date: str
  reviews: List[str]
  extracted_issues: List[str]
  canonical_topics: List[str]
  topic_counts: Dict[str, int]