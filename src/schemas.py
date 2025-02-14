from pydantic import BaseModel
from typing import List

class SearchResponse(BaseModel):
    id: str
    title: str
    story: str
    attributes: List[str]
    created_at: str
    updated_at: str

class SearchResult(BaseModel):
    hits: int
    results: List[SearchResponse]
    
class CreateBook(BaseModel):
    title: str
    story: str
    attributes: List[str]

class Book(BaseModel):
    id: str
    title: str
    story: str
    attributes: List[str]
    created_at: str
    updated_at: str
