import json
from langgraph.graph import StateGraph, END
from langchain_core.messages import SystemMessage, HumanMessage

from app.core.llm import get_llm
from app.services.analysis.state import AnalysisState
from app.services.analysis.prompts import LECTURE_AGG_ANALYSIS_SYSTEM_PROMPT

llm = get_llm()


def preprocess_node(state: AnalysisState) -> AnalysisState:
    full_text = (state.get("full_text") or "").strip()
    cleaned_text = " ".join(full_text.split())
    return {"cleaned_text": cleaned_text}


def analyze_node(state: AnalysisState) -> AnalysisState:
    cleaned_text = state.get("cleaned_text", "")
    candidate_ranges = state.get("candidate_ranges", [])
    segments = state.get("segments", [])

    human_text = f"""
candidateRanges:
{json.dumps(candidate_ranges, ensure_ascii=False)}

segments:
{json.dumps(segments, ensure_ascii=False)}

relatedText:
{cleaned_text}
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
        data = json.loads(raw)
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
            "teacher_guides": teacher_guides[:3],
        }
    except Exception:
        return {
            "quizzes": [],
            "teacher_guides": [],
        }


def build_lecture_agg_graph():
    graph = StateGraph(AnalysisState)
    graph.add_node("preprocess", preprocess_node)
    graph.add_node("analyze", analyze_node)
    graph.add_node("parse", parse_node)

    graph.set_entry_point("preprocess")
    graph.add_edge("preprocess", "analyze")
    graph.add_edge("analyze", "parse")
    graph.add_edge("parse", END)

    return graph.compile()