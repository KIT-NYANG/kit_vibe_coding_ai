from typing import List, Dict


def normalize_segment_text(text: str) -> str:
    return " ".join(text.strip().split())


def build_full_text(segments: List[Dict]) -> str:
    texts = [segment["text"] for segment in segments if segment["text"]]
    return " ".join(texts)