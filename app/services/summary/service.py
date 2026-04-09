# services/summary/service.py - 그래프 선택, invoke, 결과 반환

from app.schemas.summary import SummarizeResponse
from app.services.summary.graph_factory import graph_factory

# "lecture_summary" 그래프를 가져와 실행하고 결과를 SummarizeResponse로 반환
class SummaryService:
    def summarize_lecture(self, text: str) -> SummarizeResponse:
        if not text or not text.strip():
            return SummarizeResponse(
                summary_text="",
                keywords=[]
            )

        try:
            graph = graph_factory.get_graph("lecture_summary")
            result = graph.invoke({"text": text})

            return SummarizeResponse(
                summary_text=result.get("summary_text", ""),
                keywords=result.get("keywords", []),
            )
        except Exception as e:
            print(e)
            return SummarizeResponse(
                summary_text="요약 생성 중 오류가 발생했습니다.",
                keywords=[],
            )


summary_service = SummaryService()