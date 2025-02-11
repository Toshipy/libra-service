from fastapi import FastAPI, HTTPException
from opensearchpy import OpenSearch
from mangum import Mangum
import os
from schemas import SearchResult, SearchResponse
app = FastAPI(
  title="Search API",
  description="Search API for OpenSearch",
  version="1.0.0"
)

def get_opensearch_client():
  return OpenSearch(
    hosts=[os.environ.get('OPENSEARCH_ENDPOINT', '')],    
    # http_auth=(os.getenv("OPENSEARCH_USERNAME"), os.getenv("OPENSEARCH_PASSWORD")),
    http_compress=True,
    use_ssl=True,
    # scheme="https",
    verify_certs=False
  )

@app.get("/search",response_model=SearchResult, summary="Search for a character", description="Search for a character by name")
async def search(keyword: str=None):
  try:
    client = get_opensearch_client()

    query = {
      "query": {
        "multi_match": {
          "query": keyword,
          "fields": ["name", "story", "attributes"]
        }
      }
    }

    result = client.search(index="japanese-folktalesaa", body=query)

    hits = result["hits"]["total"]["value"]

    results = [
      SearchResponse(
        name=hit['_source']['name'],
        story=hit['_source']['story'],
        attributes=hit['_source']['attributes']
      )
      for hit in result["hits"]["hits"]
    ]

    return SearchResult(hits=hits, results=results)
  except Exception as e:
    raise HTTPException(status_code=500, detail=str(e))

handler = Mangum(app)
