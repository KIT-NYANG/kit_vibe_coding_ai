# schemas/summary.py - 최종 API 응답 형식 정의

from pydantic import BaseModel, Field
from typing import List


class SummarizeResponse(BaseModel):
    summary_text: str
    keywords: List[str] = Field(default_factory=list)