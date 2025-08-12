# prompt-processing.py
import os
import time
import json
import logging
from functions import text_normalization, embedding_vector_extraction, keyword_extraction

# --- Logging Configuration ---
# Create the logging directory if it doesn't exist
log_dir = "logging"
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(os.path.join(log_dir, "app.log")),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def process_prompt(prompt: str) -> dict:
    """
    Processes the input prompt to extract keywords and generate embeddings.

    Args:
        prompt (str): The input text prompt to process.

    Returns:
        dict: A dictionary containing normalized text, keyword extraction results,
              and embedding vectors.
    """
    logger.info(f"Bắt đầu xử lý prompt: '{prompt}'")
    
    # Normalize the input text
    normalized_text = text_normalization.normalize_text(prompt)
    logger.info(f"Đã chuẩn hóa văn bản: '{normalized_text}'")

    # Extract keywords using the keyword extraction function
    try:
        keywords = keyword_extraction.extract_keywords(normalized_text)
        logger.info(f"Đã trích xuất từ khóa thành công: {keywords}")
    except Exception as e:
        logger.error(f"Lỗi khi trích xuất từ khóa: {e}")
        keywords = None

    # Generate embedding vector for the normalized text
    try:
        embedding_vector = embedding_vector_extraction.get_phobert_sentence_embedding(normalized_text)
        logger.info("Đã tạo embedding vector thành công.")
    except Exception as e:
        logger.error(f"Lỗi khi tạo embedding vector: {e}")
        embedding_vector = None

    return {
        "normalized_text": normalized_text,
        "keywords": keywords,
        "embedding_vector": embedding_vector
    }

if __name__ == "__main__":
    sample_prompt = "Ảnh chụp Lăng Bác vào tháng 5 năm 2023, có trời nắng và đám đông"
    
    start_time = time.time()
    
    result = process_prompt(sample_prompt)
    
    end_time = time.time()
    elapsed_time = end_time - start_time
    
    logger.info("--- Kết quả xử lý ---")
    logger.info(f"Văn bản chuẩn hóa: {result.get('normalized_text')}")
    logger.info(f"Từ khóa: {result.get('keywords')}")
    
    embedding_info = "Không thể tạo embedding"
    if result.get('embedding_vector') is not None and result.get('embedding_vector').numel() > 0:
        embedding_info = f"Vector Embedding (5 chiều đầu tiên): {result['embedding_vector'][0, :5]}"
    logger.info(embedding_info)
    
    logger.info(f"Thời gian chạy: {elapsed_time:.4f} giây")