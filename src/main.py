import datetime
from fastapi import FastAPI, HTTPException
from opensearchpy import OpenSearch
from mangum import Mangum
import os
from src.schemas import Book, SearchResult, SearchResponse
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

@app.get("/books",response_model=SearchResult, summary="Search for a character", description="Search for a character by name")
async def search(keyword: str=None):
  try:
    client = get_opensearch_client()

    query = {
      "query": {
        "multi_match": {
          "query": keyword,
          "fields": ["title", "story", "attributes"]
        }
      }
    }

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
async def create_book(book: Book):
  try:
    client = get_opensearch_client()
    now = datetime.datetime.now().isoformat()
    document = {
      "id": book.id,
      "title": book.title,
      "story": book.story,
      "attributes": book.attributes,
      "created_at": now,
      "updated_at": now
    }
    
    response = client.index(index="japanese-folktales", body=document, id=book.id)
    
    return document
  except Exception as e:
    raise HTTPException(status_code=500, detail=str(e))
  
# インデックス初期化用のエンドポイント
@app.post("/initialize")
async def initialize_index():
    try:
        client = get_opensearch_client()
        index_name = "japanese-folktales"

        # インデックスが存在する場合は削除
        if client.indices.exists(index=index_name):
            client.indices.delete(index=index_name)

        # マッピングを定義
        mapping = {
            "mappings": {
                "properties": {
                    "id": {"type": "integer"},
                    "title": {"type": "text"},
                    "story": {"type": "text"},
                    "attributes": {"type": "text"},
                    "created_at": {"type": "date"},
                    "updated_at": {"type": "date"}
                }
            }
        }

        # インデックスを作成
        client.indices.create(index=index_name, body=mapping)

        # サンプルデータ
        books = [
            {
                "id": 1,
                "title": "桃太郎",
                "story": "桃川上から流れてきた大きな桃から生まれた桃太郎が、犬・猿・きじを家来にして、鬼を討伐する",
                "attributes": ["正義感", "チームワーク", "勇気"],
            },
            {
                "id": 2,
                "title": "浦島太郎",
                "story": "浦島太郎は、亀を助けたことで竜宮城へ招かれ、そこで時の流れを忘れる。しかし、地上に戻ると時が大きく過ぎていて驚く。",
                "attributes": ["弱いものを守る", "約束", "玉手箱"],
            },
            {
                "id": 3,
                "title": "かぐや姫",
            "story": "竹の中から現れた美しい女性、かぐや姫は多くの求婚者を試しふるいにかけ、最終的には月に帰る。",
                "attributes": ["知的", "お金と権力", "結婚"],
            },
            {
                "id": 4,
                "title": "一寸法師",
                "story": "一寸法師は非常に小さな男の子で、大小の武器を使って大きな冒険を繰り広げる。最終的には巨大な鬼を倒す。",
                "attributes": ["お椀の舟", "機転", "打ち出の小槌"],
            },
            {
                "id": 5,
                "title": "金太郎",
                "story": "赤い服を着た力持ちの金太郎は、山の動物たちと毎日楽しく過ごしていた。最終的にはお偉いさんの家来となる。",
                "attributes": ["強い", "急ぐな休むな", "まさかり"],
            }
          ]

        # データを投入
        now = datetime.datetime.now().isoformat()
        for book in books:
            book["created_at"] = now
            book["updated_at"] = now
            client.index(
                index=index_name,
                body=book,
                id=str(book["id"])
            )

        return {"message": "Index initialized with sample data"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

handler = Mangum(app)
