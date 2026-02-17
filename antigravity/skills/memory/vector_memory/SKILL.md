---
name: vector-memory
description: Provides long-term semantic memory storage and retrieval using ChromaDB and Sentence Transformers. Use this to store user preferences, facts, and conversation context that needs to persist across sessions.
---

# Vector Memory Skill

## Purpose
To provide the agent with Long-Term Memory (LTM) capabilities. It allows the system to store text with semantic meaning and retrieve it later based on relevance, not just keyword matching.

## Usage

### 1. Storing Memory
Add a new memory to the database.
```python
add_memory(text="User prefers dark mode.", metadata={"category": "preference"})
```

### 2. Retrieving Context
Find memories relevant to a query.
```python
results = query_memory(query="What UI style does the user like?", n_results=3)
```

### 3. Clearing Memory
Reset the memory store (Caution!).
```python
clear_memory()
```

## Technical Implementation
- **Database**: ChromaDB (Embedded)
- **Embedding Model**: `all-MiniLM-L6-v2` (via Sentence Transformers)
- **Storage Path**: `./antigravity/data/chroma_db`

## Dependencies
- `chromadb`
- `sentence-transformers`
