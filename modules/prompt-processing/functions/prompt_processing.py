import re
import unicodedata

def normalize_prompt(text: str) -> str:
    """
    Chuẩn hóa prompt để xử lý NLP.
    
    Các bước:
    - Chuẩn hóa Unicode (NFC)
    - Loại bỏ khoảng trắng thừa
    - Thay thế nhiều dấu cách liên tiếp bằng 1 dấu cách
    - Cắt khoảng trắng đầu và cuối
    """
    if not isinstance(text, str):
        raise ValueError("Input must be a string")

    # Chuẩn hóa Unicode
    text = unicodedata.normalize("NFC", text)

    # Loại bỏ khoảng trắng thừa xung quanh dấu câu
    text = re.sub(r"\s+([.,!?;:])", r"\1", text)

    # Thay nhiều khoảng trắng bằng 1
    text = re.sub(r"\s+", " ", text)

    # Loại bỏ khoảng trắng đầu và cuối
    text = text.strip()

    return text


sample = "   Xin   chào   ,   tôi   là   Long   Đạt đạt "
print(normalize_prompt(sample))