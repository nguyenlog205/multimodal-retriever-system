import torch
from transformers import AutoModel, AutoTokenizer
from pyvi import ViTokenizer

# Load the pre-trained PhoBERT model and tokenizer globally or pass them as arguments
# Loading them once saves time if you process many texts.
phobert_model = AutoModel.from_pretrained("vinai/phobert-base")
phobert_tokenizer = AutoTokenizer.from_pretrained("vinai/phobert-base")

def get_phobert_sentence_embedding(text: str) -> torch.Tensor:
    """
    Generates a sentence embedding for a given Vietnamese text using PhoBERT.

    Args:
        text (str): The input Vietnamese text string.

    Returns:
        torch.Tensor: A tensor representing the sentence embedding (from the [CLS] token).
                      The shape will be [1, hidden_size], typically [1, 768].
    """
    # Step 1: Word-segment the text using ViTokenizer
    # PhoBERT models are trained on word-segmented Vietnamese text.
    segmented_text = ViTokenizer.tokenize(text)

    # Step 2: Tokenize the segmented text using PhoBERT's tokenizer
    # `return_tensors="pt"` ensures the output is a PyTorch tensor.
    # The `encode` method handles adding special tokens like [CLS] and [SEP].
    input_ids = phobert_tokenizer.encode(segmented_text, return_tensors="pt")

    # Step 3: Extract embeddings from the PhoBERT model
    # `torch.no_grad()` disables gradient calculation, which is good practice
    # when you're only performing inference and not training, saving memory.
    with torch.no_grad():
        outputs = phobert_model(input_ids)

    # PhoBERT (like BERT) outputs a tuple. The first element (outputs[0])
    # is the last layer's hidden states for all tokens.
    # Its shape is (batch_size, sequence_length, hidden_size).
    last_hidden_states = outputs[0]

    # Step 4: Extract the sentence embedding from the [CLS] token
    # The embedding of the [CLS] token (the first token, index 0)
    # is commonly used as the sentence representation in BERT-like models.
    sentence_embedding = last_hidden_states[:, 0, :]

    return sentence_embedding

# --- Example Usage ---
if __name__ == "__main__":
    example_text_1 = "Chào bạn, hôm nay bạn thế nào?"
    embedding_1 = get_phobert_sentence_embedding(example_text_1)
    print(f"Text 1: '{example_text_1}'")
    print(f"Embedding 1 Shape: {embedding_1.shape}")
    print(f"Embedding 1 (first 5 dimensions): {embedding_1[0, :5]}\n")