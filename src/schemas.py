from pydantic import BaseModel
from typing import List

class SearchResponse(BaseModel):
    id: int
    title: str
    story: str
    attributes: List[str]
    created_at: str
    updated_at: str

class SearchResult(BaseModel):
    hits: int
    results: List[SearchResponse]

class Book(BaseModel):
    id: int
    title: str
    story: str
    attributes: List[str]
    created_at: str
    updated_at: str
