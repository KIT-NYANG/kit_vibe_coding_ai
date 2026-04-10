from fastapi import APIRouter, HTTPException
from app.schemas.analysis import AggregateAnalysisRequest, AggregateAnalysisResponse
from app.services.analysis.service import analysis_service

router = APIRouter(prefix="/api/analysis", tags=["analysis"])


@router.post("/aggregate", response_model=AggregateAnalysisResponse)
async def aggregate_analysis(request: AggregateAnalysisRequest) -> AggregateAnalysisResponse:
    try:
        result = analysis_service.analyze_aggregate(
            candidate_ranges=request.candidateRanges,
            segments=request.segments
        )
        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Aggregate analysis failed: {str(e)}")