# services/summary/graphs/lecture_summary_graph.py - LangGraph 정의
# preprocess → summarize → parse → END

import json
import re
from langgraph.graph import StateGraph, END
from langchain_core.messages import SystemMessage, HumanMessage

from app.core.llm import get_summary_llm
from app.services.summary.state import SummaryState
from app.services.summary.prompts import LECTURE_SUMMARY_SYSTEM_PROMPT

# 요약에 사용할 LLM 객체 생성
llm = get_summary_llm()

def remove_cjk(text: str) -> str:
    if not isinstance(text, str):
        return ""

    # 문자열에서 CJK 계열 문자(중국어, 일본어 등)를 제거
    text = re.sub(r'[\u4E00-\u9FFF\u3400-\u4DBF\u3040-\u30FF]+', '', text)

    # 공백 정리
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def preprocess_node(state: SummaryState) -> SummaryState:
    """
    1단계: 전처리 노드

    입력:
    - state["text"] : 원본 STT 텍스트

    처리:
    - 앞뒤 공백 제거
    - 줄바꿈/중복 공백을 하나의 공백으로 정리

    출력:
    - cleaned_text
    """
    text = state.get("text", "").strip()
    cleaned = " ".join(text.split())
    return {"cleaned_text": cleaned}


def summarize_node(state: SummaryState) -> SummaryState:
    """
    2단계: LLM 요약 노드

    입력:
    - state["cleaned_text"]

    처리:
    - SystemPrompt + HumanMessage 구성
    - LLM 호출
    - 모델이 JSON 문자열 형태로 응답한다고 가정

    출력:
    - llm_response : LLM의 원본 응답 문자열
    """
    text = state.get("cleaned_text", "")

    # 입력 텍스트가 비어 있으면 빈 결과를 JSON 문자열 형태로 반환
    if not text:
        return {
            "llm_response": '{"summary_text": "", "keywords": []}'
        }

    messages = [
        SystemMessage(content=LECTURE_SUMMARY_SYSTEM_PROMPT),
        HumanMessage(content=f"다음은 강의 STT 원문이다.\n\n{text}")
    ]

    response = llm.invoke(messages)
    return {"llm_response": response.content}


def parse_node(state: SummaryState) -> SummaryState:
    """
    3단계: 파싱 노드

    입력:
    - state["llm_response"]

    처리:
    - JSON 파싱 시도
    - summary_text, keywords 추출
    - 타입 검증
    - CJK 문자 제거
    - keywords 최대 3개로 제한

    예외 처리:
    - JSON 파싱 실패 시 raw 문자열 자체를 summary_text로 사용
    - keywords는 빈 리스트 반환

    출력:
    - summary_text
    - keywords
    """
    raw = state.get("llm_response", "")

    try:
        data = json.loads(raw)
        summary_text = data.get("summary_text", "")
        keywords = data.get("keywords", [])

        if not isinstance(summary_text, str):
            summary_text = ""
        if not isinstance(keywords, list):
            keywords = []

        # 요약문 후처리
        summary_text = remove_cjk(summary_text)

        # 키워드 후처리
        keywords = [remove_cjk(str(k).strip()) for k in keywords if str(k).strip()]
        keywords = [str(k).strip() for k in keywords if str(k).strip()]

        # 최대 3개만 사용
        keywords = keywords[:3]

        return {
            "summary_text": summary_text,
            "keywords": keywords,
        }
    except Exception:
        # JSON 파싱 실패 시, raw 문자열을 그대로 summary_text로 사용
        return {
            "summary_text": remove_cjk(raw) if isinstance(raw, str) else "",
            "keywords": [],
        }

# 강의 요약용 LangGraph 생성 함수
def build_lecture_summary_graph():
    graph = StateGraph(SummaryState)

    # 노드 등록
    graph.add_node("preprocess", preprocess_node)
    graph.add_node("summarize", summarize_node)
    graph.add_node("parse", parse_node)

    # 시작 노드 설정
    graph.set_entry_point("preprocess")

    # 노드 연결
    graph.add_edge("preprocess", "summarize")
    graph.add_edge("summarize", "parse")
    graph.add_edge("parse", END)

    # 컴파일 후 반환
    return graph.compile()