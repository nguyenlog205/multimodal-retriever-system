import os
import mimetypes
import magic  # pip install python-magic
from pathlib import Path


class MultimediaPreprocessor:
    IMAGE_EXT = [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff"]
    TEXT_EXT = [".txt", ".md", ".csv", ".json", ".xml"]
    AUDIO_EXT = [".wav", ".mp3", ".flac", ".ogg", ".m4a"]

    def __init__(self, use_magic=True):
        self.use_magic = use_magic

    def _detect_by_extension(self, file_path):
        ext = Path(file_path).suffix.lower()
        if ext in self.IMAGE_EXT:
            return "image"
        elif ext in self.TEXT_EXT:
            return "text"
        elif ext in self.AUDIO_EXT:
            return "audio"
        return "unknown"

    def _detect_by_mimetype(self, file_path):
        mime_type, _ = mimetypes.guess_type(file_path)
        if mime_type:
            if mime_type.startswith("image"):
                return "image"
            elif mime_type.startswith("text"):
                return "text"
            elif mime_type.startswith("audio"):
                return "audio"
        return "unknown"

    def _detect_by_content(self, file_path):
        mime_type = magic.from_file(file_path, mime=True)
        if mime_type.startswith("image"):
            return "image"
        elif mime_type.startswith("text"):
            return "text"
        elif mime_type.startswith("audio"):
            return "audio"
        return "unknown"

    def detect_file_type(self, file_path):
        """Kết hợp nhiều phương pháp để xác định loại file"""
        # 1. Extension
        result = self._detect_by_extension(file_path)
        if result != "unknown":
            return result

        # 2. MIME type
        result = self._detect_by_mimetype(file_path)
        if result != "unknown":
            return result

        # 3. Nội dung thực
        if self.use_magic:
            return self._detect_by_content(file_path)

        return "unknown"

    def preprocess(self, input_path):
        """
        Quét toàn bộ file trong input_path và phân loại
        Trả về dict: {"image": [...], "text": [...], "audio": [...], "unknown": [...]}
        """
        result = {"image": [], "text": [], "audio": [], "unknown": []}

        # Nếu là 1 file
        if os.path.isfile(input_path):
            file_type = self.detect_file_type(input_path)
            result[file_type].append(input_path)
            return result

        # Nếu là thư mục
        for root, _, files in os.walk(input_path):
            for file in files:
                file_path = os.path.join(root, file)
                file_type = self.detect_file_type(file_path)
                result[file_type].append(file_path)

        return result


# --- Demo ---
if __name__ == "__main__":
    pre = MultimediaPreprocessor()
    classified_files = pre.preprocess("data/")  # folder chứa nhiều loại file

    for t, flist in classified_files.items():
        print(f"{t.upper()} ({len(flist)} files):")
        for f in flist:
            print("  -", f)
