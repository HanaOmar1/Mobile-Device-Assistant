from app.utils.bm25_index import search_bm25
from app.utils.embeddings import dense_search
from app.data.devices import DEVICE_DOCUMENTS
def hybrid_search(query: str, k: int = 3):
    bm25_results = search_bm25(query, k)
    dense_results = dense_search(query, k)
    rrf_scores = {}

    for rank, doc_index in enumerate(bm25_results, start=1):
        rrf_scores[doc_index] = 1 / (60 + rank)

    for rank, doc_index in enumerate(dense_results, start=1):
        if doc_index in rrf_scores:
            rrf_scores[doc_index] += 1 / (60 + rank)
        else:
            rrf_scores[doc_index] = 1 / (60 + rank)

    ranked_results = sorted(rrf_scores.items(),key=lambda x: x[1],reverse=True)[:k]

    return[
            (DEVICE_DOCUMENTS[doc_index], score)
            for doc_index, score in ranked_results]    