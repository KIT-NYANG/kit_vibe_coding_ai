import json
from langgraph.graph import StateGraph, END
from langchain_core.messages import SystemMessage, HumanMessage

from app.core.llm import get_llm
from app.services.analysis.state import AnalysisState
from app.services.analysis.prompts import LECTURE_PRE_ANALYSIS_SYSTEM_PROMPT

llm = get_llm()

def preprocess_node(state: AnalysisState) -> AnalysisState:
    full_text = (state.get("full_text") or "").strip()
    cleaned_text = " ".join(full_text.split())
    return {"cleaned_text": cleaned_text}


def analyze_node(state: AnalysisState) -> AnalysisState:
    #cleaned_text = state.get("cleaned_text", "")
    segments = state.get("segments", [])

    segment_data = "\n".join(
    f"{s.get('start', '')}~{s.get('end', '')} : {(s.get('text') or '').strip()}"
    for s in segments
    )
    human_text = f"""

segments:
{json.dumps(segment_data, ensure_ascii=False)}
"""

    messages = [
        SystemMessage(content=LECTURE_PRE_ANALYSIS_SYSTEM_PROMPT),
        HumanMessage(content=human_text),
    ]

    response = llm.invoke(messages)
    return {"llm_response": response.content}


def parse_node(state: AnalysisState) -> AnalysisState:
    raw = state.get("llm_response", "")

    try:
        cleaned = raw.strip()

        if cleaned.startswith("```json"):
            cleaned = cleaned[len("```json"):].strip()
        elif cleaned.startswith("```"):
            cleaned = cleaned[len("```"):].strip()

        if cleaned.endswith("```"):
            cleaned = cleaned[:-3].strip()

        data = json.loads(cleaned)

        quizzes = data.get("quizzes", [])
        teacherGuides = data.get("teacherGuides", [])

        if not isinstance(quizzes, list):
            quizzes = []
        if not isinstance(teacherGuides, list):
            teacherGuides = []

        return {
            "quizzes": quizzes[:3],
            "teacherGuides": teacherGuides[:3],
        }
    except Exception as e:
        print(f"parse error: {type(e).__name__}: {e}")
        print(raw)
        return {
            "quizzes": [],
            "teacherGuides": [],
        }


def build_lecture_pre_graph():
    graph = StateGraph(AnalysisState)
    #graph.add_node("preprocess", preprocess_node)
    graph.add_node("analyze", analyze_node)
    graph.add_node("parse", parse_node)

    graph.set_entry_point("analyze")
    #graph.set_entry_point("preprocess")
    #graph.add_edge("preprocess", "analyze")
    graph.add_edge("analyze", "parse")
    graph.add_edge("parse", END)

    return graph.compile()