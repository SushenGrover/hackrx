# utils/faiss_index.py
import faiss
import numpy as np

def build_faiss_index(embeddings):
    dim = len(embeddings[0])
    index = faiss.IndexFlatL2(dim)
    index.add(np.array(embeddings).astype('float32'))
    return index

def search_faiss_index(index, query_embedding, k=15):
    D, I = index.search(np.array([query_embedding]).astype('float32'), k)
    return I[0]
