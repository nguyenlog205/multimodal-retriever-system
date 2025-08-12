import uuid
from pathlib import Path

IMG_EXT = {".jpg",".jpeg",".png",".bmp",".tiff",".webp"}
AUDIO_EXT = {".wav",".mp3",".flac",".m4a",".aac",".ogg"}
VIDEO_EXT = {".mp4",".mov",".avi",".mkv",".webm"}
TEXT_EXT = {".txt",".md",".json",".csv"}


def new_id(prefix: str = "m") -> str:
    """Return a short unique id string with prefix."""
    return f"{prefix}_{uuid.uuid4().hex}"


def classify_file(path: Path) -> str:
    """Return one of: 'image','audio','video','text','other' based on file extension."""
    ext = path.suffix.lower()
    if ext in IMG_EXT:
        return "image"
    if ext in AUDIO_EXT:
        return "audio"
    if ext in VIDEO_EXT:
        return "video"
    if ext in TEXT_EXT:
        return "text"
    return "other"