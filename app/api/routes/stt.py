from fastapi import APIRouter, UploadFile, File, HTTPException
from app.schemas.stt import TranscriptionResponse
from app.services.stt.transcriber import transcriber
from app.services.summary.service import summary_service
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