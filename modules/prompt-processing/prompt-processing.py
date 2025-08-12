from functions import text_normalization, embedding_vector_extraction, keyword_extraction
import time

def process_prompt(prompt: str) -> dict:
    """
    Processes the input prompt to extract keywords and generate embeddings.

    Args:
        prompt (str): The input text prompt to process.

    Returns:
        dict: A dictionary containing normalized text, keyword extraction results,
              and embedding vectors.
    """
    # Normalize the input text
    normalized_text = text_normalization.normalize_text(prompt)

    # Extract keywords using the keyword extraction function
    keywords = keyword_extraction.extract_keywords(normalized_text)

    # Generate embedding vector for the normalized text
    embedding_vector = embedding_vector_extraction.get_phobert_sentence_embedding(normalized_text)

    return {
        "normalized_text": normalized_text,
        "keywords": keywords,
        "embedding_vector": embedding_vector
    }

if __name__ == "__main__":
    sample_prompt = "Ảnh chụp Lăng Bác vào tháng 5 năm 2023, có trời nắng và đám đông"
    
    # Ghi lại thời gian bắt đầu
    start_time = time.time()
    
    # Gọi hàm cần đo thời gian
    result = process_prompt(sample_prompt)
    

    
    print("Normalized Text:", result["normalized_text"])
    print("Keywords:", result["keywords"])
    print("Embedding Vector (first 5 dimensions):", result["embedding_vector"][0, :5])
    
        # Ghi lại thời gian kết thúc
    end_time = time.time()
    
    # Tính toán thời gian đã trôi qua
    elapsed_time = end_time - start_time
    # In ra thời gian chạy
    print(f"Thời gian chạy: {elapsed_time:.4f} giây")