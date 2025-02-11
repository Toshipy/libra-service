from pydantic import BaseModel
from typing import List

class SearchResponse(BaseModel):
    name: str
    story: str
    attributes: List[str]

class SearchResult(BaseModel):
    hits: int
    results: List[SearchResponse]
