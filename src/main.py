import uuid
import datetime
from fastapi import FastAPI, HTTPException
from mangum import Mangum
from .utils import build_opensearch_query, get_dynamodb_table, get_opensearch_client
from .schemas import Book, CreateBook, SearchResult, SearchResponse

table = get_dynamodb_table()

app = FastAPI(
  title="Search API",
  description="Search API for OpenSearch",
  version="1.0.0"
)

@app.get("/books",response_model=SearchResult, summary="Search for a character", description="Search for a character by name")
async def search(keyword: str=None):
  try:
    client = get_opensearch_client()
    query = build_opensearch_query(keyword)
    result = client.search(index="japanese-folktales", body=query)
    hits = result["hits"]["total"]["value"]
    results = [
      SearchResponse(
        id=str(hit['_source']['id']),
        title=hit['_source']['title'],
        story=hit['_source']['story'],
        attributes=hit['_source']['attributes'],
        created_at=hit['_source']['created_at'],
        updated_at=hit['_source']['updated_at']
      )
      for hit in result["hits"]["hits"]
    ]

    return SearchResult(hits=hits, results=results)
  except Exception as e:
    raise HTTPException(status_code=500, detail=str(e))
  
@app.post("/books", response_model=Book)
async def create_book(book: CreateBook):
  try:
    now = datetime.datetime.now().isoformat()
    item = {
      "id": str(uuid.uuid4()),
      "title": book.title,
      "story": "",
      "attributes": [],
      "created_at": now,
      "updated_at": now
    }
    
    table.put_item(Item=item)
    return item

  except Exception as e:
    raise HTTPException(status_code=500, detail=str(e))
  
handler = Mangum(app)
