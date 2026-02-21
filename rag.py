import os
import re
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# Load embedding model (small & fast)
model = SentenceTransformer("all-MiniLM-L6-v2")

DATA_PATH = "notes.txt"

# Load and chunk notes
def load_chunks():
    if not os.path.exists(DATA_PATH):
        return []
    
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        text = f.read()

    # Split into chunks (400–700 chars)
    chunks = re.split(r'\n\n+', text)
    chunks = [c.strip() for c in chunks if len(c.strip()) > 30]
    return chunks

CHUNKS = load_chunks()
if CHUNKS:
    EMBEDDINGS = model.encode(CHUNKS)
else:
    EMBEDDINGS = []
    

def retrieve_relevant(query, top_k=3):
    """Returns top-k most relevant chunks to the query."""
    if not CHUNKS:
        return ""

    q_emb = model.encode([query])
    scores = cosine_similarity(q_emb, EMBEDDINGS)[0]

    top_idx = scores.argsort()[-top_k:][::-1]
    retrieved = "\n\n".join(CHUNKS[i] for i in top_idx)

    return retrieved
