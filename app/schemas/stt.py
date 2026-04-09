from pydantic import BaseModel
from typing import List, Optional
from app.schemas.summary import SummarizeResponse


class SegmentResponse(BaseModel):
    index: int
    start: float
    end: float
    text: str


class TranscriptionResponse(BaseModel):
    language: Optional[str] = None
    duration_sec: Optional[float] = None
    full_text: str
    segments: List[SegmentResponse]
    summarize: Optional[SummarizeResponse] = None #stt 요약