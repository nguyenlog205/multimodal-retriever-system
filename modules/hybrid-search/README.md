# Hybrid Search module with processed input
> This module is to perform retrieval tasks, from a processed input to conduct hybrid search, which is a combination of keyword-based search and semantic-based search. 

## Top-level approach
### 1. I/O
#### Input
This module requires the following input, which is processed and returned by **prompt-processing** module (`./modules/prompt-processing/prompt-processing.py`).

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
```
#### Output
This returns a list of top-k best results (k is defaultly defined as 5). Particularly, the retrieval module returns their relevant **file path** and **ranking score** relying on Reciprocal Rank Fusion (RRF) approach. For more information, read APPENDIX A. For example:
| Rank | File Path | RRF Score |
| :--- | :--- | :--- |
| 1 | `/picture/203012.png` | 0.85 |
| 2 | `/picture/203004.png` | 0.72 |
| 3 | `/picture/203013.png` | 0.65 |
| 4 | `/picture/203005.png` | 0.58 |
| 5 | `/picture/203007.png` | 0.51 |

### 2. Main tasks for module



## APPENDIX
### APPENDIX A - RECIPROCAL RANK FUSION (RRF)
Reciprocal Rank Fusion (RRF) is a popular and effective method for combining result lists from multiple sources (e.g., keyword search and semantic search) without needing to normalize the initial scores.

It works by assigning a score to each document based on its rank in each result list. The core idea is that a document's position (rank) is more important than its raw score, and a document that consistently appears at a high rank across multiple lists is likely highly relevant.

The RRF score for a document ($d$) is calculated using the following formula:

$$\text{RRF}\_{}\text{score}(d) = \sum_{r \in R}{\frac{1}{k + \text{rank}_{r}{d}}}$$

**Where**:
- $R$ is the set of all result lists being combined.
- $\text{rank}_{r}{(d)}$ is the rank of document d in result list r. Ranks typically start at 1.
- $k$ is an adjustable constant, often set to 60. This constant prevents documents with extremely high ranks from dominating the final score and ensures that documents not present in a particular list still receive a small, non-zero "score."

After calculating the RRF score for all documents from all lists, the system sorts them in descending order to create a final, unified result list.

