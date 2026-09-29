from pydantic import BaseModel, Field
from typing import Dict, Literal, List

class Device(BaseModel):
    brand:str=Field(..., description="Brand of the device")
    model:str=Field(..., description="Model of the device")
    specs:Dict[str,str]=Field(..., description="Specifications of the device")
    release_year:int=Field(..., description="Release year of the device")
    price_tier:Literal["budget", "mid-range", "flagship"]
class ExtractRequest(BaseModel):
    text:str=Field(..., description="Input for specification extraction")
class ExtractResponse(BaseModel):
    brand:str=Field(..., description="Brand of the device")
    model:str=Field(..., description="Model of the device")
    specs:Dict[str,str]=Field(..., description="Specifications of the device")
    release_year:int=Field(..., description="Release year of the device")
    price_tier:Literal["budget", "mid-range", "flagship"]
class SearchRequest(BaseModel):
    q:str=Field(..., description="Search query")
class SearchResult(BaseModel):
    document:str=Field(..., description="Search result document")
    score:float=Field(..., description="Search result score")
class SearchResponse(BaseModel):
    results: List[SearchResult]=Field(..., description="List of search results")