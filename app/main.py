from fastapi import FastAPI, HTTPException
from app.schema.device import ExtractRequest, ExtractResponse, SearchRequest, SearchResponse, SearchResult
from app.services.search import hybrid_search
from app.services.extraction import extract_device, is_suspicious

app = FastAPI(title="Mobile Device Assistant")

@app.post("/extract")
async def extract(request: ExtractRequest):
    if len(request.text)>500:
        raise HTTPException(400,"Request is longer than 500 Characters")
    if is_suspicious(request.text):
        raise HTTPException(400,"Text has suspicious words")
    device= extract_device(request.text)
    response=ExtractResponse(
        brand=device.brand,
        model=device.model,
        specs=device.specs,
        release_year=device.release_year,
        price_tier=device.price_tier
    )
    return response
@app.post("/search")
async def search(request: SearchRequest):
    if len(request.q)>500:
        raise HTTPException(400,"Request is longer than 500 Characters")
    results=hybrid_search(request.q)
    SearchRes = [
    SearchResult(document=doc, score=score)
    for doc, score in results
    ]
    response=SearchResponse(results=SearchRes)
    return response

