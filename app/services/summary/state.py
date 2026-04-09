# services/summary/state.py - 그래프 각 단계에서 주고받는 데이터 구조 정의

from typing import TypedDict, List

class SummaryState(TypedDict, total=False):
    text: str
    cleaned_text: str
    llm_response: str
    summary_text: str
    keywords: List[str]