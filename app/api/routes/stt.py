from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from app.schemas.stt import TranscriptionResponse
from app.schemas.analysis import PreAnalysisResponse
from app.services.stt.transcriber import transcriber
from app.services.summary.service import summary_service
from app.services.analysis.service import analysis_service
from app.utils.file import save_upload_file_to_temp, remove_file_safely


router = APIRouter(prefix="/api/stt", tags=["stt"])


@router.post("/transcribe", response_model=TranscriptionResponse)
async def transcribe_video(file: UploadFile = File(...)) -> TranscriptionResponse:
    temp_path = None

    try:
        temp_path = await save_upload_file_to_temp(file)
        result = transcriber.transcribe(temp_path)

        summary_result = summary_service.summarize_lecture(result["full_text"])
        result["summarize"] = summary_result.model_dump()

        return TranscriptionResponse(**result)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"STT failed: {str(e)}")

    finally:
        if temp_path:
            remove_file_safely(temp_path)


@router.post("/transcribe-and-pre-analyze")
async def transcribe_and_pre_analyze(
    file: UploadFile = File(...)
):
    temp_path = None

    try:
        temp_path = await save_upload_file_to_temp(file)
        result = transcriber.transcribe(temp_path)

        summary_result = summary_service.summarize_lecture(result["full_text"])
        pre_result = analysis_service.analyze_pre(
            segments=result["segments"],
        )

        return {
            "language": result.get("language"),
            "duration_sec": result.get("duration_sec"),
            "full_text": result.get("full_text"),
            "segments": result.get("segments", []),
            "summarize": summary_result.model_dump(),
            "pre_analysis": pre_result.model_dump(),
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"STT + pre analysis failed: {str(e)}")

    finally:
        if temp_path:
            remove_file_safely(temp_path)