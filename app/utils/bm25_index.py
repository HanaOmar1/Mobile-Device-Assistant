
from rank_bm25 import BM25Okapi
from app.data.devices import DEVICE_DOCUMENTS
def create_bm25_index():
    #tokenize using lowe and whitespace
    documents=DEVICE_DOCUMENTS
    tokenized_documents = [doc.lower().split() for doc in documents]
    bm25 = BM25Okapi(tokenized_documents)
    return bm25
bm25 = create_bm25_index()

def search_bm25(query:str,k=3)-> list[str]:
    tokenized_query=query.lower().split()
    scores=bm25.get_scores(tokenized_query)
    ranked_indices = sorted(
        range(len(scores)),
        key=lambda i: scores[i],
        reverse=True
    )
    return ranked_indices[:k]