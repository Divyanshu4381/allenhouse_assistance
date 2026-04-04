import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from app.data.college_data import COLLEGE_DATA

model = SentenceTransformer("all-MiniLM-L6-v2")

texts = [item["content"] for item in COLLEGE_DATA]
embeddings = model.encode(texts)

dimension = embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)
index.add(np.array(embeddings))


def search_vectors(query: str, k=3):
    query_vec = model.encode([query])
    distances, indices = index.search(np.array(query_vec), k)

    return [texts[i] for i in indices[0]]
