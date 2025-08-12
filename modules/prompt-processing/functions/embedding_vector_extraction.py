import torch
from transformers import AutoModel, AutoTokenizer
from pyvi import ViTokenizer
import logging
import sys

# --- Cấu hình Logging ---
# Thiết lập logger để ghi log ra console và file
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        # Bạn có thể thêm FileHandler nếu muốn ghi log ra file
        # logging.FileHandler("app.log"),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)
# -------------------------

# --- Tải mô hình và tokenizer ---
# Đảm bảo tải mô hình và tokenizer chỉ một lần duy nhất
try:
    logger.info("Đang tải mô hình và tokenizer PhoBERT...")
    phobert_model = AutoModel.from_pretrained("vinai/phobert-base")
    phobert_tokenizer = AutoTokenizer.from_pretrained("vinai/phobert-base")
    phobert_model.eval() # Chuyển sang chế độ đánh giá để tắt dropout
    logger.info("Đã tải mô hình và tokenizer PhoBERT thành công.")
except Exception as e:
    logger.error(f"Lỗi khi tải mô hình hoặc tokenizer: {e}")
    phobert_model = None
    phobert_tokenizer = None
# ---------------------------------

def get_phobert_sentence_embedding(text: str) -> torch.Tensor:
    """
    Generates a sentence embedding for a given Vietnamese text using PhoBERT.

    Args:
        text (str): The input Vietnamese text string.

    Returns:
        torch.Tensor: A tensor representing the sentence embedding (from the [CLS] token).
                      The shape will be [1, hidden_size], typically [1, 768].
    """
    if phobert_model is None or phobert_tokenizer is None:
        logger.warning("Mô hình PhoBERT chưa được tải. Không thể tạo embedding.")
        return torch.empty(0) # Trả về tensor rỗng nếu mô hình không tồn tại

    logger.info(f"Đang tạo embedding cho văn bản: '{text}'")

    try:
        # Bước 1: Word-segment the text using ViTokenizer
        segmented_text = ViTokenizer.tokenize(text)
        logger.info(f"Văn bản đã được tách từ: '{segmented_text}'")

        # Bước 2: Tokenize the segmented text using PhoBERT's tokenizer
        input_ids = phobert_tokenizer.encode(segmented_text, return_tensors="pt")
        
        # Bước 3: Extract embeddings from the PhoBERT model
        with torch.no_grad():
            outputs = phobert_model(input_ids)

        last_hidden_states = outputs[0]

        # Bước 4: Extract the sentence embedding from the [CLS] token
        sentence_embedding = last_hidden_states[:, 0, :]
        logger.info("Đã tạo embedding thành công.")
        
        return sentence_embedding
    except Exception as e:
        logger.error(f"Lỗi trong quá trình tạo embedding: {e}")
        return torch.empty(0)


# --- Ví dụ sử dụng ---
if __name__ == "__main__":
    example_text_1 = "Chào bạn, hôm nay bạn thế nào?"
    embedding_1 = get_phobert_sentence_embedding(example_text_1)
    
    if embedding_1.numel() > 0:
        print(f"\nText 1: '{example_text_1}'")
        print(f"Embedding 1 Shape: {embedding_1.shape}")
        print(f"Embedding 1 (first 5 dimensions): {embedding_1[0, :5]}\n")
    else:
        print("\nKhông thể tạo embedding cho văn bản 1.")

    example_text_2 = "Đây là một ví dụ khác."
    embedding_2 = get_phobert_sentence_embedding(example_text_2)
    
    if embedding_2.numel() > 0:
        print(f"\nText 2: '{example_text_2}'")
        print(f"Embedding 2 Shape: {embedding_2.shape}")
        print(f"Embedding 2 (first 5 dimensions): {embedding_2[0, :5]}\n")
    else:
        print("\nKhông thể tạo embedding cho văn bản 2.")