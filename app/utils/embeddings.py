from sentence_transformers import SentenceTransformer
from app.data.devices import DEVICE_DOCUMENTS
model = SentenceTransformer('BAAI/bge-small-en-v1.5')
import numpy as np
def create_embeddings():
    embeddings = model.encode(DEVICE_DOCUMENTS,normalize_embeddings=True)
    return embeddings
embeddings = create_embeddings()
def dense_search(query:str,k=3)-> list[int]:
    query_emb=model.encode([query],normalize_embeddings=True)
    similarities=np.dot(query_emb,embeddings.T)[0]
    ranked_indices=similarities.argsort()[::-1]
    return ranked_indices[:k]

