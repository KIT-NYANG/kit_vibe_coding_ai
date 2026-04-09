from typing import TypedDict, List, Dict, Any


class AnalysisState(TypedDict, total=False):
    full_text: str
    segments: List[Dict[str, Any]]
    candidate_ranges: List[Dict[str, Any]]
    cleaned_text: str
    llm_response: str
    quizzes: List[Dict[str, Any]]
    teacherGuides: List[Dict[str, Any]]
    analyzed_log_count: int