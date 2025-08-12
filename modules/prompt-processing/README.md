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

**Implementation:** `./function/normalize_prompt.py`

### 2. Feature Extraction
Identifies explicit **metadata-like fields** from the prompt that can be used for filtering, such as:
- **Entities:** object, person, location, event
- **Attributes:** date, format, category, tags
- **Keywords:** domain-specific terms

These attributes are later applied as structured filters in the **attribute-based search** step of hybrid retrieval.


### 3. Semantic Embedding Vector Extraction
Transforms the normalized prompt into a high-dimensional vector representation to capture:
- Contextual meaning
- Synonym relationships
- Implicit intent

**Purpose:** Enables **semantic search** against multimedia embeddings (video, image, text).


### 4. Hybrid Search Integration
The extracted outputs are passed to the retrieval engine in two channels:
- **Semantic Search:** Uses embeddings for similarity scoring.
- **Attribute-Based Filtering:** Uses extracted attributes for precise filtering.

**Flow Example:**
1. Prompt → Normalization  
2. Prompt → Attribute Extraction → Filter query  
3. Prompt → Embedding → Vector similarity search  
4. Combine results (scoring fusion)

---

## Example Flow
**Prompt:**  
> "Video tôi nấu ăn ở nhà bếp, tháng 7 năm 2023"

**After Processing:**
```json
{
  "normalized_prompt": "video toi nau an o nha bep thang 7 nam 2023",
  "attributes": {
    "type": "video",
    "activity": "nấu ăn",
    "location": "nhà bếp",
    "date": "2023-07"
  },
  "embedding": [0.012, -0.543, ...]
}
