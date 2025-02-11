import os
from opensearchpy import OpenSearch

def get_client():
    # 環境変数からエンドポイントを取得
    opensearch_endpoint = os.environ.get('OPENSEARCH_ENDPOINT', '')
    
    # OpenSearchクライアントを設定
    client = OpenSearch(
        hosts=[opensearch_endpoint],
        http_compress=True,
        use_ssl=True,      # AWS環境では通常SSL必須
        verify_certs=True,
        ssl_show_warn=False,
    )
    return client

def create_index_if_not_exists(client, index_name):
    if not client.indices.exists(index=index_name):
        index_settings = {
            "settings": {
                "analysis": {
                    "analyzer": {
                        "kuromoji": {
                            "type": "kuromoji"
                        }
                    }
                }
            },
            "mappings": {
                "properties": {
                    "name": {"type": "text", "analyzer": "kuromoji"},
                    "story": {"type": "text", "analyzer": "kuromoji"},
                    "attributes": {"type": "text", "analyzer": "kuromoji"}
                }
            }
        }
        client.indices.create(index=index_name, body=index_settings)

def lambda_handler(event, context):
    try:
        # OpenSearchクライアントを初期化
        client = get_client()
        
        # インデックス名を設定
        index_name = "japanese-folktales"
        
        # インデックスが存在しない場合は作成
        create_index_if_not_exists(client, index_name)

        # 検索クエリを実行
        query = {
            "query": {
                "match_all": {}  # すべてのドキュメントを取得
            }
        }
        
        result = client.search(
            index=index_name,
            body=query
        )
        
        return {
            'statusCode': 200,
            'body': result
        }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'body': str(e)
        }
