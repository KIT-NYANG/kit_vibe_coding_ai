from faster_whisper import WhisperModel
from app.core.config import settings
from app.services.stt.postprocess import normalize_segment_text, build_full_text


class Transcriber:
    def __init__(self) -> None:
        self.model = WhisperModel(
            settings.model_size,
            device=settings.device,
            compute_type=settings.compute_type,
        )

    def transcribe(self, file_path: str) -> dict:
        segments, info = self.model.transcribe(
            file_path,
            beam_size=settings.beam_size,
            vad_filter=True,
        )

        result_segments = []

        for idx, segment in enumerate(segments):
            text = normalize_segment_text(segment.text)

            result_segments.append({
                "index": idx,
                "start": float(segment.start),
                "end": float(segment.end),
                "text": text,
            })

        full_text = build_full_text(result_segments)

        return {
            "language": getattr(info, "language", None),
            "duration_sec": getattr(info, "duration", None),
            "full_text": full_text,
            "segments": result_segments,
        }


transcriber = Transcriber()