from app.schemas.analysis import (
    PreAnalysisResponse,
    AggregateAnalysisResponse,
)
from app.services.analysis.graph_factory import analysis_graph_factory


class AnalysisService:
    def analyze_pre(self, segments: list) -> PreAnalysisResponse:
        try:
            graph = analysis_graph_factory.get_graph("lecture_pre")
            result = graph.invoke({
                #"full_text": full_text, #세그먼트만 보내기
                "segments": segments,
            })

            return PreAnalysisResponse(
                quizzes=result.get("quizzes", []),
                teacherGuides=result.get("teacherGuides", []),
            )
        except Exception as e:
            print(e)
            return PreAnalysisResponse(
                quizzes=[],
                teacherGuides=[],
            )

    def analyze_aggregate(self, lecture_id: int, candidate_ranges: list, full_text: str = "", additional_prompt: str = "") -> AggregateAnalysisResponse:
        try:
            graph = analysis_graph_factory.get_graph("lecture_agg")
            result = graph.invoke({
                "lecture_id": lecture_id,
                "candidate_ranges": candidate_ranges,
                "full_text": full_text,
                "additional_prompt": additional_prompt,
            })

            return AggregateAnalysisResponse(
                lecture_id=lecture_id,
                analyzed_log_count=len(candidate_ranges),
                quizzes=result.get("quizzes", []),
                teacher_guides=result.get("teacher_guides", []),
            )
        except Exception:
            return AggregateAnalysisResponse(
                lecture_id=lecture_id,
                analyzed_log_count=len(candidate_ranges),
                quizzes=[],
                teacher_guides=[],
            )


analysis_service = AnalysisService()