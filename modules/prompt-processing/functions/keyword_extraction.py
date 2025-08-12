from google import genai

template = """
  Bạn là một hệ thống trích xuất thông tin tự động, chuyên phân tích mô tả và tạo ra đối tượng JSON chứa các thuộc tính liên quan.

  Yêu cầu:
  1. Phân tích mô tả: Đọc và hiểu ý nghĩa của một đoạn văn bản được cung cấp.
  2. Trích xuất các thuộc tính chính: Xác định và trích xuất các thông tin quan trọng nhất, như:
    - type: Loại nội dung (ví dụ: `text`, `image`, `audio`, `video`). Trường này là **bắt buộc**.
    - activity: Hoạt động diễn ra (ví dụ: `nấu ăn`, `chụp ảnh`, `đi chơi`).
    - location: Địa điểm cụ thể (ví dụ: `công viên Yên Sở`, `Đà Lạt`, `Việt Nam`).
    - event: Sự kiện cụ thể (ví dụ: `buổi sinh nhật`, `lễ cưới`).
    - date: Thời gian (năm-tháng-ngày, năm-tháng hoặc chỉ năm).
    - people: Những người được nhắc đến (ví dụ: `tôi`, `bạn bè`, `gia đình`).
    - emotion: Cảm xúc chủ đạo (ví dụ: `vui vẻ`, `buồn bã`).
    - device: Thiết bị được sử dụng (ví dụ: `điện thoại`, `máy ảnh`).
    - weather: Thời tiết (ví dụ: `nắng`, `mưa`).
    - object: Các đối tượng chính (ví dụ: `hoa anh đào`, `bánh kem`).
  3. Định dạng đầu ra:
    - Trả về một đối tượng JSON hợp lệ.
    - Các trường trong JSON phải sử dụng các **từ khóa chính xác** từ mô tả gốc.
    - **Tuyệt đối không** bao gồm bất kỳ giải thích, đoạn văn bản phụ hay dấu định dạng nào khác ngoài JSON.
    - Bỏ qua định dạng ```json``` trong câu trả lời, chỉ cần trả về đối tượng JSON thuần túy.

  Ví dụ 1:
  Input: "Ảnh chụp hoa anh đào tại công viên Yên Sở tháng 3 năm 2021, với tôi và bạn bè"
  Output:
  {
    "type": "image",
    "activity": "chụp hoa anh đào",
    "location": "công viên Yên Sở",
    "date": "2021-03",
    "people": ["tôi", "bạn bè"]
  }

  Ví dụ 2:
  Input: "Video buổi sinh nhật vui vẻ của tôi, quay bằng điện thoại vào tháng 10 năm 2023, trời nắng"
  Output:
  {
    "type": "video",
    "event": "buổi sinh nhật",
    "emotion": "vui vẻ",
    "people": ["tôi"],
    "device": "điện thoại",
    "date": "2023-10",
    "weather": "nắng"
  }

"""

def extract_keywords(text: str) -> list:
  """
  Extracts keywords from the input text using Google's Gemini model.
  Args:
    text (str): The input text from which to extract keywords.
  Returns:
    list: A list of extracted keywords.
  """

  client = genai.Client(api_key='AIzaSyCsWZjclPxavDFcwdZEPz1HJad9u9pzdSk')

  task = f'Input: {text}\nOutput:'
  
  few_shot_prompt = template + task

  response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=few_shot_prompt
  )

  # print("Response:", response.text)
  return response.text