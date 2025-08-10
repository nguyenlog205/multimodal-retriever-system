## Prompt Processing with Natural Language Understanding
> *The **Prompt Processing** module serves as the first stage in the query-handling pipeline. Its main goal is to transform raw user input into a structured, machine-readable representation that can be effectively passed to downstream components (retrieval)*.

## Overview
The Prompt Processing module handles the first stage of the text-based pipeline:
- Accepts a raw user prompt (typed input).
- Preprocesses and normalizes the text for consistent handling.
- Applies Natural Language Understanding (NLU) techniques to extract semantic meaning.

## Core Function
### 1. Text Normalization

Converts input text into a standardized format by removing accents, converting to lowercase, replacing spaces with hyphens, and removing special characters. This ensures consistency for further processing.

Performed within `./function/normalize_prompt.py` Python script.

### 2. Knowledge Graph Construction
#### Definition and use
This phase is to transform the user’s natural language prompt into a structured, machine-readable representation that captures entities, attributes, and semantic relationships. This structured form enables the system to reason over the input, match it to relevant multimedia content, and bridge the gap between semanteme between diferrent types of media knowledge.

P/s: This approach is inspired from *Entity–Relationship Model*.
#### Top-level approach
1. Entiry recognition
2. Attitude labeling
3. Relationship extraction
4. Graph assembly

### 3. Semantemes Extraction

## REFERENCES
> [1] Prompt engineering: overview and guide, https://cloud.google.com/discover/what-is-prompt-engineering?hl=vi \
> [2] Knowledge Graph, https://www.ibm.com/think/topics/knowledge-graph \
> [3] PhoBERT Named Entity Reconigtion, https://github.com/Avi197/Phobert-Named-Entity-Reconigtion