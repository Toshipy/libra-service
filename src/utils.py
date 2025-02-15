from opensearchpy import OpenSearch
import os
import boto3

def get_opensearch_client():
  return OpenSearch(
    hosts=[os.environ.get('OPENSEARCH_ENDPOINT', '')],    
    # http_auth=(os.getenv("OPENSEARCH_USERNAME"), os.getenv("OPENSEARCH_PASSWORD")),
    http_compress=True,
    use_ssl=True,
    # scheme="https",
    verify_certs=False
  )

def get_dynamodb_table():
  return boto3.resource('dynamodb').Table('Books')

OPENSEARCH_INDEX = 'japanese-folktales'

OPENSEARCH_MAPPING = {
  "mappings": {
    "properties": {
      "id": {"type": "keyword"},
      "title": {"type": "text"},
      "story": {"type": "text"},
      "attributes": {"type": "keyword"},
      "created_at": {"type": "date"},
      "updated_at": {"type": "date"}
    }
  }
}

def build_opensearch_query(keyword):
  return {
    "query": {
      "multi_match": {
        "query": keyword,
        "fields": ["title", "story"]
      }
    }
  }
