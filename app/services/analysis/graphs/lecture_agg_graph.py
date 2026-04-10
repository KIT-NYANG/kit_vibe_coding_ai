import json
from langgraph.graph import StateGraph, END
from langchain_core.messages import SystemMessage, HumanMessage

from app.core.llm import get_llm
from app.services.analysis.state import AnalysisState
from app.services.analysis.prompts import LECTURE_AGG_ANALYSIS_SYSTEM_PROMPT

llm = get_llm()


def analyze_node(state: AnalysisState) -> AnalysisState:

    candidate_ranges = state.get("candidate_ranges", []) or []
    segments = state.get("segments", []) or []

    # CandidateRange 객체 -> dict
    candidate_range_dicts = [
        {
            "startSec": getattr(r, "startSec", None),
            "endSec": getattr(r, "endSec", None),
            "pauseCount": getattr(r, "pauseCount", 0),
            "seekBackCount": getattr(r, "seekBackCount", 0),
            "affectedUserCount": getattr(r, "affectedUserCount", 0),
            "score": getattr(r, "score", 0),
            "reasons": getattr(r, "reasons", []),
        }
        for r in candidate_ranges
    ]

    # SegmentResponse 객체 -> 문자열
    segment_text = "\n".join(
        f"{getattr(s, 'start', '')}~{getattr(s, 'end', '')} : {getattr(s, 'text', '').strip()}"
        for s in segments
        if getattr(s, "text", "").strip()
    )


    human_text = f"""
candidateRanges:
{json.dumps(candidate_range_dicts, ensure_ascii=False)}

segments:
{segment_text}
"""

    messages = [
        SystemMessage(content=LECTURE_AGG_ANALYSIS_SYSTEM_PROMPT),
        HumanMessage(content=human_text),
    ]

    response = llm.invoke(messages)

    return {"llm_response": response.content}


def normalize_quiz_item(item: dict) -> dict:
    return {
        "quizInsertTimeSec": item.get("quizInsertTimeSec", item.get("quiz_insert_time_sec")),
        "question": item.get("question", ""),
        "answer": item.get("answer", ""),
        "explanation": item.get("explanation", ""),
        "supplementalDescription": item.get(
            "supplementalDescription",
            item.get("supplemental_description", "")
        ),
    }


def normalize_teacher_guide(item: dict) -> dict:
    return {
        "predictedDifficultSection": item.get(
            "predictedDifficultSection",
            item.get("predicted_difficult_section", "")
        ),
        "predictedReason": item.get(
            "predictedReason",
            item.get("predicted_reason", "")
        ),
        "improvementSuggestion": item.get(
            "improvementSuggestion",
            item.get("improvement_suggestion", "")
        ),
    }


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
        teacher_guides = data.get("teacherGuides", data.get("teacher_guides", []))

        if not isinstance(quizzes, list):
            quizzes = []
        if not isinstance(teacher_guides, list):
            teacher_guides = []

        quizzes = [normalize_quiz_item(item) for item in quizzes if isinstance(item, dict)]
        teacher_guides = [normalize_teacher_guide(item) for item in teacher_guides if isinstance(item, dict)]

        return {
            "quizzes": quizzes[:3],
            "teacherGuides": teacher_guides[:3],  # 여기 중요
        }
    except Exception as e:
        print(f"parse error: {type(e).__name__}: {e}")
        print(raw)
        return {
            "quizzes": [],
            "teacherGuides": [],
        }


def build_lecture_agg_graph():
    graph = StateGraph(AnalysisState)
    graph.add_node("analyze", analyze_node)
    graph.add_node("parse", parse_node)

    graph.set_entry_point("analyze")
    graph.add_edge("analyze", "parse")
    graph.add_edge("parse", END)

    return graph.compile()