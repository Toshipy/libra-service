from opensearchpy import OpenSearch, RequestsHttpConnection
from requests_aws4auth import AWS4Auth
import os
import boto3

def get_opensearch_client():
    endpoint = os.environ.get('OPENSEARCH_ENDPOINT', '')
    host = endpoint.replace('https://', '').replace('http://', '')
    
    credentials = boto3.Session().get_credentials()
    region = os.environ.get('AWS_REGION', 'ap-northeast-1')
    
    auth = AWS4Auth(
        credentials.access_key,
        credentials.secret_key,
        region,
        'es',
        session_token=credentials.token
    )
    
    return OpenSearch(
        hosts=[{'host': host, 'port': 443}],
        http_auth=auth,
        use_ssl=True,
        verify_certs=False,
        connection_class=RequestsHttpConnection
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
