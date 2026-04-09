# core/llm.py - LLM 모델 설정

#from langchain_openai import ChatOpenAI
from langchain_groq import ChatGroq
from app.core.config import settings


def get_summary_llm() -> ChatGroq:
    return ChatGroq(
        model=settings.summary_model,
        api_key=settings.openai_api_key,
        temperature=0.2,
    )
def get_llm() -> ChatGroq:
    return ChatGroq(
        model=settings.llm_model,
        api_key=settings.groq_api_key,
        temperature=settings.llm_temperature,
    )

