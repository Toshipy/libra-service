import os
from dotenv import load_dotenv
from opensearchpy import OpenSearch

load_dotenv()  # .envファイルを読み込む

def main() -> None:
    host = "localhost"
    port = 9200
    auth = (
        "admin",
        os.getenv("OPENSEARCH_INITIAL_ADMIN_PASSWORD"),
    )
    
    # クライアントを作成
    client = OpenSearch(
        hosts=[{"host": host, "port": port}],
        http_auth=auth,
        use_ssl=True,
        verify_certs=False,
        ssl_show_warn=False,
    )

    index_name = "japanese-folktales"

    # インデックスを作成
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
    else:
        query = {"query": {"match_all": {}}}
        client.delete_by_query(index=index_name, body=query)

    folktales = [
        {
            "name": "桃太郎",
            "story": "桃川上から流れてきた大きな桃から生まれた桃太郎が、犬・猿・きじを家来にして、鬼を討伐する",
            "attributes": ["正義感", "チームワーク", "勇気"],
        },
        {
            "name": "浦島太郎",
            "story": "浦島太郎は、亀を助けたことで竜宮城へ招かれ、そこで時の流れを忘れる。しかし、地上に戻ると時が大きく過ぎていて驚く。",
            "attributes": ["弱いものを守る", "約束", "玉手箱"],
        },
        {
            "name": "かぐや姫",
            "story": "竹の中から現れた美しい女性、かぐや姫は多くの求婚者を試しふるいにかけ、最終的には月に帰る。",
            "attributes": ["知的", "お金と権力", "結婚"],
        },
        {
            "name": "一寸法師",
            "story": "一寸法師は非常に小さな男の子で、大小の武器を使って大きな冒険を繰り広げる。最終的には巨大な鬼を倒す。",
            "attributes": ["お椀の舟", "機転", "打ち出の小槌"],
        },
        {
            "name": "金太郎",
            "story": "赤い服を着た力持ちの金太郎は、山の動物たちと毎日楽しく過ごしていた。最終的にはお偉いさんの家来となる。",
            "attributes": ["強い", "急ぐな休むな", "まさかり"],
        }
    ]

    print('\nデータを格納 ... \n')

    # インデックスにデータを格納
    for folktale in folktales:
        response = client.index(index=index_name, body=folktale)
        print(f"id: {response['_id']}, name: {folktale['name']}")

    query = {
        "query": {
            "match": {
                "story": "鬼"
            }
        }
    }

    # インデックスのデータを検索
    search_response = client.search(index=index_name, body=query)
    print("\nデータを検索 ... \n")
    print("鬼が登場する話:")
    print(f"ヒット数: {search_response['hits']['total']['value']}")
    for hit in search_response['hits']['hits']:
        print(f"* {hit['_source']['name']} (スコア: {hit['_score']})")
        print(f"  ストーリー: {hit['_source']['story']}")
        print()


if __name__ == "__main__":
    main()
