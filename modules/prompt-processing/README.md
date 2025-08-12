## Prompt Processing with Hybrid Search  
> *The **Prompt Processing** module is the entry point of the retrieval pipeline. It converts raw user input into a structured and enriched representation that supports both **vector-based semantic search** and **attribute-based filtering** for hybrid search.*


## Overview
The Prompt Processing module orchestrates three main steps:
1. Accept raw user prompt (text input).
2. Normalize and preprocess it for consistent handling.
3. Extract both semantic meaning and explicit attributes to support **hybrid retrieval**.

## Core Functions

### 1. Text Standardization
Standardizes the input text by:
- Removing accents
- Converting to lowercase
- Trimming extra spaces
- Removing special characters

**Purpose:** Ensures uniformity before semantic embedding and attribute extraction.

**Implementation:** `./function/text_normalization.py`

### 2. Keyword Extraction
Identifies explicit **metadata-like fields** from the prompt that can be used for filtering, such as:
- **Entities:** object, person, location, event
- **Attributes:** date, format, category, tags
- **Keywords:** domain-specific terms

These attributes are later applied as structured filters in the **attribute-based search** step of hybrid retrieval.

**Implementation:** `./function/keyword_extraction.py`


### 3. Semantic Embedding Vector Extraction
Transforms the normalized prompt into a high-dimensional vector representation to capture:
- Contextual meaning
- Synonym relationships
- Implicit intent

**Purpose:** Enables **semantic search** against multimedia embeddings (video, image, text).

**Implementation:** `./function/embedding_vector_extraction.py`




## Example Flow
**Prompt:**  
> "Ảnh chụp Lăng Bác vào tháng 5 năm 2023, có trời nắng và đám đông"

**After Processing:**
```json
{
  "normalized_text": "Ảnh chụp Lăng Bác vào tháng 5 năm 2023, có trời nắng và đám đông",
  "keywords": {
    "type": "image",
    "activity": "chụp Lăng Bác",
    "location": "Lăng Bác",
    "date": "2023-05",
    "weather": "nắng",
    "people": ["đám đông"]
  },
  "embedding_vector": [0.012, -0.543, ...]
}
