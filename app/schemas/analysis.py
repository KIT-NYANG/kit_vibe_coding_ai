from pydantic import BaseModel, Field
from typing import List, Optional


class QuizItemResponse(BaseModel):
    quizInsertTimeSec: int
    question: str
    answer: str
    explanation: str
    supplementalDescription: str


class TeacherGuideResponse(BaseModel):
    predictedDifficultSection: str
    predictedReason: str
    improvementSuggestion: str


class PreAnalysisResponse(BaseModel):
    quizzes: List[QuizItemResponse] = Field(default_factory=list)
    teacherGuides: List[TeacherGuideResponse] = Field(default_factory=list)


class CandidateRange(BaseModel):
    startSec: int
    endSec: int
    pauseCount: int = 0
    seekBackCount: int = 0
    affectedUserCount: int = 0
    score: float = 0.0
    reasons: List[str] = Field(default_factory=list)


class SegmentResponse(BaseModel):
    index: int
    start: float
    end: float
    text: str


class AggregateAnalysisRequest(BaseModel):
    lectureId: int
    candidateRanges: List[CandidateRange]
    segments: List[SegmentResponse] = Field(default_factory=list)
    additionalPrompt: Optional[str] = None


class AggregateAnalysisResponse(BaseModel):
    lectureId: int
    quizzes: List[QuizItemResponse] = Field(default_factory=list)
    teacherGuides: List[TeacherGuideResponse] = Field(default_factory=list)