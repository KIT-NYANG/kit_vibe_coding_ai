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

    def analyze_aggregate(self, candidate_ranges: list, segments: list) -> AggregateAnalysisResponse:
        try:
            graph = analysis_graph_factory.get_graph("lecture_agg")

            result = graph.invoke({
                "candidate_ranges": candidate_ranges,
                "segments": segments
            })
            return AggregateAnalysisResponse(
                quizzes=result.get("quizzes", []),
                teacherGuides=result.get("teacherGuides", []),
            )
        except Exception:
            return AggregateAnalysisResponse(
                quizzes=[],
                teacherGuides=[],
            )


analysis_service = AnalysisService()