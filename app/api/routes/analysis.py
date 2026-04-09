from fastapi import APIRouter, HTTPException
from app.schemas.analysis import AggregateAnalysisRequest, AggregateAnalysisResponse
from app.services.analysis.service import analysis_service

router = APIRouter(prefix="/api/analysis", tags=["analysis"])


@router.post("/aggregate", response_model=AggregateAnalysisResponse)
async def aggregate_analysis(request: AggregateAnalysisRequest) -> AggregateAnalysisResponse:
    try:
        result = analysis_service.analyze_aggregate(
            lecture_id=request.lecture_id,
            candidate_ranges=[item.model_dump() for item in request.candidate_ranges],
            full_text=request.full_text or "",
            additional_prompt=request.additional_prompt or "",
        )
        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Aggregate analysis failed: {str(e)}")